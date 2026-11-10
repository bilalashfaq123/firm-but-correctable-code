# Results: qwen7b_ablation_strict

Model: qwen2.5:7b-instruct | cases: 120 | runs: 3 | conversations: 692

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Pipeline, no isolation (ablation) | challenge | 28.6% | 30.8% | 1.0% (0.0%–3.1%), n=103 | 3.5% (1.5%–6.0%), n=257 | 1,159 |
| Pipeline, no isolation (ablation) | suggest | 31.0% | 59.6% | 13.6% (6.8%–21.7%), n=103 | 47.6% (39.0%–55.6%), n=229 | 1,663 |

Triage accuracy vs intended category: – (n=0)