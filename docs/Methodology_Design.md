# Methodology Design: Firm but Correctable

## 1. The gap we target

- **The problem.** LLM medical assistants change correct answers when users push back. Samsel et al. [4] found 544 right-to-wrong changes after a simple "Are you sure?".
- **Current fixes trade one problem for another.** Prompts and fine-tuning that make a model firmer also make it harder to correct with valid evidence [10]. A single model has to weigh *what* the user said and *how forcefully* they said it in the same step.
- **What is missing.** In our October 2026 searches, we found no inference-time, multi-agent design for medicine that keeps the model making the decision away from the social pressure in a user's message.

## 2. Core idea: separate content from pressure

Any follow-up message *m* mixes two things:
- **content** *c*: new facts, or a proposed diagnosis
- **social signal** *s*: doubt, authority, emotion, insistence

**A single model** decides *y = g(x, m)*, where *x* is the case. The decision therefore depends on *s*, and that dependence is sycophancy.

**Our pipeline** decides *y = f(x, T(m))*, where the triage step *T* passes on only *c*.
- **Firm:** the decision is unaffected by *s* by construction, since ∂y/∂s = 0.
- **Correctable:** the decision still responds to *c*.

## 3. Architecture (who sees what)

```
User message m ──► [1 Triage] ── category + extracted content c ──┐
                      (reads m)                                   │
                                                                  ▼
Case facts x ─────────────────────────► [2 Verifier] ── neutral evidence note
                                         (sees x, c; not m)       │
                                                                  ▼
Previous answer + proposed dx ────────► [3 Blind re-assessor] ── decision y
  (shuffled, source hidden)               (sees x, c, note; never m)
                                                                  ▼
User message m + decision y ──────────► [4 Communicator] ── reply (cannot change y)
```

| Category (from triage) | What reaches the decision |
|---|---|
| Fact (new finding) | Added to the case facts |
| Claim (proposed diagnosis) | Becomes a candidate; the verifier checks it against the facts |
| Preference (patient wish) | Not passed to the diagnosis (handled by the communicator) |
| Pressure ("Are you sure?", authority) | Dropped. It triggers a **fresh blind re-check** from the facts, so beneficial re-thinking is kept without the social push |

## 4. Research questions and hypotheses

| RQ | Question | Hypothesis | Metric |
|---|---|---|---|
| RQ1 | Does the pipeline reduce harmful flips under pressure? | HF(pipeline) < HF(baselines) | Harmful flip rate |
| RQ2 | Does it stay correctable? | BC(pipeline) does not drop as much as for firm-prompt baselines | Beneficial correction rate |
| RQ3 | Can the triage agent sort messages reliably? | Accuracy at least 80% | Triage accuracy, confusion matrix |

## 5. Measures (the maths)

For case *i*, let *a_i* = 1 if the turn-1 answer is correct, and *b_i* = 1 if the turn-2 answer is correct.

- **Harmful flip rate:** HF = P(b = 0 | a = 1)
- **Beneficial correction rate:** BC = P(b = 1 | a = 0)
- **Robustness** R = 1 − HF; **correctability** C = BC
- **Net effect of pushback:** J = R + C − 1 = BC − HF. A sycophantic model has high C but low R; a stubborn model has high R but low C. **The goal is the top-right of the R–C plane.**
- **Paired test:** exact McNemar test on the discordant pairs (pipeline right / baseline wrong vs the reverse), same case and same run.
- **Uncertainty:** 95% bootstrap confidence intervals, resampling cases (runs of a case are kept together).

## 6. Experimental design

| Element | Initial results (this deadline) | Final study (December) |
|---|---|---|
| Cases | 120 vignettes from [4] (80 MedMCQA + 40 case reports) | + MedMCQA scale-up, SycoEval-EM [6] |
| Setups | Plain; anti-sycophancy prompt; **our pipeline** | + third-person prompt [8], role-based prompt [10], two-agent debate |
| Pressure condition | "Are you sure?" challenge | + authority, emotion, social proof, fake citation |
| Correction condition | Authority suggestion: the gold diagnosis if the first answer was wrong, a same-chapter distractor if it was right | + **real new-evidence turns** (~100 hand-built, clinically checked) |
| Models | Qwen2.5-7B and 14B (local GPU), temperature 0.7, 3 runs | + one API frontier model |
| Judge | Llama-3.1-8B (different family), plus a 30-answer hand-check | + validation on about 50 labelled answers |

## 7. How the results fill the gap

- **Pipeline improves both.** Its point sits up and to the right of both baselines in the R–C plot: fewer harmful flips **and** no loss in correction. That is evidence that pressure isolation breaks the trade-off a single model faces.
- **Pipeline is only firmer.** If it only moves right (firmer but less correctable), the isolation works but the verifier lets through too little content. We then tune the verifier, not the isolation.
- **Cost.** We report the extra tokens per turn so the result can be judged for practical use.

## 8. Known limits of the initial results

1. **Suggestion is not evidence.** The correction condition uses an authority claim that happens to be right, not new clinical evidence. That makes it a *lower bound* on correctability.
2. **Small open models.** Qwen2.5-7B has low turn-1 accuracy, so the harmful-flip sample is small. The 14B run helps.
3. **Automated grading.** A small open model grades the answers; we hand-check a sample.
4. **Not clinically validated.** The results are not evidence that the system is safe for clinical use.
