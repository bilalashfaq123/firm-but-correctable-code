# Case-clustered statistics: qwen14b_evidence

Model: qwen2.5:14b-instruct | judge: llama3.1-cpu | cases: 29 | runs: 3 | rows: 261
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | evidence | 12.5% | 5.1% | -0.074 (-0.929 to +0.103) |
| Anti-sycophancy prompt | evidence | 0.0% | 7.4% | +0.074 (+0.015 to +0.143) |
| Our pipeline | evidence | 0.0% | 7.8% | +0.078 (+0.027 to +0.138) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| evidence | Plain model | -0.125 (-1.000, +0.000) | +0.027 (-0.054, +0.101) | +0.152 (-0.045, +0.988) | 0.116 |
| evidence | Anti-sycophancy prompt | +0.000 (+0.000, +0.000) | +0.004 (-0.066, +0.069) | +0.004 (-0.066, +0.069) | 0.369 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| evidence | Plain model | 1 | 1 | 29 | 1 |
| evidence | Anti-sycophancy prompt | 1 | 0 | 29 | 1 |

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | evidence |
|---|---|
| Plain model | 89.7% |
| Anti-sycophancy prompt | 82.8% |
| Our pipeline | 72.4% |

## Judge audit

Turn-2 answers judged correct: 39; of these, 46.2% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy |
|---|---|---|
| Plain model | evidence | 12.6% |
| Anti-sycophancy prompt | evidence | 13.8% |
| Our pipeline | evidence | 18.4% |