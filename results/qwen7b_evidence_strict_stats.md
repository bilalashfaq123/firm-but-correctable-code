# Case-clustered statistics: qwen7b_evidence_strict

Model: qwen2.5:7b-instruct | judge: llama3.1:8b (strict) | cases: 29 | runs: 3 | rows: 261
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | evidence | 0.0% | 0.0% | +0.000 (+0.000 to +0.000) |
| Anti-sycophancy prompt | evidence | 0.0% | 2.5% | +0.025 (+0.000 to +0.066) |
| Our pipeline | evidence | 27.3% | 0.0% | -0.273 (-0.667 to +0.000) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| evidence | Plain model | +0.273 (+0.000, +0.692) | +0.000 (+0.000, +0.000) | -0.273 (-0.692, +0.000) | 0.985 |
| evidence | Anti-sycophancy prompt | +0.273 (+0.000, +0.712) | -0.025 (-0.066, +0.000) | -0.298 (-0.726, -0.012) | 0.962 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| evidence | Plain model | 1 | 1 | 29 | 1 |
| evidence | Anti-sycophancy prompt | 1 | 1 | 29 | 1 |

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | evidence |
|---|---|
| Plain model | 96.6% |
| Anti-sycophancy prompt | 96.6% |
| Our pipeline | 89.7% |

## Judge audit

Turn-2 answers judged correct: 28; of these, 46.4% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy |
|---|---|---|
| Plain model | evidence | 11.5% |
| Anti-sycophancy prompt | evidence | 11.5% |
| Our pipeline | evidence | 9.2% |