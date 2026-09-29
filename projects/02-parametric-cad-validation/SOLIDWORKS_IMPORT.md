# SolidWorks import / continuation

1. Open each `.step` file directly in SolidWorks.
2. Use **File > Save As** to save imported parts as `.SLDPRT` and assemblies as `.SLDASM`.
3. STEP preserves the exact solid geometry but not the original CadQuery feature history.
4. For a native SolidWorks feature tree, rebuild the BasePlate and SliderPlate using the parameter table in `README.md`; use the STEP bodies as geometric references/checks.
5. The source of truth for parametric behavior is `05_Source/parametric_motor_mount.py`.
6. Compare rebuilt SolidWorks geometry against the STEP files using **Evaluate > Compare Geometry** where available.
