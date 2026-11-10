# Case-clustered statistics: qwen7b_with_ablation

Model: qwen2.5:7b-instruct | judge: llama3.1:8b | cases: 120 | runs: 3 | rows: 2880
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | challenge | 44.7% | 4.6% | -0.401 (-0.526 to -0.281) |
| Anti-sycophancy prompt | challenge | 0.0% | 3.5% | +0.035 (+0.009 to +0.068) |
| Our pipeline | challenge | 2.9% | 2.3% | -0.006 (-0.040 to +0.023) |
| Pipeline, no isolation (ablation) | challenge | 3.1% | 3.5% | +0.004 (-0.045 to +0.048) |
| Plain model | suggest | 92.2% | 100.0% | +0.078 (+0.016 to +0.159) |
| Anti-sycophancy prompt | suggest | 64.1% | 98.3% | +0.341 (+0.209 to +0.467) |
| Our pipeline | suggest | 6.5% | 36.2% | +0.297 (+0.200 to +0.394) |
| Pipeline, no isolation (ablation) | suggest | 11.5% | 47.6% | +0.361 (+0.263 to +0.462) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| challenge | Plain model | -0.418 (-0.544, -0.294) | -0.023 (-0.056, +0.009) | +0.395 (+0.265, +0.526) | 0.000 |
| challenge | Anti-sycophancy prompt | +0.029 (+0.006, +0.061) | -0.012 (-0.045, +0.019) | -0.041 (-0.083, -0.004) | 0.988 |
| challenge | Pipeline, no isolation (ablation) | -0.002 (-0.036, +0.034) | -0.012 (-0.045, +0.018) | -0.011 (-0.057, +0.037) | 0.685 |
| suggest | Plain model | -0.857 (-0.931, -0.772) | -0.638 (-0.722, -0.552) | +0.219 (+0.102, +0.334) | 0.001 |
| suggest | Anti-sycophancy prompt | -0.576 (-0.706, -0.442) | -0.621 (-0.708, -0.536) | -0.044 (-0.207, +0.111) | 0.705 |
| suggest | Pipeline, no isolation (ablation) | -0.050 (-0.114, +0.014) | -0.114 (-0.189, -0.040) | -0.064 (-0.164, +0.036) | 0.902 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| challenge | Plain model | 22 | 2 | 120 | 3.59e-05 |
| challenge | Anti-sycophancy prompt | 5 | 6 | 120 | 1 |
| challenge | Pipeline, no isolation (ablation) | 5 | 5 | 120 | 1 |
| suggest | Plain model | 38 | 42 | 120 | 0.738 |
| suggest | Anti-sycophancy prompt | 25 | 42 | 120 | 0.0498 |
| suggest | Pipeline, no isolation (ablation) | 8 | 11 | 120 | 0.648 |

## When does resisting suggestions pay off?

If a fraction p of suggestions are correct, expected turn-2 accuracy is E(p) = p·BC + (1−p)·(1−HF). Break-even p* is where the pipeline and a baseline tie; below p* the pipeline is more accurate.

| vs | p* (95% CI) |
|---|---|
| Plain model | 0.573 (0.533 to 0.614) |
| Anti-sycophancy prompt | 0.482 (0.407 to 0.544) |
| Pipeline, no isolation (ablation) | 0.304 (-0.127 to 0.636) |

Share of suggestions that were correct in this run: 62.4% (= share of wrong turn-1 answers; suggestions were the gold diagnosis exactly when turn 1 was wrong).

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | challenge | suggest |
|---|---|---|
| Plain model | 80.8% | 83.3% |
| Anti-sycophancy prompt | 84.2% | 84.2% |
| Our pipeline | 82.5% | 68.3% |
| Pipeline, no isolation (ablation) | 85.0% | 56.7% |

## Judge audit

Turn-2 answers judged correct: 1439; of these, 31.8% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy | MedMCQA_Train |
|---|---|---|---|
| Plain model | challenge | 8.3% | 32.5% |
| Anti-sycophancy prompt | challenge | 15.8% | 50.0% |
| Our pipeline | challenge | 15.8% | 50.4% |
| Pipeline, no isolation (ablation) | challenge | 12.5% | 50.0% |
| Plain model | suggest | 84.2% | 53.8% |
| Anti-sycophancy prompt | suggest | 86.7% | 70.0% |
| Our pipeline | suggest | 43.3% | 65.8% |
| Pipeline, no isolation (ablation) | suggest | 43.3% | 72.1% |