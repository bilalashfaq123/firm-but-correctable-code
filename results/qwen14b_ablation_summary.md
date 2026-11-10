# Results: qwen14b_ablation

Model: qwen2.5:14b-instruct | cases: 120 | runs: 3 | conversations: 720

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Pipeline, no isolation (ablation) | challenge | 46.7% | 46.4% | 3.0% (0.6%–5.7%), n=168 | 2.1% (0.5%–4.4%), n=192 | 1,222 |
| Pipeline, no isolation (ablation) | suggest | 46.7% | 71.1% | 4.2% (1.2%–8.0%), n=168 | 49.5% (39.6%–59.8%), n=192 | 1,750 |

Triage accuracy vs intended category: – (n=0)