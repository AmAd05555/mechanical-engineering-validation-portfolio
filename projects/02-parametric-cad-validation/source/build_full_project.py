from pathlib import Path
import cadquery as cq
from cadquery import exporters
import json, math, csv, shutil, os

ROOT = Path(__file__).resolve().parents[1] / 'generated_full_project'
if ROOT.exists():
    shutil.rmtree(ROOT)
for d in [
    '01_Parts_STEP','02_Assembly_STEP','03_STL','04_DXF','05_Source','06_Validation','07_Debug_Cases','08_Renders'
]:
    (ROOT/d).mkdir(parents=True, exist_ok=True)

CONFIGS = {
    'Compact': dict(base_l=190, base_w=120, base_t=8, slot_l=70, slot_w=12, slot_offset=35,
                    slider_l=110, slider_w=90, slider_t=10, motor_pitch_x=60, motor_pitch_y=40,
                    motor_hole_d=8.5, guide_hole_d=10.5, pin_d=10, travel=28, edge_fillet=4),
    'Standard': dict(base_l=220, base_w=140, base_t=8, slot_l=90, slot_w=12, slot_offset=45,
                    slider_l=130, slider_w=110, slider_t=10, motor_pitch_x=70, motor_pitch_y=50,
                    motor_hole_d=8.5, guide_hole_d=10.5, pin_d=10, travel=40, edge_fillet=4),
    'Extended': dict(base_l=260, base_w=160, base_t=8, slot_l=120, slot_w=12, slot_offset=50,
                    slider_l=150, slider_w=120, slider_t=10, motor_pitch_x=80, motor_pitch_y=60,
                    motor_hole_d=8.5, guide_hole_d=10.5, pin_d=10, travel=52, edge_fillet=4),
}

def rounded_box(l,w,h,r):
    wp = cq.Workplane('XY').rect(l,w).extrude(h)
    # fillet only vertical edges to avoid issues on thin plates
    if r > 0:
        try:
            wp = wp.edges('|Z').fillet(r)
        except Exception:
            pass
    return wp

def base_plate(p):
    part = rounded_box(p['base_l'], p['base_w'], p['base_t'], p['edge_fillet'])
    # two straight slots parallel X
    for y in (p['slot_offset'], -p['slot_offset']):
        cutter = (cq.Workplane('XY')
                  .center(0,y)
                  .slot2D(p['slot_l'], p['slot_w'], angle=0)
                  .extrude(p['base_t']+2))
        part = part.cut(cutter)
    # chassis holes
    xh = p['base_l']/2 - 20
    yh = p['base_w']/2 - 15
    holes = [(xh,yh),(xh,-yh),(-xh,yh),(-xh,-yh)]
    part = part.faces('>Z').workplane().pushPoints(holes).hole(9)
    return part

def slider_plate(p):
    part = rounded_box(p['slider_l'], p['slider_w'], p['slider_t'], 3)
    # motor mounting holes, symmetric around origin
    xs = p['motor_pitch_x']/2
    ys = p['motor_pitch_y']/2
    holes = [(xs,ys),(xs,-ys),(-xs,ys),(-xs,-ys)]
    part = part.faces('>Z').workplane().pushPoints(holes).hole(p['motor_hole_d'])
    # guide holes aligned with base slots
    guide = [(0,p['slot_offset']),(0,-p['slot_offset'])]
    part = part.faces('>Z').workplane().pushPoints(guide).hole(p['guide_hole_d'])
    return part

def stop_bracket():
    # horizontal foot 40 x 30 x 6; vertical plate 6 x 30 x 35 at back edge
    foot = cq.Workplane('XY').box(40,30,6, centered=(True,True,False))
    vertical = cq.Workplane('XY').box(6,30,35, centered=(True,True,False)).translate((-17,0,6))
    bracket = foot.union(vertical)
    # through hole in vertical plate, axis X
    cutter = (cq.Workplane('YZ').center(0, 6+18).circle(5.25).extrude(20, both=True))
    bracket = bracket.cut(cutter)
    # two foot mounting holes
    bracket = bracket.faces('>Z').workplane().pushPoints([(8,0),(-8,0)]).hole(6.5)
    return bracket

def guide_pin():
    shaft = cq.Workplane('XY').circle(5).extrude(25)
    head = cq.Workplane('XY').circle(8).extrude(4)
    return shaft.union(head)

def motor_envelope(p):
    # simple reference envelope only, not a manufactured part
    body = cq.Workplane('XY').box(80,65,55, centered=(True,True,False))
    shaft = cq.Workplane('YZ').circle(8).extrude(30).translate((40,0,27.5))
    return body.union(shaft)

def export_part(shape, name):
    exporters.export(shape, str(ROOT/'01_Parts_STEP'/f'{name}.step'))
    exporters.export(shape, str(ROOT/'03_STL'/f'{name}.stl'))

def export_top_dxf(shape, name):
    # project top face wires to a 2D workplane via section of top face edges
    try:
        top_edges = shape.faces('>Z').edges()
        exporters.exportDXF(top_edges, str(ROOT/'04_DXF'/f'{name}_TopView.dxf'))
    except Exception as e:
        (ROOT/'04_DXF'/f'{name}_DXF_ERROR.txt').write_text(str(e))

def make_assembly(p, slider_x=0, exploded=False, include_motor=True):
    b = base_plate(p)
    s = slider_plate(p)
    br = stop_bracket()
    pin = guide_pin()
    motor = motor_envelope(p)
    assy = cq.Assembly(name='AdjustableMotorMount')
    assy.add(b, name='BasePlate', loc=cq.Location(cq.Vector(0,0,0)))
    # slider on top of base
    z_slider = p['base_t']
    assy.add(s, name='SliderPlate', loc=cq.Location(cq.Vector(slider_x,0,z_slider + (25 if exploded else 0))))
    # pins: head at bottom, shafts passing upward through slider
    for i, y in enumerate((p['slot_offset'],-p['slot_offset']), start=1):
        zpin = 0 if not exploded else 15
        assy.add(pin, name=f'GuidePin_{i}', loc=cq.Location(cq.Vector(slider_x,y,zpin)))
    # bracket near left end on top
    xbr = -p['base_l']/2 + 25
    assy.add(br, name='StopBracket', loc=cq.Location(cq.Vector(xbr,0,p['base_t'] + (50 if exploded else 0))))
    if include_motor:
        assy.add(motor, name='MotorEnvelope', loc=cq.Location(cq.Vector(slider_x,0,p['base_t']+p['slider_t'] + (70 if exploded else 0))))
    return assy

def validate_config(name,p):
    results=[]
    def check(key, ok, actual, expected):
        results.append(dict(check=key,status='PASS' if ok else 'FAIL',actual=actual,expected=expected))
    check('slot_clearance', p['slot_w'] > p['pin_d'], p['slot_w']-p['pin_d'], '> 0 mm radial/diametral clearance')
    check('guide_hole_clearance', p['guide_hole_d'] > p['pin_d'], p['guide_hole_d']-p['pin_d'], '> 0 mm')
    check('slider_smaller_than_base_X', p['slider_l'] < p['base_l'], p['slider_l'], f"< {p['base_l']}")
    check('slider_smaller_than_base_Y', p['slider_w'] < p['base_w'], p['slider_w'], f"< {p['base_w']}")
    max_travel = (p['slot_l'] - p['pin_d'])/2
    check('requested_travel_within_slot', p['travel'] <= max_travel+1e-9, p['travel'], f'<= {max_travel:.2f} mm')
    check('motor_pattern_inside_slider_X', p['motor_pitch_x']/2 + p['motor_hole_d']/2 < p['slider_l']/2,
          p['motor_pitch_x']/2 + p['motor_hole_d']/2, f"< {p['slider_l']/2}")
    check('motor_pattern_inside_slider_Y', p['motor_pitch_y']/2 + p['motor_hole_d']/2 < p['slider_w']/2,
          p['motor_pitch_y']/2 + p['motor_hole_d']/2, f"< {p['slider_w']/2}")
    # model build check
    try:
        b=base_plate(p); s=slider_plate(p)
        check('base_geometry_build', b.val().Volume()>0, round(b.val().Volume(),2), '> 0')
        check('slider_geometry_build', s.val().Volume()>0, round(s.val().Volume(),2), '> 0')
    except Exception as e:
        check('geometry_build', False, str(e), 'successful CAD rebuild')
    return results

# Build Standard individual parts
std=CONFIGS['Standard']
parts={'BasePlate':base_plate(std),'SliderPlate':slider_plate(std),'StopBracket':stop_bracket(),'GuidePin':guide_pin(),'MotorEnvelope_REFERENCE':motor_envelope(std)}
for n,sh in parts.items():
    export_part(sh,n)
    if n in ('BasePlate','SliderPlate'):
        export_top_dxf(sh,n)

# Export assemblies/configurations, centered and travel endpoints
for cfg,p in CONFIGS.items():
    assy=make_assembly(p,0)
    exporters.assembly.exportAssembly(assy, str(ROOT/'02_Assembly_STEP'/f'AdjustableMotorMount_{cfg}.step'))
    # individual config parts for direct comparison
    exporters.export(base_plate(p), str(ROOT/'01_Parts_STEP'/f'BasePlate_{cfg}.step'))
    exporters.export(slider_plate(p), str(ROOT/'01_Parts_STEP'/f'SliderPlate_{cfg}.step'))

# Travel endpoint assemblies Standard
for label,x in [('Travel_Left',-std['travel']),('Centered',0),('Travel_Right',std['travel'])]:
    exporters.assembly.exportAssembly(make_assembly(std,x), str(ROOT/'02_Assembly_STEP'/f'AdjustableMotorMount_{label}.step'))
exporters.assembly.exportAssembly(make_assembly(std,0,exploded=True), str(ROOT/'02_Assembly_STEP'/'AdjustableMotorMount_Exploded.step'))

# Validation reports
all_reports={}
for cfg,p in CONFIGS.items():
    all_reports[cfg]=validate_config(cfg,p)
(ROOT/'06_Validation'/'validation_report.json').write_text(json.dumps(all_reports,indent=2))
with open(ROOT/'06_Validation'/'validation_report.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['Configuration','Check','Status','Actual','Expected'])
    for cfg,rows in all_reports.items():
        for r in rows: w.writerow([cfg,r['check'],r['status'],r['actual'],r['expected']])

# Debug cases: intentionally invalid parameter scenarios, deterministic validator results
DEBUGS = {
    'Debug01_SlotTooNarrow': {**std, 'slot_w': 9.0},
    'Debug02_ExcessTravel': {**std, 'travel': 50.0},
    'Debug03_SliderTooWide': {**std, 'slider_w': 150.0},
    'Debug04_MotorPatternOutsidePlate': {**std, 'motor_pitch_x': 130.0},
    'Debug05_GuideHoleInterference': {**std, 'guide_hole_d': 9.5},
}
for name,p in DEBUGS.items():
    rep=validate_config(name,p)
    (ROOT/'07_Debug_Cases'/f'{name}.json').write_text(json.dumps({'parameters':p,'validation':rep},indent=2))

# Parametric source code with clean API
source = r'''"""Parametric Adjustable Motor Mount benchmark project.
Generated for CAD validation, geometry robustness, configuration testing, and debugging practice.
Units: mm.
"""
import cadquery as cq

DEFAULT = dict(
    base_l=220, base_w=140, base_t=8,
    slot_l=90, slot_w=12, slot_offset=45,
    slider_l=130, slider_w=110, slider_t=10,
    motor_pitch_x=70, motor_pitch_y=50,
    motor_hole_d=8.5, guide_hole_d=10.5,
    pin_d=10, travel=40, edge_fillet=4,
)

def base_plate(p=DEFAULT):
    base = cq.Workplane("XY").rect(p["base_l"],p["base_w"]).extrude(p["base_t"])
    for y in (p["slot_offset"],-p["slot_offset"]):
        slot=(cq.Workplane("XY").center(0,y).slot2D(p["slot_l"],p["slot_w"]).extrude(p["base_t"]+2))
        base=base.cut(slot)
    xh=p["base_l"]/2-20; yh=p["base_w"]/2-15
    base=base.faces(">Z").workplane().pushPoints([(xh,yh),(xh,-yh),(-xh,yh),(-xh,-yh)]).hole(9)
    return base

def slider_plate(p=DEFAULT):
    s=cq.Workplane("XY").rect(p["slider_l"],p["slider_w"]).extrude(p["slider_t"])
    xs=p["motor_pitch_x"]/2; ys=p["motor_pitch_y"]/2
    s=s.faces(">Z").workplane().pushPoints([(xs,ys),(xs,-ys),(-xs,ys),(-xs,-ys)]).hole(p["motor_hole_d"])
    s=s.faces(">Z").workplane().pushPoints([(0,p["slot_offset"]),(0,-p["slot_offset"])]).hole(p["guide_hole_d"])
    return s

def deterministic_checks(p=DEFAULT):
    max_travel=(p["slot_l"]-p["pin_d"])/2
    return {
      "slot_clearance": p["slot_w"] > p["pin_d"],
      "guide_hole_clearance": p["guide_hole_d"] > p["pin_d"],
      "slider_inside_base": p["slider_l"] < p["base_l"] and p["slider_w"] < p["base_w"],
      "travel_valid": p["travel"] <= max_travel,
      "motor_pattern_inside_slider": (p["motor_pitch_x"]/2+p["motor_hole_d"]/2 < p["slider_l"]/2 and p["motor_pitch_y"]/2+p["motor_hole_d"]/2 < p["slider_w"]/2),
    }
'''
(ROOT/'05_Source'/'parametric_motor_mount.py').write_text(source)

# Validation script standalone
validator = r'''import json
from pathlib import Path
from parametric_motor_mount import DEFAULT, deterministic_checks
print(json.dumps(deterministic_checks(DEFAULT), indent=2))
'''
(ROOT/'05_Source'/'run_validation.py').write_text(validator)

# SolidWorks import notes
(ROOT/'SOLIDWORKS_IMPORT.md').write_text('''# SolidWorks import / continuation\n\n1. Open each `.step` file directly in SolidWorks.\n2. Use **File > Save As** to save imported parts as `.SLDPRT` and assemblies as `.SLDASM`.\n3. STEP preserves the exact solid geometry but not the original CadQuery feature history.\n4. For a native SolidWorks feature tree, rebuild the BasePlate and SliderPlate using the parameter table in `README.md`; use the STEP bodies as geometric references/checks.\n5. The source of truth for parametric behavior is `05_Source/parametric_motor_mount.py`.\n6. Compare rebuilt SolidWorks geometry against the STEP files using **Evaluate > Compare Geometry** where available.\n''')

# Readme
README = f'''# Adjustable Motor Mount — Parametric CAD Validation Benchmark\n\n## Purpose\nA real, generated CAD project built to demonstrate parametric mechanical design, configuration testing, deterministic geometry checks, motion-range reasoning, and CAD debugging practice. It maps closely to CAD-evaluation work involving geometry validity, constraints/parameters, rebuild robustness, and automated checks.\n\n## Deliverables\n- STEP solids for all parts\n- STEP assemblies for Compact / Standard / Extended configurations\n- STEP assemblies for left / centered / right travel states\n- Exploded assembly STEP\n- STL meshes for quick viewing\n- DXF top views for BasePlate and SliderPlate\n- Parametric CadQuery source\n- Automated validation report (CSV + JSON)\n- Five deliberately invalid parameter cases for debugging practice\n- SolidWorks import/rebuild instructions\n\n## Standard configuration\n- Base plate: 220 x 140 x 8 mm\n- Base slots: 90 x 12 mm, Y offsets ±45 mm\n- Slider plate: 130 x 110 x 10 mm\n- Motor mounting pattern: 70 x 50 mm, Ø8.5 mm\n- Guide holes: Ø10.5 mm\n- Guide pins: Ø10 mm\n- Requested travel: ±40 mm\n- Base chassis holes: Ø9 mm\n\n## Configurations\n### Compact\nBase 190 x 120; Slider 110 x 90; slots 70; slot offset 35; travel ±28.\n\n### Standard\nBase 220 x 140; Slider 130 x 110; slots 90; slot offset 45; travel ±40.\n\n### Extended\nBase 260 x 160; Slider 150 x 120; slots 120; slot offset 50; travel ±52.\n\n## Deterministic validation rules\n1. Slot width must exceed guide-pin diameter.\n2. Guide hole must exceed guide-pin diameter.\n3. Slider must remain inside the base footprint.\n4. Requested travel must fit the slot geometry.\n5. Motor-hole pattern must remain inside slider boundaries.\n6. Base and slider solids must rebuild to positive volume.\n\n## Debug cases\n- Debug01: slot narrower than guide pin\n- Debug02: requested travel exceeds geometric range\n- Debug03: slider wider than base\n- Debug04: motor-hole pattern outside slider boundary\n- Debug05: guide-hole interference with guide pin\n\nThese cases are intentionally invalid and are caught by the validator.\n\n## Suggested portfolio statement after reviewing and understanding the project\nDesigned and validated a parametric adjustable motor-mount benchmark with multiple dimensional configurations, controlled slider travel, and deterministic geometry checks; investigated invalid parameter states including clearance, travel, envelope, and hole-pattern failures.\n\n## Important\nThe native parametric source in this package is CadQuery, which is one of the parametric CAD tools listed in StoryGold's CAD Evaluation Engineer requirements. STEP files open directly in SolidWorks, but STEP does not preserve a native SolidWorks feature tree.\n'''
(ROOT/'README.md').write_text(README)

# create manifest
manifest=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file():
        manifest.append(str(p.relative_to(ROOT)))
(ROOT/'MANIFEST.txt').write_text('\n'.join(manifest))
print(ROOT)
