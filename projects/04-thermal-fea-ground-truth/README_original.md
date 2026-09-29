# StoryGold Project 03 — Thermal Analysis Ground-Truth Benchmark

This is a complete thermal-validation project built around a rectangular aluminum cooling fin.

## Core engineering question
Can a thermal simulation reproduce a known physical ground truth, remain stable under mesh refinement, and satisfy energy conservation?

## Problem definition
- Aluminum fin: 200 × 30 × 4 mm
- k = 205 W/m·K
- Heated base = 100 °C
- Ambient = 25 °C
- Convection coefficient = 15 W/m²·K
- Side and tip convection

## Validated headline results
- Analytical tip temperature: **63.0819 °C**
- Fine FE tip temperature: **63.0815 °C**
- Tip excess-temperature error: **0.0012%**
- Analytical base heat input: **10.23513 W**
- Fine FE base heat input: **10.23529 W**
- Base heat-flow error: **0.0015%**
- Energy-balance error: **0.000000%**

## Contents
`01_CAD` — STEP/STL geometry
`02_Analytical_Ground_Truth` — derivation and exact profile
`03_FEA_Solver` — finite-element source code
`04_Results` — convergence and nodal results
`05_Validation` — pass/fail validation report
`06_ANSYS_Replication` — exact ANSYS setup
`07_Portfolio` — case study and CV bullets
`08_Renders` — temperature and convergence figures
`09_Interview_Notes` — concepts and interview preparation

## Important
The included numerical FE model is a transparent 1D thermal finite-element benchmark. A separate guide explains how to replicate the same physics in ANSYS Steady-State Thermal using the provided 3D STEP geometry.
