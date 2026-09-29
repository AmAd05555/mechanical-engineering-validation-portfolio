# StoryGold Project 02 — Static FEA Ground-Truth Benchmark

## Project goal
Build and validate a reproducible static structural benchmark that compares finite-element results against closed-form engineering calculations. The project is designed to demonstrate **FEA fundamentals, boundary-condition discipline, ground-truth validation, mesh convergence, reaction equilibrium, and engineering interpretation**.

## Model
- Geometry: rectangular cantilever plate/beam
- Length: **250 mm**
- Height: **30 mm**
- Thickness: **10 mm**
- Material: Structural Steel, **E = 210 GPa**, **nu = 0.30**, nominal yield = **250 MPa**
- Boundary condition: left edge fixed in X and Y
- Load: **600 N downward**, represented as uniform end traction on the right edge
- FEA idealization: 2D plane-stress Q4 bilinear quadrilateral elements

## Analytical ground truth
- Second moment of area: **22,500 mm^4**
- Root surface bending stress: **100.000 MPa**
- Euler-Bernoulli tip deflection: **0.661376 mm**
- Nominal yield factor of safety: **2.500**

## Mesh study
| mesh   |   nx |   ny |   elements |   nodes |   tip_deflection_fea_mm |   tip_deflection_analytical_mm |   tip_deflection_error_pct |   stress_sample_x_mm |   stress_sample_y_mm |   sigma_x_fea_MPa |   sigma_x_analytical_MPa |   stress_error_pct |   reaction_y_N |   reaction_moment_Nmm |   force_balance_error_pct |   moment_balance_error_pct |
|:-------|-----:|-----:|-----------:|--------:|------------------------:|-------------------------------:|---------------------------:|---------------------:|---------------------:|------------------:|-------------------------:|-------------------:|---------------:|----------------------:|--------------------------:|---------------------------:|
| Coarse |   20 |    4 |         80 |     105 |                0.620311 |                       0.661376 |                   6.20904  |                56.25 |               11.25  |           54.1741 |                  58.125  |            6.79721 |            600 |                150000 |               6.85683e-10 |                6.11083e-10 |
| Medium |   50 |    8 |        400 |     459 |                0.658682 |                       0.661376 |                   0.407301 |                62.5  |               13.125 |           64.8322 |                  65.625  |            1.20814 |            600 |                150000 |               8.16992e-10 |                1.17271e-09 |
| Fine   |  100 |   12 |       1200 |    1313 |                0.664841 |                       0.661376 |                   0.523998 |                61.25 |               13.75  |           68.9767 |                  69.2083 |            0.33465 |            600 |                150000 |               4.69943e-10 |                4.47442e-10 |

## Validation outcome
Fine mesh pass status: **PASS**

The fine mesh is checked against:
1. analytical tip deflection,
2. analytical bending stress at a matching interior section/sample location,
3. total vertical reaction equilibrium,
4. reaction moment equilibrium,
5. nominal yield check.

## Folder map
- `01_CAD/` — STEP/STL/DXF geometry
- `02_FEA_Solver/` — self-contained Python Q4 plane-stress solver
- `03_Analytical_Ground_Truth/` — hand-equation equivalent script and results
- `04_Mesh_Convergence/` — mesh convergence CSV/JSON/charts
- `05_Validation/` — pass/fail validation summary
- `06_ANSYS_Replication/` — exact ANSYS Workbench setup instructions
- `07_Portfolio/` — portfolio case study and interview notes
- `08_Renders/` — CAD/deformation/stress visual evidence
- `09_Raw_Results/` — nodal displacement, element stress, node and connectivity data

## What this project proves
- Correct definition of material, loads, supports, and plane-stress assumptions
- Independent analytical verification instead of trusting the solver blindly
- Mesh-convergence testing
- Interpretation of stress and displacement results
- Force/moment equilibrium checks
- Ability to reproduce the same benchmark in ANSYS
