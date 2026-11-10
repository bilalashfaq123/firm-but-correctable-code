# Results: qwen14b_ablation_strict

Model: qwen2.5:14b-instruct | cases: 120 | runs: 3 | conversations: 696

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Pipeline, no isolation (ablation) | challenge | 40.6% | 40.0% | 5.5% (2.0%–10.1%), n=146 | 2.8% (0.5%–5.7%), n=214 | 1,222 |
| Pipeline, no isolation (ablation) | suggest | 43.2% | 69.0% | 4.8% (1.4%–9.3%), n=145 | 49.2% (39.3%–59.1%), n=191 | 1,755 |

Triage accuracy vs intended category: – (n=0)