# Results: qwen14b

Model: qwen2.5:14b-instruct | cases: 120 | runs: 3 | conversations: 2160

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Plain model | challenge | 42.5% | 30.3% | 58.2% (45.3%–71.2%), n=153 | 21.7% (13.4%–30.3%), n=207 | 636 |
| Plain model | suggest | 42.5% | 64.7% | 83.0% (73.4%–91.8%), n=153 | 100.0% (100.0%–100.0%), n=207 | 641 |
| Anti-sycophancy prompt | challenge | 44.4% | 44.4% | 1.9% (0.0%–4.4%), n=160 | 1.5% (0.0%–4.0%), n=200 | 725 |
| Anti-sycophancy prompt | suggest | 44.4% | 70.8% | 65.6% (54.1%–76.4%), n=160 | 100.0% (100.0%–100.0%), n=200 | 737 |
| Our pipeline | challenge | 45.8% | 48.6% | 1.2% (0.0%–3.1%), n=165 | 6.2% (2.5%–10.9%), n=195 | 1,207 |
| Our pipeline | suggest | 45.8% | 75.8% | 3.0% (0.6%–6.6%), n=165 | 57.9% (48.3%–67.5%), n=195 | 1,722 |

## Paired exact (McNemar) tests on turn-2 correctness

| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |
|---|---|---|---|---|---|
| pipeline vs plain | challenge | 99 | 33 | 360 | 7.5e-09 |
| pipeline vs plain | suggest | 122 | 82 | 360 | 0.00618 |
| pipeline vs plain | all | 221 | 115 | 720 | 7.69e-09 |
| pipeline vs antisyc | challenge | 28 | 13 | 360 | 0.0275 |
| pipeline vs antisyc | suggest | 97 | 79 | 360 | 0.2 |
| pipeline vs antisyc | all | 125 | 92 | 720 | 0.0296 |

Triage accuracy vs intended category: 100.0% (n=720)