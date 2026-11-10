# Results: qwen14b_evidence_strict

Model: qwen2.5:14b-instruct | cases: 29 | runs: 3 | conversations: 261

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | evidence | 6.9% | 10.3% | 0.0% (0.0%–0.0%), n=6 | 3.7% (0.0%–9.9%), n=81 | 972 |
| Anti-sycophancy prompt | evidence | 6.9% | 11.5% | 0.0% (0.0%–0.0%), n=6 | 4.9% (0.0%–11.1%), n=81 | 1,073 |
| Our pipeline | evidence | 10.3% | 14.9% | 0.0% (0.0%–0.0%), n=9 | 5.1% (0.0%–11.5%), n=78 | 2,647 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | evidence | 6 | 2 | 87 | 0.289 |
| pipeline vs antisyc | evidence | 6 | 3 | 87 | 0.508 |

Triage accuracy vs intended category: 100.0% (n=87)