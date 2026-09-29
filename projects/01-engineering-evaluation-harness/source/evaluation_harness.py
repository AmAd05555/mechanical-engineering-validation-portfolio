#!/usr/bin/env python3
import argparse, json, hashlib, csv
from pathlib import Path


def load_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def bounded_metric_score(value, limit):
    # Full credit at zero error, zero credit at/above 2x limit; smooth and deterministic.
    if limit <= 0: return 100.0 if value <= 0 else 0.0
    return round(max(0.0, 100.0 * (1.0 - value/(2.0*limit))), 3)

def eval_cad(data, cfg):
    checks=[]
    for configuration, rows in sorted(data.items()):
        for r in rows:
            checks.append({'configuration':configuration,'check':r['check'],'status':r['status'],'actual':r.get('actual'),'expected':r.get('expected')})
    n=len(checks); passed=sum(c['status']=='PASS' for c in checks)
    ratio=passed/n if n else 0.0
    critical_failures=[c for c in checks if c['check'] in cfg['critical_checks'] and c['status']!='PASS']
    domain_pass=(ratio >= cfg['minimum_pass_ratio']) and not critical_failures
    score=round(100.0*ratio,3)
    return {'domain':'CAD','score':score,'pass':domain_pass,'checks_total':n,'checks_passed':passed,'pass_ratio':round(ratio,6),'critical_failures':critical_failures,'details':checks}

def eval_static(data, cfg):
    f=data['fine_mesh']; a=data['analytical']
    metrics={
      'tip_deflection_error_pct': float(f['tip_deflection_error_pct']),
      'stress_error_pct': float(f['stress_error_pct']),
      'force_balance_error_pct': float(f['force_balance_error_pct']),
      'moment_balance_error_pct': float(f['moment_balance_error_pct'])
    }
    limits={
      'tip_deflection_error_pct':cfg['tip_deflection_error_pct_max'],
      'stress_error_pct':cfg['stress_error_pct_max'],
      'force_balance_error_pct':cfg['force_balance_error_pct_max'],
      'moment_balance_error_pct':cfg['moment_balance_error_pct_max']
    }
    rows=[]
    for k in metrics:
        v=metrics[k]; lim=limits[k]
        rows.append({'metric':k,'actual':v,'limit':lim,'status':'PASS' if v<=lim else 'FAIL','score':bounded_metric_score(v,lim)})
    below_yield = bool(data.get('validation_criteria',{}).get('nominal_root_stress_below_yield', a.get('nominal_factor_of_safety_vs_yield',0)>1))
    rows.append({'metric':'nominal_root_stress_below_yield','actual':below_yield,'limit':True,'status':'PASS' if (below_yield or not cfg['require_below_yield']) else 'FAIL','score':100.0 if below_yield else 0.0})
    domain_pass=all(r['status']=='PASS' for r in rows)
    score=round(sum(r['score'] for r in rows)/len(rows),3)
    return {'domain':'Static FEA','score':score,'pass':domain_pass,'details':rows,'key_results':{'analytical_tip_deflection_mm':a['tip_deflection_mm'],'fea_tip_deflection_mm':f['tip_deflection_fea_mm'],'nominal_factor_of_safety':a['nominal_factor_of_safety_vs_yield']}}

def eval_thermal(data, cfg):
    vals={
      'tip_excess_temperature_error_pct':float(data['fine_mesh_tip_excess_error_pct']),
      'base_heat_error_pct':float(data['fine_mesh_base_heat_error_pct']),
      'energy_balance_error_pct':float(data['energy_balance_error_pct'])
    }
    limits={
      'tip_excess_temperature_error_pct':cfg['tip_excess_temperature_error_pct_max'],
      'base_heat_error_pct':cfg['base_heat_error_pct_max'],
      'energy_balance_error_pct':cfg['energy_balance_error_pct_max']
    }
    rows=[]
    for k in vals:
        v=vals[k]; lim=limits[k]
        rows.append({'metric':k,'actual':v,'limit':lim,'status':'PASS' if v<=lim else 'FAIL','score':bounded_metric_score(v,lim)})
    domain_pass=all(r['status']=='PASS' for r in rows)
    score=round(sum(r['score'] for r in rows)/len(rows),3)
    return {'domain':'Thermal FEA','score':score,'pass':domain_pass,'details':rows,'key_results':{'analytic_tip_temperature_C':data['analytic_tip_temperature_C'],'fea_tip_temperature_C':data['fine_mesh_tip_temperature_C'],'analytic_base_heat_W':data['analytic_base_heat_W'],'fea_base_heat_W':data['fine_mesh_base_heat_W']}}

def evaluate(cad_path, static_path, thermal_path, config_path):
    cfg=load_json(config_path)
    cad=eval_cad(load_json(cad_path), cfg['cad'])
    static=eval_static(load_json(static_path), cfg['static_fea'])
    thermal=eval_thermal(load_json(thermal_path), cfg['thermal_fea'])
    weights=cfg['weights']
    overall=round(cad['score']*weights['cad']+static['score']*weights['static_fea']+thermal['score']*weights['thermal_fea'],3)
    domains_pass=all(x['pass'] for x in [cad,static,thermal])
    final_pass=(overall>=cfg['overall_pass_score']) and (domains_pass if cfg['require_each_domain_pass'] else True)
    return {
      'harness_version':cfg['version'],
      'input_hashes':{'cad':sha256_file(cad_path),'static_fea':sha256_file(static_path),'thermal_fea':sha256_file(thermal_path),'rules':sha256_file(config_path)},
      'weights':weights,'overall_score':overall,'threshold_score':cfg['overall_pass_score'],'status':'PASS' if final_pass else 'FAIL',
      'domains':{'cad':cad,'static_fea':static,'thermal_fea':thermal}
    }

def write_csv(report,p):
    rows=[]
    for key,d in report['domains'].items():
        rows.append({'domain':key,'score':d['score'],'status':'PASS' if d['pass'] else 'FAIL'})
    rows.append({'domain':'overall','score':report['overall_score'],'status':report['status']})
    with open(p,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['domain','score','status']); w.writeheader(); w.writerows(rows)

def write_markdown(report,p):
    lines=['# Automated Engineering Evaluation Report','',f"**Overall status:** {report['status']}",f"**Overall score:** {report['overall_score']}/100",'', '| Domain | Score | Status |','|---|---:|---|']
    for k,d in report['domains'].items(): lines.append(f"| {d['domain']} | {d['score']:.3f} | {'PASS' if d['pass'] else 'FAIL'} |")
    lines += ['','## Deterministic Input Fingerprints','']
    for k,v in report['input_hashes'].items(): lines.append(f'- **{k}:** `{v}`')
    lines += ['','## Detailed Checks','']
    for k,d in report['domains'].items():
        lines += [f"### {d['domain']}",'']
        if k=='cad':
            lines += ['| Configuration | Check | Status | Actual | Expected |','|---|---|---|---:|---|']
            for r in d['details']: lines.append(f"| {r['configuration']} | {r['check']} | {r['status']} | {r.get('actual','')} | {r.get('expected','')} |")
        else:
            lines += ['| Metric | Actual | Limit | Status | Score |','|---|---:|---:|---|---:|']
            for r in d['details']: lines.append(f"| {r['metric']} | {r['actual']} | {r['limit']} | {r['status']} | {r['score']} |")
        lines.append('')
    Path(p).write_text('\n'.join(lines),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(description='Deterministic CAD/FEA engineering evaluation harness')
    ap.add_argument('--cad',required=True); ap.add_argument('--static',required=True); ap.add_argument('--thermal',required=True); ap.add_argument('--rules',required=True); ap.add_argument('--outdir',required=True)
    a=ap.parse_args(); out=Path(a.outdir); out.mkdir(parents=True,exist_ok=True)
    r=evaluate(a.cad,a.static,a.thermal,a.rules)
    (out/'evaluation_report.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    write_csv(r,out/'score_summary.csv'); write_markdown(r,out/'EVALUATION_REPORT.md')
    print(json.dumps({'status':r['status'],'overall_score':r['overall_score']},indent=2))
    raise SystemExit(0 if r['status']=='PASS' else 2)
if __name__=='__main__': main()
