# Validation Report — Static FEA Ground-Truth Benchmark

## Acceptance criteria
- Fine-mesh tip-deflection error < 5%: **PASS** (0.524%)
- Fine-mesh section-stress error < 5%: **PASS** (0.335%)
- Vertical reaction balance error < 0.1%: **PASS** (0.000000%)
- Reaction-moment balance error < 0.1%: **PASS** (0.000000%)
- Nominal analytical root stress below yield: **PASS**

## Fine mesh numerical results
- Elements: 1200
- Nodes: 1313
- FEA tip deflection: 0.664841 mm
- Analytical tip deflection: 0.661376 mm
- FEA sample sigma_x: 68.976728 MPa
- Analytical sigma_x at same centroid: 69.208333 MPa
- Total Y reaction: 600.000000 N
- Reaction moment: 149999.999999 N·mm
- Expected reaction moment magnitude: 150000.000000 N·mm

## Interpretation
The benchmark intentionally compares stress away from the fixed-edge corner because a fully fixed 2D continuum can produce local boundary effects that are not represented by elementary beam theory. The comparison therefore uses the same physical section and sample coordinate in both the analytical and FE models.

This is an important engineering-validation principle: **do not compare unlike quantities simply because both are called “maximum stress.”**
