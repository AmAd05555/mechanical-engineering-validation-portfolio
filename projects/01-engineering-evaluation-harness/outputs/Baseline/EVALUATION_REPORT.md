# Automated Engineering Evaluation Report

**Overall status:** PASS
**Overall score:** 99.3/100

| Domain | Score | Status |
|---|---:|---|
| CAD | 100.000 | PASS |
| Static FEA | 98.283 | PASS |
| Thermal FEA | 99.955 | PASS |

## Deterministic Input Fingerprints

- **cad:** `7f6e8c037cc0d841a9db9d14d1587bf32996c63a83f47be9a83feb23b36271eb`
- **static_fea:** `9ca01d331bee5a603a05562675d3f3451ba50fdd46fe17fbca81138c31846dbf`
- **thermal_fea:** `38eeb7f435149c7d028e153d03da60b98a3c7a8c5a24aad0240e50d008d2c3b0`
- **rules:** `0b41e9300184878d2e2f7cff2d6f1b594f52cd1eb4643087ddd698301ce1bfd8`

## Detailed Checks

### CAD

| Configuration | Check | Status | Actual | Expected |
|---|---|---|---:|---|
| Compact | slot_clearance | PASS | 2 | > 0 mm radial/diametral clearance |
| Compact | guide_hole_clearance | PASS | 0.5 | > 0 mm |
| Compact | slider_smaller_than_base_X | PASS | 110 | < 190 |
| Compact | slider_smaller_than_base_Y | PASS | 90 | < 120 |
| Compact | requested_travel_within_slot | PASS | 28 | <= 30.00 mm |
| Compact | motor_pattern_inside_slider_X | PASS | 34.25 | < 55.0 |
| Compact | motor_pattern_inside_slider_Y | PASS | 24.25 | < 45.0 |
| Compact | base_geometry_build | PASS | 167308.81 | > 0 |
| Compact | slider_geometry_build | PASS | 94921.14 | > 0 |
| Extended | slot_clearance | PASS | 2 | > 0 mm radial/diametral clearance |
| Extended | guide_hole_clearance | PASS | 0.5 | > 0 mm |
| Extended | slider_smaller_than_base_X | PASS | 150 | < 260 |
| Extended | slider_smaller_than_base_Y | PASS | 120 | < 160 |
| Extended | requested_travel_within_slot | PASS | 52 | <= 55.00 mm |
| Extended | motor_pattern_inside_slider_X | PASS | 44.25 | < 75.0 |
| Extended | motor_pattern_inside_slider_Y | PASS | 34.25 | < 60.0 |
| Extended | base_geometry_build | PASS | 308108.81 | > 0 |
| Extended | slider_geometry_build | PASS | 175921.14 | > 0 |
| Standard | slot_clearance | PASS | 2 | > 0 mm radial/diametral clearance |
| Standard | guide_hole_clearance | PASS | 0.5 | > 0 mm |
| Standard | slider_smaller_than_base_X | PASS | 130 | < 220 |
| Standard | slider_smaller_than_base_Y | PASS | 110 | < 140 |
| Standard | requested_travel_within_slot | PASS | 40 | <= 40.00 mm |
| Standard | motor_pattern_inside_slider_X | PASS | 39.25 | < 65.0 |
| Standard | motor_pattern_inside_slider_Y | PASS | 29.25 | < 55.0 |
| Standard | base_geometry_build | PASS | 227468.81 | > 0 |
| Standard | slider_geometry_build | PASS | 138921.14 | > 0 |

### Static FEA

| Metric | Actual | Limit | Status | Score |
|---|---:|---:|---|---:|
| tip_deflection_error_pct | 0.5239976814345839 | 5.0 | PASS | 94.76 |
| stress_error_pct | 0.33464954790122065 | 5.0 | PASS | 96.654 |
| force_balance_error_pct | 4.699434915285868e-10 | 0.1 | PASS | 100.0 |
| moment_balance_error_pct | 4.474422894418239e-10 | 0.1 | PASS | 100.0 |
| nominal_root_stress_below_yield | True | True | PASS | 100.0 |

### Thermal FEA

| Metric | Actual | Limit | Status | Score |
|---|---:|---:|---|---:|
| tip_excess_temperature_error_pct | 0.001188 | 1.0 | PASS | 99.941 |
| base_heat_error_pct | 0.001492 | 1.0 | PASS | 99.925 |
| energy_balance_error_pct | 0.0 | 0.5 | PASS | 100.0 |
