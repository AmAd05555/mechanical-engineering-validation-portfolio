# ANSYS Steady-State Thermal Replication Guide

## Geometry
Import `01_CAD/Aluminum_Cooling_Fin.step`.

Dimensions:
- 200 mm length
- 30 mm width
- 4 mm thickness

## Material
Use aluminum with thermal conductivity **205 W/m·K**. Density and specific heat are not required for steady-state, but values 2700 kg/m³ and 900 J/kg·K are included for completeness.

## Boundary conditions
1. Base face at x=0: **Temperature = 100 °C**.
2. Four long faces: **Convection h = 15 W/m²·K, ambient = 25 °C**.
3. Tip face at x=200 mm: **Convection h = 15 W/m²·K, ambient = 25 °C**.
4. Do NOT apply convection to the fixed-temperature base face.

## Mesh
Run at least three meshes. Suggested global element sizes:
- Coarse: 20 mm
- Medium: 10 mm
- Fine: 5 mm or finer

Because the cross-section Biot number is very small (0.000146), the temperature should be nearly uniform through each cross-section.

## Results to request
- Temperature distribution
- Total heat flux
- Directional heat flux in X
- Reaction heat flow at the 100 °C base

## Ground-truth targets
- Tip temperature ≈ **63.0819 °C**
- Base heat input ≈ **10.23513 W**

A good 3D ANSYS model should approach these results as the mesh is refined. Small differences are expected because the analytic model assumes a uniform cross-sectional temperature.
