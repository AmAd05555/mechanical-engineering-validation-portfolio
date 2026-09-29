# StoryGold-Relevant Capability Mapping

| Job-relevant capability | Evidence in this project |
|---|---|
| Automated scoring scripts | Python evaluator calculates weighted domain and overall scores |
| Deterministic validation checks | Explicit thresholds; same input gives same output |
| CAD evaluation | Parses parametric CAD validation checks across configurations |
| Static stress / FEA evaluation | Checks deflection, stress, force and moment balance, yield |
| Thermal analysis evaluation | Checks analytical temperature, heat flow and energy balance |
| Ground-truth benchmarks | Uses outputs from validated analytical-vs-FEA benchmark projects |
| Failure diagnosis | Reports failed metric, actual value and allowable limit |
| Evaluation infrastructure | Configurable rules, CLI, JSON/CSV/Markdown outputs, tests |
| Reward-metric foundation | Weighted score can serve as a deterministic benchmark signal |
