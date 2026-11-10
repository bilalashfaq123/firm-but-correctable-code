# Results: qwen7b_strict

Model: qwen2.5:7b-instruct | cases: 120 | runs: 3 | conversations: 2070

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | challenge | 30.0% | 18.3% | 47.2% (33.0%–61.2%), n=108 | 3.6% (1.6%–6.1%), n=252 | 600 |
| Plain model | suggest | 33.0% | 67.3% | 94.4% (85.8%–100.0%), n=108 | 97.7% (94.4%–100.0%), n=219 | 613 |
| Anti-sycophancy prompt | challenge | 28.9% | 30.3% | 1.9% (0.0%–5.0%), n=104 | 2.7% (0.8%–5.2%), n=256 | 671 |
| Anti-sycophancy prompt | suggest | 31.2% | 78.4% | 59.6% (44.8%–74.3%), n=104 | 95.6% (91.5%–98.7%), n=229 | 687 |
| Our pipeline | challenge | 30.3% | 30.3% | 6.4% (1.8%–12.3%), n=109 | 2.8% (0.8%–5.6%), n=251 | 1,143 |
| Our pipeline | suggest | 33.0% | 54.8% | 7.3% (2.8%–12.7%), n=109 | 36.2% (27.8%–44.9%), n=221 | 1,644 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | challenge | 56 | 13 | 360 | 1.68e-07 |
| pipeline vs plain | suggest | 89 | 125 | 313 | 0.0165 |
| pipeline vs plain | all | 145 | 138 | 673 | 0.721 |
| pipeline vs antisyc | challenge | 19 | 19 | 360 | 1 |
| pipeline vs antisyc | suggest | 56 | 129 | 316 | 8.24e-08 |
| pipeline vs antisyc | all | 75 | 148 | 676 | 1.16e-06 |

Triage accuracy vs intended category: 99.6% (n=690)