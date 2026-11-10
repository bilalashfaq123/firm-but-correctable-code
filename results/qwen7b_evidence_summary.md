# Results: qwen7b_evidence

Model: qwen2.5:7b-instruct | cases: 29 | runs: 3 | conversations: 261

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | evidence | 13.8% | 13.8% | 0.0% (0.0%–0.0%), n=12 | 0.0% (0.0%–0.0%), n=75 | 947 |
| Anti-sycophancy prompt | evidence | 10.3% | 12.6% | 0.0% (0.0%–0.0%), n=9 | 2.6% (0.0%–6.4%), n=78 | 1,032 |
| Our pipeline | evidence | 14.9% | 10.3% | 30.8% (6.2%–70.0%), n=13 | 0.0% (0.0%–0.0%), n=74 | 2,550 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | evidence | 2 | 5 | 87 | 0.453 |
| pipeline vs antisyc | evidence | 3 | 5 | 87 | 0.727 |

Triage accuracy vs intended category: 98.9% (n=87)