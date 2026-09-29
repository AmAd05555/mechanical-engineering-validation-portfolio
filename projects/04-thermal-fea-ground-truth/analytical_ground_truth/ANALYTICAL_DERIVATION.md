# Analytical Ground Truth — Convective Rectangular Fin

## Problem
A rectangular aluminum fin loses heat by convection from its long surfaces and its tip.

- Length, L = 200 mm
- Width, b = 30 mm
- Thickness, t = 4 mm
- Cross-sectional area, A = 0.000120 m²
- Wetted perimeter, P = 0.068 m
- Thermal conductivity, k = 205.0 W/m·K
- Convection coefficient, h = 15.0 W/m²·K
- Base temperature, Tb = 100.0 °C
- Ambient temperature, T∞ = 25.0 °C

## Governing equation
For a straight fin of uniform cross-section:

`d²θ/dx² - m²θ = 0`, where `θ = T - T∞` and `m = sqrt(hP/(kA))`.

For a convective tip, the exact temperature distribution is:

`θ(x)/θb = [cosh(m(L-x)) + (h/(mk))sinh(m(L-x))] / [cosh(mL) + (h/(mk))sinh(mL)]`

## Calculated values
- m = 6.439209 1/m
- mL = 1.287842
- h/(mk) = 0.011363
- Tip temperature = **63.0819 °C**
- Base heat flow = **10.23513 W**
- Thickness-based Biot number = **0.000146** (small, supporting the 1D assumption)
