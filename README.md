# Firm but Correctable

Code, data and results for our Mathematical Foundations of AI semester project.

| Group member | Roll number |
|---|---|
| Muhammad Bilal Ashfaq | 26i-7671 |
| Mujtaba Abbas | 26i-7626 |

We test a four-agent medical assistant that keeps the agent making the diagnosis away from the user's social pressure. A triage agent sorts each follow-up message, a verifier checks any proposed diagnosis against the case, a blind re-assessor decides without seeing the user's wording, and a communicator writes the reply but cannot change the decision. We compare it with a plain model and with an anti-sycophancy prompt.

The written report is submitted separately.

## Training graphs

No model is trained or fine-tuned in this project. Every agent, both baselines and the judge use pretrained open models (Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct, Llama-3.1-8B) unchanged, so there are no training curves. The evaluation graphs are in `results/figures/`.

| Figure suffix | What it shows |
|---|---|
| `_1_harmful_flips` | Share of correct answers given up after the follow-up |
| `_2_beneficial` | Share of wrong answers corrected |
| `_3_tradeoff` | Robustness against correctability for each setup |
| `_4_accuracy` | Accuracy before and after the follow-up |
| `_5_triage` | Triage confusion matrix |
| `_6_cost` | Tokens per conversation |
| `_7_net_benefit` | Net benefit J = BC − HF with 95% CIs |
| `_8_breakeven` | Break-even share of correct suggestions |
| `selectivity.png` | How often each setup changes its diagnosis under doubt, authority and new evidence |

File prefixes: `qwen7b`, `qwen14b` (main runs), `_evidence` (new-evidence turns), `_ablation` (re-assessor also sees the message), `_strict` (strict re-grading), `pilot_` (first 10-case pilot).

## Layout

| Path | Contents |
|---|---|
| `sycorun.py` | Runs the experiment: setups, follow-up messages, judge |
| `analyze.py` | Summary tables, McNemar tests, figures 1 to 6 |
| `stats_extra.py` | Case-clustered bootstrap, net benefit, break-even, figures 7 and 8 |
| `selectivity.py` | Selectivity table and `selectivity.png` |
| `build_evidence.py` | Builds the new-evidence turns from the full case reports, with a grounding check |
| `rejudge.py` | Re-grades every answer with a stricter judge prompt |
| `verify_claims.py` | Recomputes the report's numbers from the raw logs |
| `runner/` | GPU run script with a temperature guard, and helper scripts |
| `data/` | Evidence turns (`evidence_turns.jsonl`); the discarded first version is kept as `evidence_turns_v1_INVALID.jsonl` |
| `results/` | Every conversation (`*.jsonl`), summaries, statistics, hand-check sheets, figures |

## Data

The 120 vignettes come from Samsel et al., "Too agreeable to be accurate?" (Artificial Intelligence in Medicine, 2026). Their repository has no licence file, so the spreadsheet is not included here. Download it into `data/`:

```bash
curl -L -o data/Sycophancy_Main.xlsx \
  https://github.com/HIVE-UofT/Investigating-The-Impact-of-Sycophancy-on-Diagnostic-Accuracy/raw/main/Benchmark/data/Sycophancy_Main.xlsx
```

The result files in `results/` are enough to rerun every analysis without it.

## Reproduce

```bash
pip install -r requirements.txt

# models served locally with Ollama (OpenAI-compatible endpoint)
ollama pull qwen2.5:7b-instruct
ollama pull llama3.1:8b

# main run: 120 cases x 3 setups x 2 follow-ups x 3 runs
python sycorun.py --backend openai --base-url http://localhost:11434/v1 \
  --model qwen2.5:7b-instruct --runs 3 --temperature 0.7 --out qwen7b \
  --judge-backend openai --judge-base-url http://localhost:11434/v1 --judge-model llama3.1:8b

# analysis (works on the included result files)
python analyze.py results/qwen7b.jsonl
python stats_extra.py results/qwen7b.jsonl
python selectivity.py results/qwen7b.jsonl results/qwen7b_evidence.jsonl results/qwen14b.jsonl results/qwen14b_evidence.jsonl
python verify_claims.py .
```

`python sycorun.py --help` lists every option. `--backend mock` runs the whole pipeline with random answers, for testing without a model.

Hardware used: one RTX 5080 (16 GB), Ollama with 4-bit models, context length 4096. The 14B runs used the judge on the CPU (`runner/Modelfile.llama-cpu`) to fit in GPU memory.
