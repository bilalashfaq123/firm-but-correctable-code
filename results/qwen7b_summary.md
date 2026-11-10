# Results: qwen7b

Model: qwen2.5:7b-instruct | cases: 120 | runs: 3 | conversations: 2160

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | challenge | 39.2% | 24.4% | 44.7% (33.3%–56.9%), n=141 | 4.6% (2.2%–7.5%), n=219 | 600 |
| Plain model | suggest | 39.2% | 63.9% | 92.2% (84.5%–98.5%), n=141 | 100.0% (100.0%–100.0%), n=219 | 609 |
| Anti-sycophancy prompt | challenge | 36.4% | 38.6% | 0.0% (0.0%–0.0%), n=131 | 3.5% (0.9%–7.0%), n=229 | 671 |
| Anti-sycophancy prompt | suggest | 36.4% | 75.6% | 64.1% (50.8%–76.4%), n=131 | 98.3% (96.0%–100.0%), n=229 | 685 |
| Our pipeline | challenge | 38.6% | 38.9% | 2.9% (0.7%–6.0%), n=139 | 2.3% (0.5%–4.3%), n=221 | 1,143 |
| Our pipeline | suggest | 38.6% | 58.3% | 6.5% (2.9%–11.2%), n=139 | 36.2% (27.6%–44.9%), n=221 | 1,633 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | challenge | 69 | 17 | 360 | 1.35e-08 |
| pipeline vs plain | suggest | 110 | 130 | 360 | 0.22 |
| pipeline vs plain | all | 179 | 147 | 720 | 0.0858 |
| pipeline vs antisyc | challenge | 26 | 25 | 360 | 1 |
| pipeline vs antisyc | suggest | 73 | 135 | 360 | 2.05e-05 |
| pipeline vs antisyc | all | 99 | 160 | 720 | 0.000181 |

Triage accuracy vs intended category: 99.6% (n=720)