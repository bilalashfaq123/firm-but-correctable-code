# Results: qwen14b_evidence

Model: qwen2.5:14b-instruct | cases: 29 | runs: 3 | conversations: 261

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | evidence | 9.2% | 12.6% | 12.5% (0.0%–50.0%), n=8 | 5.1% (0.0%–12.7%), n=79 | 972 |
| Anti-sycophancy prompt | evidence | 6.9% | 13.8% | 0.0% (0.0%–0.0%), n=6 | 7.4% (2.5%–13.6%), n=81 | 1,073 |
| Our pipeline | evidence | 11.5% | 18.4% | 0.0% (0.0%–0.0%), n=10 | 7.8% (2.6%–13.8%), n=77 | 2,647 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | evidence | 9 | 4 | 87 | 0.267 |
| pipeline vs antisyc | evidence | 5 | 1 | 87 | 0.219 |

Triage accuracy vs intended category: 100.0% (n=87)