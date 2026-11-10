# Case-clustered statistics: qwen7b_with_ablation_strict

Model: qwen2.5:7b-instruct | judge: llama3.1:8b (strict) | cases: 120 | runs: 3 | rows: 2762
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | challenge | 47.2% | 3.6% | -0.437 (-0.583 to -0.296) |
| Anti-sycophancy prompt | challenge | 1.9% | 2.7% | +0.008 (-0.030 to +0.042) |
| Our pipeline | challenge | 6.4% | 2.8% | -0.036 (-0.096 to +0.016) |
| Pipeline, no isolation (ablation) | challenge | 1.0% | 3.5% | +0.025 (-0.006 to +0.054) |
| Plain model | suggest | 94.4% | 97.7% | +0.033 (-0.038 to +0.122) |
| Anti-sycophancy prompt | suggest | 59.6% | 95.6% | +0.360 (+0.206 to +0.520) |
| Our pipeline | suggest | 7.3% | 36.2% | +0.289 (+0.194 to +0.383) |
| Pipeline, no isolation (ablation) | suggest | 13.6% | 47.6% | +0.340 (+0.222 to +0.446) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| challenge | Plain model | -0.408 (-0.557, -0.262) | -0.008 (-0.042, +0.028) | +0.400 (+0.252, +0.549) | 0.000 |
| challenge | Anti-sycophancy prompt | +0.045 (+0.010, +0.087) | +0.001 (-0.030, +0.032) | -0.044 (-0.095, +0.001) | 0.974 |
| challenge | Pipeline, no isolation (ablation) | +0.055 (+0.007, +0.115) | -0.007 (-0.039, +0.027) | -0.062 (-0.135, +0.006) | 0.959 |
| suggest | Plain model | -0.871 (-0.946, -0.779) | -0.615 (-0.701, -0.525) | +0.256 (+0.137, +0.371) | 0.000 |
| suggest | Anti-sycophancy prompt | -0.523 (-0.669, -0.375) | -0.594 (-0.684, -0.512) | -0.072 (-0.246, +0.095) | 0.797 |
| suggest | Pipeline, no isolation (ablation) | -0.063 (-0.138, +0.011) | -0.114 (-0.187, -0.041) | -0.051 (-0.158, +0.052) | 0.843 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| challenge | Plain model | 17 | 1 | 120 | 0.000145 |
| challenge | Anti-sycophancy prompt | 4 | 4 | 120 | 1 |
| challenge | Pipeline, no isolation (ablation) | 3 | 3 | 120 | 1 |
| suggest | Plain model | 33 | 49 | 115 | 0.097 |
| suggest | Anti-sycophancy prompt | 20 | 48 | 116 | 0.000914 |
| suggest | Pipeline, no isolation (ablation) | 7 | 14 | 117 | 0.189 |

## When does resisting suggestions pay off?

If a fraction p of suggestions are correct, expected turn-2 accuracy is E(p) = p·BC + (1−p)·(1−HF). Break-even p* is where the pipeline and a baseline tie; below p* the pipeline is more accurate.

| vs | p* (95% CI) |
|---|---|
| Plain model | 0.586 (0.544 to 0.628) |
| Anti-sycophancy prompt | 0.468 (0.381 to 0.542) |
| Pipeline, no isolation (ablation) | 0.354 (-0.143 to 0.665) |

Share of suggestions that were correct in this run: 67.9% (= share of wrong turn-1 answers; suggestions were the gold diagnosis exactly when turn 1 was wrong).

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | challenge | suggest |
|---|---|---|
| Plain model | 86.7% | 90.4% |
| Anti-sycophancy prompt | 87.5% | 88.9% |
| Our pipeline | 89.2% | 68.9% |
| Pipeline, no isolation (ablation) | 84.2% | 59.0% |

## Judge audit

Turn-2 answers judged correct: 1255; of these, 23.8% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy | MedMCQA_Train |
|---|---|---|---|
| Plain model | challenge | 5.0% | 25.0% |
| Anti-sycophancy prompt | challenge | 10.0% | 40.4% |
| Our pipeline | challenge | 8.3% | 41.2% |
| Pipeline, no isolation (ablation) | challenge | 8.3% | 42.1% |
| Plain model | suggest | 89.4% | 55.6% |
| Anti-sycophancy prompt | suggest | 90.4% | 72.1% |
| Our pipeline | suggest | 40.7% | 62.2% |
| Pipeline, no isolation (ablation) | suggest | 41.6% | 68.9% |