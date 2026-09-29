# Adjustable Motor Mount — Parametric CAD Validation Benchmark

## Purpose
A real, generated CAD project built to demonstrate parametric mechanical design, configuration testing, deterministic geometry checks, motion-range reasoning, and CAD debugging practice. It maps closely to CAD-evaluation work involving geometry validity, constraints/parameters, rebuild robustness, and automated checks.

## Deliverables
- STEP solids for all parts
- STEP assemblies for Compact / Standard / Extended configurations
- STEP assemblies for left / centered / right travel states
- Exploded assembly STEP
- STL meshes for quick viewing
- DXF top views for BasePlate and SliderPlate
- Parametric CadQuery source
- Automated validation report (CSV + JSON)
- Five deliberately invalid parameter cases for debugging practice
- SolidWorks import/rebuild instructions

## Standard configuration
- Base plate: 220 x 140 x 8 mm
- Base slots: 90 x 12 mm, Y offsets ±45 mm
- Slider plate: 130 x 110 x 10 mm
- Motor mounting pattern: 70 x 50 mm, Ø8.5 mm
- Guide holes: Ø10.5 mm
- Guide pins: Ø10 mm
- Requested travel: ±40 mm
- Base chassis holes: Ø9 mm

## Configurations
### Compact
Base 190 x 120; Slider 110 x 90; slots 70; slot offset 35; travel ±28.

### Standard
Base 220 x 140; Slider 130 x 110; slots 90; slot offset 45; travel ±40.

### Extended
Base 260 x 160; Slider 150 x 120; slots 120; slot offset 50; travel ±52.

## Deterministic validation rules
1. Slot width must exceed guide-pin diameter.
2. Guide hole must exceed guide-pin diameter.
3. Slider must remain inside the base footprint.
4. Requested travel must fit the slot geometry.
5. Motor-hole pattern must remain inside slider boundaries.
6. Base and slider solids must rebuild to positive volume.

## Debug cases
- Debug01: slot narrower than guide pin
- Debug02: requested travel exceeds geometric range
- Debug03: slider wider than base
- Debug04: motor-hole pattern outside slider boundary
- Debug05: guide-hole interference with guide pin

These cases are intentionally invalid and are caught by the validator.

## Suggested portfolio statement after reviewing and understanding the project
Designed and validated a parametric adjustable motor-mount benchmark with multiple dimensional configurations, controlled slider travel, and deterministic geometry checks; investigated invalid parameter states including clearance, travel, envelope, and hole-pattern failures.

## Important
The native parametric source in this package is CadQuery, which is one of the parametric CAD tools listed in StoryGold's CAD Evaluation Engineer requirements. STEP files open directly in SolidWorks, but STEP does not preserve a native SolidWorks feature tree.
