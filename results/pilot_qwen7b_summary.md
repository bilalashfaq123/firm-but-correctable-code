# Results: pilot_qwen7b

Model: qwen2.5:7b-instruct | cases: 10 | runs: 1 | conversations: 60

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | challenge | 30.0% | 20.0% | 33.3% (0.0%–100.0%), n=3 | 0.0% (0.0%–0.0%), n=7 | 618 |
| Plain model | suggest | 30.0% | 70.0% | 100.0% (100.0%–100.0%), n=3 | 100.0% (100.0%–100.0%), n=7 | 635 |
| Anti-sycophancy prompt | challenge | 30.0% | 30.0% | 0.0% (0.0%–0.0%), n=3 | 0.0% (0.0%–0.0%), n=7 | 700 |
| Anti-sycophancy prompt | suggest | 30.0% | 80.0% | 66.7% (0.0%–100.0%), n=3 | 100.0% (100.0%–100.0%), n=7 | 711 |
| Our pipeline | challenge | 30.0% | 30.0% | 0.0% (0.0%–0.0%), n=3 | 0.0% (0.0%–0.0%), n=7 | 1,151 |
| Our pipeline | suggest | 30.0% | 60.0% | 0.0% (0.0%–0.0%), n=3 | 42.9% (14.3%–85.7%), n=7 | 1,671 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | challenge | 1 | 0 | 10 | 1 |
| pipeline vs plain | suggest | 3 | 4 | 10 | 1 |
| pipeline vs plain | all | 4 | 4 | 20 | 1 |
| pipeline vs antisyc | challenge | 0 | 0 | 10 | nan |
| pipeline vs antisyc | suggest | 2 | 4 | 10 | 0.688 |
| pipeline vs antisyc | all | 2 | 4 | 20 | 0.688 |

Triage accuracy vs intended category: 100.0% (n=20)