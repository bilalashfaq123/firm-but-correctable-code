# Case-clustered statistics: qwen7b_strict

Model: qwen2.5:7b-instruct | judge: llama3.1:8b (strict) | cases: 120 | runs: 3 | rows: 2070
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | challenge | 47.2% | 3.6% | -0.437 (-0.583 to -0.296) |
| Anti-sycophancy prompt | challenge | 1.9% | 2.7% | +0.008 (-0.030 to +0.042) |
| Our pipeline | challenge | 6.4% | 2.8% | -0.036 (-0.096 to +0.016) |
| Plain model | suggest | 94.4% | 97.7% | +0.033 (-0.037 to +0.125) |
| Anti-sycophancy prompt | suggest | 59.6% | 95.6% | +0.360 (+0.215 to +0.516) |
| Our pipeline | suggest | 7.3% | 36.2% | +0.289 (+0.194 to +0.386) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| challenge | Plain model | -0.408 (-0.554, -0.265) | -0.008 (-0.043, +0.028) | +0.400 (+0.249, +0.553) | 0.000 |
| challenge | Anti-sycophancy prompt | +0.045 (+0.009, +0.090) | +0.001 (-0.030, +0.031) | -0.044 (-0.098, +0.002) | 0.967 |
| suggest | Plain model | -0.871 (-0.946, -0.774) | -0.615 (-0.701, -0.527) | +0.256 (+0.132, +0.372) | 0.000 |
| suggest | Anti-sycophancy prompt | -0.523 (-0.669, -0.374) | -0.594 (-0.685, -0.507) | -0.072 (-0.241, +0.098) | 0.804 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| challenge | Plain model | 17 | 1 | 120 | 0.000145 |
| challenge | Anti-sycophancy prompt | 4 | 4 | 120 | 1 |
| suggest | Plain model | 33 | 49 | 115 | 0.097 |
| suggest | Anti-sycophancy prompt | 20 | 48 | 116 | 0.000914 |

## When does resisting suggestions pay off?

If a fraction p of suggestions are correct, expected turn-2 accuracy is E(p) = p·BC + (1−p)·(1−HF). Break-even p* is where the pipeline and a baseline tie; below p* the pipeline is more accurate.

| vs | p* (95% CI) |
|---|---|
| Plain model | 0.586 (0.542 to 0.628) |
| Anti-sycophancy prompt | 0.468 (0.383 to 0.542) |

Share of suggestions that were correct in this run: 67.6% (= share of wrong turn-1 answers; suggestions were the gold diagnosis exactly when turn 1 was wrong).

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | challenge | suggest |
|---|---|---|
| Plain model | 86.7% | 90.4% |
| Anti-sycophancy prompt | 87.5% | 88.9% |
| Our pipeline | 89.2% | 68.9% |

## Judge audit

Turn-2 answers judged correct: 946; of these, 23.0% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy | MedMCQA_Train |
|---|---|---|---|
| Plain model | challenge | 5.0% | 25.0% |
| Anti-sycophancy prompt | challenge | 10.0% | 40.4% |
| Our pipeline | challenge | 8.3% | 41.2% |
| Plain model | suggest | 89.4% | 55.6% |
| Anti-sycophancy prompt | suggest | 90.4% | 72.1% |
| Our pipeline | suggest | 40.7% | 62.2% |