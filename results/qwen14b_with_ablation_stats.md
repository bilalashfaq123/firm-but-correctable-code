# Case-clustered statistics: qwen14b_with_ablation

Model: qwen2.5:14b-instruct | judge: llama3.1-cpu | cases: 120 | runs: 3 | rows: 2880
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | challenge | 58.2% | 21.7% | -0.364 (-0.519 to -0.212) |
| Anti-sycophancy prompt | challenge | 1.9% | 1.5% | -0.004 (-0.034 to +0.028) |
| Our pipeline | challenge | 1.2% | 6.2% | +0.049 (+0.005 to +0.100) |
| Pipeline, no isolation (ablation) | challenge | 3.0% | 2.1% | -0.009 (-0.038 to +0.019) |
| Plain model | suggest | 83.0% | 100.0% | +0.170 (+0.079 to +0.271) |
| Anti-sycophancy prompt | suggest | 65.6% | 100.0% | +0.344 (+0.233 to +0.455) |
| Our pipeline | suggest | 3.0% | 57.9% | +0.549 (+0.449 to +0.649) |
| Pipeline, no isolation (ablation) | suggest | 4.2% | 49.5% | +0.453 (+0.342 to +0.559) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| challenge | Plain model | -0.570 (-0.693, -0.445) | -0.156 (-0.244, -0.064) | +0.414 (+0.267, +0.563) | 0.000 |
| challenge | Anti-sycophancy prompt | -0.007 (-0.029, +0.013) | +0.047 (+0.001, +0.097) | +0.053 (-0.001, +0.115) | 0.029 |
| challenge | Pipeline, no isolation (ablation) | -0.018 (-0.045, +0.007) | +0.041 (+0.005, +0.083) | +0.058 (+0.010, +0.110) | 0.009 |
| suggest | Plain model | -0.800 (-0.899, -0.685) | -0.421 (-0.516, -0.328) | +0.379 (+0.236, +0.518) | 0.000 |
| suggest | Anti-sycophancy prompt | -0.626 (-0.741, -0.507) | -0.421 (-0.518, -0.325) | +0.205 (+0.055, +0.354) | 0.004 |
| suggest | Pipeline, no isolation (ablation) | -0.011 (-0.045, +0.020) | +0.085 (+0.008, +0.163) | +0.096 (+0.011, +0.183) | 0.014 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| challenge | Plain model | 33 | 12 | 120 | 0.00246 |
| challenge | Anti-sycophancy prompt | 9 | 2 | 120 | 0.0654 |
| challenge | Pipeline, no isolation (ablation) | 3 | 2 | 120 | 1 |
| suggest | Plain model | 42 | 29 | 120 | 0.154 |
| suggest | Anti-sycophancy prompt | 32 | 29 | 120 | 0.798 |
| suggest | Pipeline, no isolation (ablation) | 9 | 6 | 120 | 0.607 |

## When does resisting suggestions pay off?

If a fraction p of suggestions are correct, expected turn-2 accuracy is E(p) = p·BC + (1−p)·(1−HF). Break-even p* is where the pipeline and a baseline tie; below p* the pipeline is more accurate.

| vs | p* (95% CI) |
|---|---|
| Plain model | 0.655 (0.594 to 0.717) |
| Anti-sycophancy prompt | 0.598 (0.524 to 0.667) |
| Pipeline, no isolation (ablation) | -0.155 (-1.000 to 1.187) |

Share of suggestions that were correct in this run: 55.1% (= share of wrong turn-1 answers; suggestions were the gold diagnosis exactly when turn 1 was wrong).

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | challenge | suggest |
|---|---|---|
| Plain model | 83.3% | 84.2% |
| Anti-sycophancy prompt | 89.2% | 84.2% |
| Our pipeline | 87.5% | 76.7% |
| Pipeline, no isolation (ablation) | 86.7% | 75.0% |

## Judge audit

Turn-2 answers judged correct: 1628; of these, 31.6% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy | MedMCQA_Train |
|---|---|---|---|
| Plain model | challenge | 8.3% | 41.2% |
| Anti-sycophancy prompt | challenge | 20.0% | 56.7% |
| Our pipeline | challenge | 22.5% | 61.7% |
| Pipeline, no isolation (ablation) | challenge | 20.0% | 59.6% |
| Plain model | suggest | 84.2% | 55.0% |
| Anti-sycophancy prompt | suggest | 81.7% | 65.4% |
| Our pipeline | suggest | 59.2% | 84.2% |
| Pipeline, no isolation (ablation) | suggest | 50.8% | 81.2% |