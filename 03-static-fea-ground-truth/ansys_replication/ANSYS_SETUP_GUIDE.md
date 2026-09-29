# ANSYS Workbench Replication Guide

Use this guide to recreate the benchmark in ANSYS Mechanical and compare it with the supplied independent Python FEA solver.

## 1. Geometry
Import `../01_CAD/Cantilever_Benchmark.step`.
Dimensions: 250 × 30 × 10 mm.

For the closest match to the Python plane-stress benchmark, you may instead create a **2D surface body** 250 × 30 mm and assign thickness = 10 mm.

## 2. Material
Structural Steel:
- Young's modulus = 210000 MPa
- Poisson ratio = 0.30
- Nominal yield strength used for project check = 250 MPa

## 3. Supports
Fix the entire left edge (X = 0). For the 2D model, constrain both UX and UY.

## 4. Load
Apply total downward force = 600 N to the right edge.
For an edge traction representation, distribute it uniformly across the right edge.

## 5. Mesh study
Run three meshes approximately equivalent to:
- Coarse: 20 × 4 elements
- Medium: 50 × 8 elements
- Fine: 100 × 12 elements

Use mapped quadrilateral elements on the 2D rectangle if available.

## 6. Results to request
- Directional deformation Y at free-end midpoint
- Normal stress X along an interior vertical section around X = 62.5 mm
- Equivalent von Mises stress
- Reaction force at fixed support
- Reaction moment at fixed support

## 7. Ground truth
- Tip deflection = 0.661376 mm downward
- Root nominal bending stress = 100.000 MPa
- Expected vertical reaction magnitude = 600.000 N
- Expected root reaction moment magnitude = 150000.000 N·mm

## 8. Important interpretation note
Do not validate the model solely using the single highest stress at the fixed-edge corners. Compare a physically equivalent interior section/sample to beam theory, then separately inspect local stress concentrations/boundary artifacts.
