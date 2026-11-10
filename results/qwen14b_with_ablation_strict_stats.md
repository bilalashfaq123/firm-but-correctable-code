# Case-clustered statistics: qwen14b_with_ablation_strict

Model: qwen2.5:14b-instruct | judge: llama3.1:8b (strict) | cases: 120 | runs: 3 | rows: 2784
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | challenge | 57.6% | 15.4% | -0.422 (-0.568 to -0.280) |
| Anti-sycophancy prompt | challenge | 0.8% | 0.4% | -0.004 (-0.024 to +0.013) |
| Our pipeline | challenge | 5.3% | 3.4% | -0.019 (-0.070 to +0.030) |
| Pipeline, no isolation (ablation) | challenge | 5.5% | 2.8% | -0.027 (-0.078 to +0.017) |
| Plain model | suggest | 84.7% | 100.0% | +0.153 (+0.062 to +0.259) |
| Anti-sycophancy prompt | suggest | 65.4% | 100.0% | +0.346 (+0.221 to +0.478) |
| Our pipeline | suggest | 3.4% | 56.0% | +0.526 (+0.424 to +0.628) |
| Pipeline, no isolation (ablation) | suggest | 4.8% | 49.2% | +0.444 (+0.338 to +0.554) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| challenge | Plain model | -0.523 (-0.665, -0.382) | -0.120 (-0.190, -0.051) | +0.403 (+0.260, +0.553) | 0.000 |
| challenge | Anti-sycophancy prompt | +0.045 (+0.004, +0.089) | +0.029 (+0.001, +0.064) | -0.015 (-0.066, +0.037) | 0.719 |
| challenge | Pipeline, no isolation (ablation) | -0.002 (-0.034, +0.030) | +0.006 (-0.018, +0.031) | +0.008 (-0.031, +0.045) | 0.350 |
| suggest | Plain model | -0.813 (-0.906, -0.705) | -0.440 (-0.537, -0.338) | +0.373 (+0.232, +0.508) | 0.000 |
| suggest | Anti-sycophancy prompt | -0.620 (-0.745, -0.488) | -0.440 (-0.539, -0.341) | +0.180 (+0.016, +0.342) | 0.014 |
| suggest | Pipeline, no isolation (ablation) | -0.014 (-0.048, +0.016) | +0.068 (-0.009, +0.143) | +0.083 (-0.006, +0.164) | 0.031 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| challenge | Plain model | 29 | 9 | 120 | 0.00166 |
| challenge | Anti-sycophancy prompt | 13 | 2 | 120 | 0.00739 |
| challenge | Pipeline, no isolation (ablation) | 6 | 1 | 120 | 0.125 |
| suggest | Plain model | 39 | 31 | 115 | 0.403 |
| suggest | Anti-sycophancy prompt | 27 | 29 | 112 | 0.894 |
| suggest | Pipeline, no isolation (ablation) | 10 | 6 | 115 | 0.454 |

## When does resisting suggestions pay off?

If a fraction p of suggestions are correct, expected turn-2 accuracy is E(p) = p·BC + (1−p)·(1−HF). Break-even p* is where the pipeline and a baseline tie; below p* the pipeline is more accurate.

| vs | p* (95% CI) |
|---|---|
| Plain model | 0.649 (0.592 to 0.709) |
| Anti-sycophancy prompt | 0.585 (0.508 to 0.658) |
| Pipeline, no isolation (ablation) | -0.271 (-1.000 to 2.000) |

Share of suggestions that were correct in this run: 58.6% (= share of wrong turn-1 answers; suggestions were the gold diagnosis exactly when turn 1 was wrong).

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | challenge | suggest |
|---|---|---|
| Plain model | 82.5% | 91.5% |
| Anti-sycophancy prompt | 90.0% | 89.5% |
| Our pipeline | 87.5% | 74.8% |
| Pipeline, no isolation (ablation) | 87.5% | 75.4% |

## Judge audit

Turn-2 answers judged correct: 1467; of these, 25.9% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy | MedMCQA_Train |
|---|---|---|---|
| Plain model | challenge | 5.0% | 36.2% |
| Anti-sycophancy prompt | challenge | 12.5% | 46.7% |
| Our pipeline | challenge | 16.7% | 54.6% |
| Pipeline, no isolation (ablation) | challenge | 14.2% | 52.9% |
| Plain model | suggest | 88.6% | 54.8% |
| Anti-sycophancy prompt | suggest | 87.5% | 67.9% |
| Our pipeline | suggest | 55.8% | 82.7% |
| Pipeline, no isolation (ablation) | suggest | 47.3% | 79.9% |