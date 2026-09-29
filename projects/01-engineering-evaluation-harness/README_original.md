# Automated Engineering Evaluation Harness

A deterministic Python evaluation pipeline that consumes validation outputs from three engineering benchmarks:

1. Parametric CAD model validation
2. Static structural FEA validation against analytical ground truth
3. Steady-state thermal FEA validation against analytical ground truth

The harness applies configurable engineering acceptance criteria, computes domain scores, produces an overall weighted score, and emits PASS/FAIL reports in JSON, CSV and Markdown.

## Why this project exists
The goal is to demonstrate an engineering-evaluation workflow rather than merely running CAD or simulation software. It separates **generation** from **evaluation** and uses explicit deterministic rules to decide whether engineering outputs are acceptable.

## Baseline result
Run `python 01_Source/evaluation_harness.py ...` using the baseline inputs. The included baseline dataset passes all engineering criteria.

## Failure demonstration
The `03_Inputs/Failure_Cases` folder contains intentionally corrupted results. Running the same evaluator on those inputs returns FAIL, demonstrating that the harness detects unacceptable CAD and physics results.

## Outputs
- `evaluation_report.json` — machine-readable detailed result
- `score_summary.csv` — compact domain score table
- `EVALUATION_REPORT.md` — human-readable engineering report

## Determinism
The report stores SHA-256 hashes for every input file and the rule configuration. Identical inputs and rules produce identical evaluation results. Unit tests explicitly verify repeatability.

## Run baseline
```bash
python 01_Source/evaluation_harness.py   --cad 03_Inputs/Baseline/cad_validation.json   --static 03_Inputs/Baseline/static_validation.json   --thermal 03_Inputs/Baseline/thermal_validation.json   --rules 02_Config/evaluation_rules.json   --outdir 04_Outputs/Baseline
```

## Run tests
```bash
python -m unittest discover 05_Tests -v
```
