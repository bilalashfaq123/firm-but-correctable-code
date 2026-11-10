# Case-clustered statistics: qwen14b_evidence_strict

Model: qwen2.5:14b-instruct | judge: llama3.1:8b (strict) | cases: 29 | runs: 3 | rows: 261
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | evidence | 0.0% | 3.7% | +0.037 (+0.000 to +0.099) |
| Anti-sycophancy prompt | evidence | 0.0% | 4.9% | +0.049 (+0.000 to +0.111) |
| Our pipeline | evidence | 0.0% | 5.1% | +0.051 (+0.000 to +0.120) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| evidence | Plain model | +0.000 (+0.000, +0.000) | +0.014 (-0.068, +0.096) | +0.014 (-0.068, +0.096) | 0.290 |
| evidence | Anti-sycophancy prompt | +0.000 (+0.000, +0.000) | +0.002 (-0.083, +0.087) | +0.002 (-0.083, +0.088) | 0.409 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| evidence | Plain model | 1 | 0 | 29 | 1 |
| evidence | Anti-sycophancy prompt | 1 | 0 | 29 | 1 |

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | evidence |
|---|---|
| Plain model | 93.1% |
| Anti-sycophancy prompt | 89.7% |
| Our pipeline | 82.8% |

## Judge audit

Turn-2 answers judged correct: 32; of these, 34.4% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy |
|---|---|---|
| Plain model | evidence | 10.3% |
| Anti-sycophancy prompt | evidence | 11.5% |
| Our pipeline | evidence | 14.9% |