# Automated Engineering Evaluation Report

**Overall status:** FAIL
**Overall score:** 44.818/100

| Domain | Score | Status |
|---|---:|---|
| CAD | 92.593 | FAIL |
| Static FEA | 42.600 | FAIL |
| Thermal FEA | 0.000 | FAIL |

## Deterministic Input Fingerprints

- **cad:** `c0f95bf18fc25b872c232319e3dfdd6dc4ab4254cc208df30f9841d5961d255e`
- **static_fea:** `0f18914d3fb6295872b2948bcd48c7bbb9e4bb438306e9fe5ce5ac714c5046b6`
- **thermal_fea:** `b49f004549a2a4af1ffccca22b6df068fec9809602105b47771f59401dcf0470`
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
| Standard | requested_travel_within_slot | FAIL | 55 | <= 40.00 mm |
| Standard | motor_pattern_inside_slider_X | PASS | 39.25 | < 65.0 |
| Standard | motor_pattern_inside_slider_Y | PASS | 29.25 | < 55.0 |
| Standard | base_geometry_build | FAIL | 0 | > 0 |
| Standard | slider_geometry_build | PASS | 138921.14 | > 0 |

### Static FEA

| Metric | Actual | Limit | Status | Score |
|---|---:|---:|---|---:|
| tip_deflection_error_pct | 8.7 | 5.0 | FAIL | 13.0 |
| stress_error_pct | 11.2 | 5.0 | FAIL | 0.0 |
| force_balance_error_pct | 4.699434915285868e-10 | 0.1 | PASS | 100.0 |
| moment_balance_error_pct | 4.474422894418239e-10 | 0.1 | PASS | 100.0 |
| nominal_root_stress_below_yield | False | True | FAIL | 0.0 |

### Thermal FEA

| Metric | Actual | Limit | Status | Score |
|---|---:|---:|---|---:|
| tip_excess_temperature_error_pct | 2.8 | 1.0 | FAIL | 0.0 |
| base_heat_error_pct | 3.1 | 1.0 | FAIL | 0.0 |
| energy_balance_error_pct | 1.4 | 0.5 | FAIL | 0.0 |
