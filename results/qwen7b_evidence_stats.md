# Case-clustered statistics: qwen7b_evidence

Model: qwen2.5:7b-instruct | judge: llama3.1:8b | cases: 29 | runs: 3 | rows: 261
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | evidence | 0.0% | 0.0% | +0.000 (+0.000 to +0.000) |
| Anti-sycophancy prompt | evidence | 0.0% | 2.6% | +0.026 (+0.000 to +0.064) |
| Our pipeline | evidence | 30.8% | 0.0% | -0.308 (-0.750 to +0.000) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| evidence | Plain model | +0.308 (+0.000, +0.750) | +0.000 (+0.000, +0.000) | -0.308 (-0.750, +0.000) | 0.994 |
| evidence | Anti-sycophancy prompt | +0.308 (+0.000, +0.750) | -0.026 (-0.064, +0.000) | -0.333 (-0.777, -0.027) | 0.962 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| evidence | Plain model | 0 | 1 | 29 | 1 |
| evidence | Anti-sycophancy prompt | 1 | 1 | 29 | 1 |

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | evidence |
|---|---|
| Plain model | 93.1% |
| Anti-sycophancy prompt | 93.1% |
| Our pipeline | 93.1% |

## Judge audit

Turn-2 answers judged correct: 32; of these, 46.9% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy |
|---|---|---|
| Plain model | evidence | 13.8% |
| Anti-sycophancy prompt | evidence | 12.6% |
| Our pipeline | evidence | 10.3% |