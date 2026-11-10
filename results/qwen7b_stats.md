# Case-clustered statistics: qwen7b

Model: qwen2.5:7b-instruct | judge: llama3.1:8b | cases: 120 | runs: 3 | rows: 2160
Bootstrap: 4000 resamples of cases (all runs of a case kept together).

## Net benefit of a follow-up turn, J = BC − HF (higher is better)

| Setup | Condition | HF | BC | J (95% CI) |
|---|---|---|---|---|
| Plain model | challenge | 44.7% | 4.6% | -0.401 (-0.526 to -0.281) |
| Anti-sycophancy prompt | challenge | 0.0% | 3.5% | +0.035 (+0.009 to +0.068) |
| Our pipeline | challenge | 2.9% | 2.3% | -0.006 (-0.040 to +0.023) |
| Plain model | suggest | 92.2% | 100.0% | +0.078 (+0.015 to +0.159) |
| Anti-sycophancy prompt | suggest | 64.1% | 98.3% | +0.341 (+0.208 to +0.472) |
| Our pipeline | suggest | 6.5% | 36.2% | +0.297 (+0.203 to +0.395) |

## Pipeline minus baseline (paired cluster bootstrap over cases)

| Condition | vs | ΔHF (95% CI) | ΔBC (95% CI) | ΔJ (95% CI) | P(ΔJ ≤ 0) |
|---|---|---|---|---|---|
| challenge | Plain model | -0.418 (-0.543, -0.298) | -0.023 (-0.056, +0.009) | +0.395 (+0.271, +0.523) | 0.000 |
| challenge | Anti-sycophancy prompt | +0.029 (+0.007, +0.060) | -0.012 (-0.045, +0.017) | -0.041 (-0.083, -0.004) | 0.989 |
| suggest | Plain model | -0.857 (-0.927, -0.770) | -0.638 (-0.723, -0.550) | +0.219 (+0.098, +0.332) | 0.001 |
| suggest | Anti-sycophancy prompt | -0.576 (-0.713, -0.444) | -0.621 (-0.704, -0.536) | -0.044 (-0.201, +0.114) | 0.695 |

## Case-level exact McNemar (majority vote over runs per case)

| Condition | vs | pipeline-only right | baseline-only right | cases | p |
|---|---|---|---|---|---|
| challenge | Plain model | 22 | 2 | 120 | 3.59e-05 |
| challenge | Anti-sycophancy prompt | 5 | 6 | 120 | 1 |
| suggest | Plain model | 38 | 42 | 120 | 0.738 |
| suggest | Anti-sycophancy prompt | 25 | 42 | 120 | 0.0498 |

## When does resisting suggestions pay off?

If a fraction p of suggestions are correct, expected turn-2 accuracy is E(p) = p·BC + (1−p)·(1−HF). Break-even p* is where the pipeline and a baseline tie; below p* the pipeline is more accurate.

| vs | p* (95% CI) |
|---|---|
| Plain model | 0.573 (0.533 to 0.615) |
| Anti-sycophancy prompt | 0.482 (0.410 to 0.544) |

Share of suggestions that were correct in this run: 61.9% (= share of wrong turn-1 answers; suggestions were the gold diagnosis exactly when turn 1 was wrong).

## Run-to-run consistency (share of cases with identical turn-2 correctness in all runs)

| Setup | challenge | suggest |
|---|---|---|
| Plain model | 80.8% | 83.3% |
| Anti-sycophancy prompt | 84.2% | 84.2% |
| Our pipeline | 82.5% | 68.3% |

## Judge audit

Turn-2 answers judged correct: 1079; of these, 31.0% have no literal overlap with the gold name or its listed synonyms. These are the candidates for lenient grading (synonyms and subtypes are legitimately counted correct). The 30-row human hand-check gives the actual error rate.

## By data source (turn-2 accuracy)

| Setup | Condition | Casestudy | MedMCQA_Train |
|---|---|---|---|
| Plain model | challenge | 8.3% | 32.5% |
| Anti-sycophancy prompt | challenge | 15.8% | 50.0% |
| Our pipeline | challenge | 15.8% | 50.4% |
| Plain model | suggest | 84.2% | 53.8% |
| Anti-sycophancy prompt | suggest | 86.7% | 70.0% |
| Our pipeline | suggest | 43.3% | 65.8% |