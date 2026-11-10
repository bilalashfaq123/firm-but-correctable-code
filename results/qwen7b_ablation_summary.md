# Results: qwen7b_ablation

Model: qwen2.5:7b-instruct | cases: 120 | runs: 3 | conversations: 720

| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |
|---|---|---|---|---|---|---|
| Pipeline, no isolation (ablation) | challenge | 36.4% | 37.5% | 3.1% (0.0%–7.2%), n=131 | 3.5% (1.3%–6.5%), n=229 | 1,159 |
| Pipeline, no isolation (ablation) | suggest | 36.4% | 62.5% | 11.5% (6.6%–16.9%), n=131 | 47.6% (39.0%–55.9%), n=229 | 1,656 |

Triage accuracy vs intended category: – (n=0)