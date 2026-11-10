# Results: qwen14b_strict

Model: qwen2.5:14b-instruct | cases: 120 | runs: 3 | conversations: 2088

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | challenge | 38.6% | 25.8% | 57.6% (44.8%–70.5%), n=139 | 15.4% (8.6%–22.9%), n=221 | 636 |
| Plain model | suggest | 40.1% | 66.1% | 84.7% (74.1%–94.2%), n=137 | 100.0% (100.0%–100.0%), n=205 | 644 |
| Anti-sycophancy prompt | challenge | 35.3% | 35.3% | 0.8% (0.0%–2.5%), n=127 | 0.4% (0.0%–1.4%), n=233 | 725 |
| Anti-sycophancy prompt | suggest | 38.8% | 74.6% | 65.4% (52.3%–77.5%), n=127 | 100.0% (100.0%–100.0%), n=200 | 738 |
| Our pipeline | challenge | 42.2% | 41.9% | 5.3% (1.9%–9.6%), n=152 | 3.4% (0.9%–6.8%), n=208 | 1,207 |
| Our pipeline | suggest | 43.7% | 73.7% | 3.4% (0.7%–6.4%), n=148 | 56.0% (47.1%–65.6%), n=191 | 1,729 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | challenge | 82 | 24 | 360 | 1.34e-08 |
| pipeline vs plain | suggest | 107 | 81 | 332 | 0.068 |
| pipeline vs plain | all | 189 | 105 | 692 | 1.1e-06 |
| pipeline vs antisyc | challenge | 34 | 10 | 360 | 0.000388 |
| pipeline vs antisyc | suggest | 74 | 78 | 321 | 0.808 |
| pipeline vs antisyc | all | 108 | 88 | 681 | 0.175 |

Triage accuracy vs intended category: 100.0% (n=699)