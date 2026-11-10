# Firm but Correctable: Validation and Publishability Report

*Status: complete for the initial study (10 Nov 2026). Every number below comes from the result files in `results/`, which are reproducible with `analyze.py`, `stats_extra.py` and `selectivity.py`.*

## Summary

- **Our pipeline cuts harmful answer changes under authority pressure from 64–92% to 3–7%.** With Qwen-14B it gives the best net benefit of all setups (ΔJ vs the anti-sycophancy prompt = +0.18 to +0.21; the CI excludes 0 under both the original and the strict judge).
- **It is the only setup that is "firm but correctable".** It changes its diagnosis for new evidence (54% / 94%) but almost never for wrong authority (8% / 0%), while both baselines do the opposite (selectivity +0.43 to +0.70 vs −0.62 to −0.84).
- **Mechanism.** The structured adjudication provides most of the robustness. Isolation adds correctability at 14B (ΔJ +0.10 with the original judge; +0.08, CI just crossing 0, with the strict judge), so it's a trend, not a confirmed effect. No effect at 7B.
- **What doesn't hold.** At 7B the pipeline only matches the anti-sycophancy prompt. Under a bare "Are you sure?" the pipeline and the prompt are equivalent. Evidence rarely produces the *correct* rare diagnosis with these small models.
- **Validation caught one serious error:** v1 evidence turns contained fabricated findings. They were invalidated and rebuilt.
- **Verdict: promising, not yet journal-ready.** See §4 for the gaps and the route.

## 1. What we ran

| Item | Detail |
|---|---|
| Test set | 120 vignettes from Samsel et al. (80 MedMCQA + 40 case reports); same cases and same wrong-diagnosis distractors for every model |
| Tested models | Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct (local, Ollama, Q4, temperature 0.7, 3 runs) |
| Judge | Llama-3.1-8B (different family), temperature 0 |
| Setups | Plain model; anti-sycophancy prompt; our 4-agent pipeline; ablation without isolation |
| Follow-ups | "Are you sure?" challenge; authority suggestion (gold if turn 1 was wrong, distractor if right); new clinical evidence from the full case report (29 cases, v2) |
| Volume | 4,320 main conversations + evidence + ablation runs |

## 2. Main results

### 2.1 Pressure and authority (120 cases × 3 runs)

| Model | Setup | Harmful flips under authority | Correct suggestions accepted | J = BC − HF (95% CI) |
|---|---|---|---|---|
| 7B | Plain | 92.2% | 100% | +0.08 (+0.02, +0.16) |
| 7B | Anti-syc prompt | 64.1% | 98.3% | +0.34 (+0.21, +0.47) |
| 7B | **Pipeline** | **6.5%** | 36.2% | +0.30 (+0.20, +0.40) |
| 14B | Plain | 83.0% | 100% | +0.17 (+0.08, +0.27) |
| 14B | Anti-syc prompt | 65.6% | 100% | +0.34 (+0.24, +0.45) |
| 14B | **Pipeline** | **3.0%** | **57.9%** | **+0.55 (+0.45, +0.65)** |

- **14B: the pipeline beats both baselines on net benefit.** Against the anti-sycophancy prompt, ΔJ = +0.205 (95% CI +0.05 to +0.36; 99.3% of bootstrap draws are above 0).
- **7B: the pipeline matches the prompt but doesn't beat it** (ΔJ = −0.04, CI −0.20 to +0.11). It sits at a firmer operating point.
- **Capability scaling.** From 7B to 14B, the pipeline's correction rate rose by 22 points while its harmful flips fell. Diagnosis at 7B: triage labelled 100% of suggestions correctly, but the blind re-assessor kept its own earlier answer 62% of the time. The limit is the re-assessor's medical knowledge, not the isolation.
- **"Are you sure?"** A plain model flips 45–58% of correct answers. The prompt and the pipeline both prevent this (0–3%). At 14B, the pipeline also recovers more wrong answers (6.2% vs 1.5%).

### 2.2 Selectivity: what makes each setup change its mind (29 case-report cases)

| 7B setup | "Are you sure?" | Wrong authority | New evidence | Selectivity S (95% CI) |
|---|---|---|---|---|
| Plain | 55.2% | 100% | 16.1% | −0.84 (−0.94, −0.72) |
| Anti-syc prompt | 6.9% | 92.3% | 27.6% | −0.65 (−0.83, −0.42) |
| **Pipeline** | **6.9%** | **7.7%** | **54.0%** | **+0.46 (+0.26, +0.59)** |

| 14B setup | "Are you sure?" | Wrong authority | New evidence | Selectivity S (95% CI) |
|---|---|---|---|---|
| Plain | 88.5% | 100% | 21.8% | −0.78 (−0.90, −0.64) |
| Anti-syc prompt | 3.4% | 100% | 24.1% | −0.76 (−0.87, +0.23) |
| **Pipeline** | 24.1% | **0%** | **94.3%** | **+0.70 (+0.61, +0.79)** |

- **The 14B pipeline's changes under "Are you sure?" are re-checks of wrong answers only.** It changed 0 of 8 correct answers and 27% of wrong ones, the designed blind re-check. Across all 120 cases its harmful-flip rate under challenge is 1.2%.
- **On new evidence (14B)** the pipeline has the best turn-2 accuracy (18.4% vs 13.8% prompt, 12.6% plain) and **0 harmful flips**. The sample is small: 29 cases, only 8–10 correct turn-1 answers per setup.
- **Small authority samples.** The "wrong authority" column on these 29 cases rests on 7–16 rows, because the models rarely get these rare cases right first time. The authority result over all 120 cases is in §2.1.

**This is the core finding.** The plain model is *inverted*: it changes its answer more for social pressure than for evidence. The prompt fixes "Are you sure?" but still caves to authority. Only the pipeline is firm under pressure and authority **and** responsive to new evidence.

**Caveat.** At 7B, evidence rarely leads to the *correct* diagnosis in any setup (0–3%), because these are rare diseases. Selectivity measures responsiveness, not accuracy.

### 2.3 Ablation: is isolation the active ingredient?

`pipeline_noiso` is identical to the pipeline except that the deciding re-assessor also sees the user's raw message. Same 120 cases, seed and judge.

| Model | Setup | Authority: harmful flips | Authority: correct accepted | J (95% CI) |
|---|---|---|---|---|
| 7B | Pipeline (isolated) | 6.5% | 36.2% | +0.30 (+0.20, +0.39) |
| 7B | Pipeline, no isolation | 11.5% | 47.6% | +0.36 (+0.26, +0.46) |
| 14B | Pipeline (isolated) | 3.0% | 57.9% | **+0.55 (+0.45, +0.65)** |
| 14B | Pipeline, no isolation | 4.2% | 49.5% | +0.45 (+0.34, +0.56) |

Isolated minus no-isolation (paired cluster bootstrap):

| Model | Condition | ΔHF | ΔBC | ΔJ (95% CI) |
|---|---|---|---|---|
| 7B | authority | −0.050 | −0.114 | −0.064 (−0.164, +0.036) |
| 7B | "Are you sure?" | −0.002 | −0.012 | −0.011 (−0.057, +0.037) |
| 14B | authority | −0.011 | **+0.085** | **+0.096 (+0.011, +0.183)** |
| 14B | "Are you sure?" | −0.018 | **+0.041** | **+0.058 (+0.010, +0.110)** |

**Reading.**
1. **Robustness comes mainly from the structure.** In both models the no-isolation pipeline is already far firmer than the baselines (harmful flips 4–12% vs 64–92%). Turning the claim into a candidate, verifying it and re-assessing it separately does most of the work.
2. **Isolation adds correctability, and only at 14B.** With a capable re-assessor, hiding the user's wording raises the share of *correct* claims accepted (+8.5 points under authority; +4 points of recovered wrong answers under "Are you sure?") without adding harmful flips. When the deciding agent sees "I'm a senior physician" or "Are you sure?", it appears to become defensive. Without the social framing it judges the claim on its merits. At 7B the effect is absent: the model is too weak to verify claims either way.
3. **Strict re-grading weakens point 2.** Under the strict judge, the 14B isolation benefit is ΔJ = +0.083 (95% CI −0.006 to +0.164; 96.9% of bootstrap draws above 0) under authority, and +0.008 (n.s.) under "Are you sure?". The isolation benefit is a **consistent trend, not a confirmed effect**, and needs more cases or a stronger model to confirm.
4. **What this means for our claim.** The robust contribution is **structured adjudication**. Pressure isolation is a promising addition whose benefit appears to grow with model capability. We shouldn't claim isolation alone causes the robustness.

## 3. Validation: what we checked, and what we found wrong

| Check | Result |
|---|---|
| Data integrity | 2,160 rows per model, no duplicates, the same 120 cases and identical distractors across models, every pipeline row triaged |
| Reproducibility | `analyze.py` on the raw records reproduces the GPU summary byte-for-byte |
| Statistics | Re-done with the **case** as the unit (cluster bootstrap; case-level McNemar on majority votes), because the 3 runs of a case aren't independent. The 7B pooled "prompt beats pipeline on turn-2 accuracy" result (p=0.0002) weakens to p=0.05 at case level; the 14B ΔJ advantage holds (CI excludes 0) |
| Triage | 99.6% (7B) and 100% (14B) of messages labelled as built; 99% of evidence turns labelled "fact" |
| **Evidence turns v1: INVALID** | The extractor copied the prompt's example findings ("Serum potassium 2.1 mmol/L", "Biopsy: non-caseating granulomas") into 19 of 40 cases. We stopped the runs, kept the files as `*_v1_INVALID*`, and rebuilt v2 with a grounding check (every number and most words must appear in the source report) and a stricter leak check. v2: 29/40 usable, 0 ungrounded findings |
| Judge leniency | Preliminary review of 30 + 30 sampled verdicts (the formal `human_correct` labels are still empty): about 10% lenient (broader diagnosis accepted, e.g. "nephrotic syndrome" for minimal change disease). **Every answer was re-graded with a strict judge** (see §3.1) |
| Model-family overlap | The evidence extractor and the judge are the same model (Llama-3.1-8B); stated as a limitation |

### 3.1 Strict re-grading (sensitivity analysis)

`rejudge.py` re-graded every turn-1 and turn-2 answer with a stricter prompt: broader categories and associated conditions count as wrong, and its examples are not from the test set. It changed 8.3% (7B) and 6.7% (14B) of turn-1 verdicts. Suggestion rows whose strict turn-1 verdict changed were dropped (90 rows for 7B, 72 for 14B), because the suggestion type no longer matched.

| Finding | Original judge | Strict judge | Holds? |
|---|---|---|---|
| 14B pipeline vs prompt, authority, ΔJ | +0.205 (+0.05, +0.35) | **+0.180 (+0.02, +0.34)** | **Yes** |
| 14B pipeline vs plain, authority, ΔJ | +0.379 | +0.373 (+0.23, +0.51) | Yes |
| 14B pipeline vs prompt, "Are you sure?", ΔJ | +0.053 (−0.001, +0.11) | −0.015 (−0.07, +0.04) | **No.** The pipeline and the prompt are equivalent here |
| 7B pipeline vs prompt, authority, ΔJ | −0.044 (n.s.) | −0.072 (n.s.) | Same conclusion: no difference |
| Harmful flips under authority, pipeline | 6.5% / 3.0% | 7.3% / 3.4% | Yes |
| Selectivity S, pipeline (7B / 14B) | +0.46 / +0.70 | **+0.43 / +0.70** | **Yes** |

The headline findings (the authority effect at 14B, and selectivity) are robust to grading strictness. The small 14B advantage under "Are you sure?" is not; we report the pipeline and the prompt as equivalent there.

## 4. Is it promising? Is it publishable?

**Promising: yes.** Three results would interest reviewers:
1. **A large, clean safety effect.** Under a wrong authority suggestion, harmful flips fall from 83–92% (plain) and 64–66% (anti-sycophancy prompt) to **3–6.5%**. With 14B, net benefit beats the strongest baseline: ΔJ = +0.21 (95% CI +0.05, +0.35).
2. **Selectivity.** Plain models change their answer *more* for social pressure than for evidence. The pipeline reverses this: S = +0.46 (7B) and +0.70 (14B), while both baselines are strongly negative. "Selectivity" is a simple, new way to show "firm but correctable" in one number.
3. **Mechanism and scaling.** The structure gives robustness. Isolation shows a trend towards extra correctability at 14B that isn't yet confirmed under strict grading. Correction rises with model size (36% → 58%) while harmful flips fall.

**Journal-ready: not yet.** A Q1 reviewer would raise these gaps, most serious first:

| # | Gap | What fixes it | Effort |
|---|---|---|---|
| 1 | Only one model family (Qwen), small open models | Add 1–2 frontier API models and another open family (e.g. Llama-3.x-70B or Gemma) | ~1 week, ~$50–150 API |
| 2 | Automated grading only (LLM judge, ~10% lenient; extractor = judge) | Clinician labels on about 200 answers; report kappa; use strict re-grading as a sensitivity check | 1–2 weeks (needs a clinician) |
| 3 | Small, auto-extracted evidence set (29 cases; floor effect at 7B) | About 100 clinician-checked evidence turns, including cases where the model's turn-1 answer is wrong but solvable | 1–2 weeks |
| 4 | Only two pressure types | Add emotion, social proof, fake citation, multi-turn escalation, and SycoEval-EM patient dialogues | ~1 week |
| 5 | Missing baselines | Third-person prompt, role-based prompt, two-agent debate (all planned) | ~3 days |
| 6 | The suggestion design ties the share of correct suggestions to turn-1 accuracy | Report the break-even analysis (already done); add a condition with a controlled share of correct suggestions | ~2 days |
| 7 | Cost | The pipeline uses ~2–2.5× the tokens; report cost per turn, and try merging triage and verifier | ~2 days |

**Realistic route.**
1. **Now (results as they are, plus gaps 5 and 6):** a workshop paper or arXiv preprint, e.g. a clinical-NLP or ML-for-health workshop.
2. **After gaps 1, 3 and 4:** competitive for a main conference track (e.g. ACL/EMNLP via ARR, or *Findings*).
3. **After gap 2 as well (clinician validation):** Q1 medical-informatics journals, e.g. *npj Digital Medicine*, *JAMIA*, *Artificial Intelligence in Medicine*, *Journal of Biomedical Informatics*. Check each journal's current scope and quartile before submitting.

**Estimated time to journal-ready:** about 4–6 weeks of team work. That fits the December semester deadline for a strong preprint and submission draft.

## 5. Deliverables ready for the assignment

- **Code:** `sycorun.py` (runner), `analyze.py`, `stats_extra.py`, `selectivity.py`, `build_evidence.py`, `rejudge.py`, `runner/*.ps1`, all in the private GitHub repo `bilalashfaq123/firm-but-correctable`.
- **Results:** `results/*_summary.md`, `*_stats.md`, `selectivity.md`, and the raw `*.jsonl` (every conversation).
- **Graphs** (`results/figures/`):
  - 1 harmful flips; 2 beneficial corrections; 3 robustness–correctability plane; 4 accuracy before and after; 5 triage confusion matrix; 6 cost
  - 7 net benefit J; 8 break-even
  - `selectivity.png`, the recommended headline figure
- **On "training graphs":** the method is inference-only, with no training. The evaluation graphs above stand in for them; say this explicitly in the submission.
