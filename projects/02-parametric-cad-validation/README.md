# Parametric CAD Validation Benchmark

A parametric adjustable motor-mount benchmark created to explore **configuration robustness, geometry validity, mechanical clearances and deterministic CAD checks**.

![Assembly](renders/Assembly_Isometric.png)

## Design
The model includes a base plate, slider plate, guide pins, bracket and reference motor envelope. Three configurations are provided:

| Configuration | Base | Slider | Slot | Travel |
|---|---|---|---|---|
| Compact | 190 × 120 mm | 110 × 90 mm | 70 mm | ±28 mm |
| Standard | 220 × 140 mm | 130 × 110 mm | 90 mm | ±40 mm |
| Extended | 260 × 160 mm | 150 × 120 mm | 120 mm | ±52 mm |

## Deterministic checks
The validator checks slot/pin clearance, guide-hole clearance, slider envelope, requested travel, motor-hole position and positive CAD solid volume.

Five intentionally invalid parameter sets are included under `debug_cases/` to demonstrate that the checks catch unacceptable configurations.

## Files
- `source/` — CadQuery parametric source and validation scripts
- `cad/` — STEP assemblies and main parts
- `dxf/` — 2D profiles
- `validation/` — CSV/JSON results
- `debug_cases/` — intentionally invalid configurations
- `renders/` — portfolio images

STEP files open in SolidWorks, but STEP does not preserve a native SolidWorks feature tree. See `SOLIDWORKS_IMPORT.md`.
