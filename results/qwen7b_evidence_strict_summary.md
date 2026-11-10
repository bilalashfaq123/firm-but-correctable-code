# Results: qwen7b_evidence_strict

Model: qwen2.5:7b-instruct | cases: 29 | runs: 3 | conversations: 261

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | evidence | 11.5% | 11.5% | 0.0% (0.0%–0.0%), n=10 | 0.0% (0.0%–0.0%), n=77 | 947 |
| Anti-sycophancy prompt | evidence | 9.2% | 11.5% | 0.0% (0.0%–0.0%), n=8 | 2.5% (0.0%–6.7%), n=79 | 1,032 |
| Our pipeline | evidence | 12.6% | 9.2% | 27.3% (0.0%–60.1%), n=11 | 0.0% (0.0%–0.0%), n=76 | 2,550 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | evidence | 3 | 5 | 87 | 0.727 |
| pipeline vs antisyc | evidence | 3 | 5 | 87 | 0.727 |

Triage accuracy vs intended category: 98.9% (n=87)