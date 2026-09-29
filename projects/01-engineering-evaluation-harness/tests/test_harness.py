import json, tempfile, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
from evaluation_harness import evaluate
class HarnessTests(unittest.TestCase):
    def p(self,*x): return ROOT.joinpath(*x)
    def test_baseline_passes(self):
        r=evaluate(self.p('inputs/Baseline/cad_validation.json'),self.p('inputs/Baseline/static_validation.json'),self.p('inputs/Baseline/thermal_validation.json'),self.p('config/evaluation_rules.json'))
        self.assertEqual(r['status'],'PASS'); self.assertGreaterEqual(r['overall_score'],85)
    def test_failure_case_fails(self):
        r=evaluate(self.p('inputs/Failure_Cases/cad_failure.json'),self.p('inputs/Failure_Cases/static_failure.json'),self.p('inputs/Failure_Cases/thermal_failure.json'),self.p('config/evaluation_rules.json'))
        self.assertEqual(r['status'],'FAIL')
    def test_deterministic(self):
        args=[self.p('inputs/Baseline/cad_validation.json'),self.p('inputs/Baseline/static_validation.json'),self.p('inputs/Baseline/thermal_validation.json'),self.p('config/evaluation_rules.json')]
        self.assertEqual(evaluate(*args),evaluate(*args))
if __name__=='__main__': unittest.main()
