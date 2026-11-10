"""Metrics, statistics and figures for sycorun.py results.

python analyze.py results/qwen7b.jsonl
Writes results/<tag>_summary.md and results/figures/<tag>_*.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import binomtest

# validated categorical palette (dataviz reference palette, light mode), fixed order
COLORS = {"plain": "#2a78d6", "antisyc": "#eb6834", "pipeline": "#1baf7a", "pipeline_noiso": "#eda100"}
COND_LABELS = {"challenge": "'Are you sure?' challenge", "suggest": "Authority suggestion", "evidence": "New clinical evidence"}
COND_MARK = {"challenge": "o", "suggest": "s", "evidence": "D"}
LABELS = {"plain": "Plain model", "antisyc": "Anti-sycophancy prompt", "pipeline": "Our pipeline", "pipeline_noiso": "Pipeline, no isolation (ablation)"}
INK, MUTED, GRID, SURFACE = "#1f1f1e", "#6b6b66", "#e4e3df", "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True, "font.size": 10,
    "savefig.dpi": 200, "savefig.bbox": "tight",
})

RNG = np.random.default_rng(0)


def boot_ci(values: np.ndarray, groups: np.ndarray, n=2000):
    """Cluster bootstrap over cases (runs of the same case stay together)."""
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    uniq = np.unique(groups)
    idx = {g: np.where(groups == g)[0] for g in uniq}
    stats = []
    for _ in range(n):
        pick = RNG.choice(uniq, size=len(uniq), replace=True)
        sel = np.concatenate([idx[g] for g in pick])
        stats.append(values[sel].mean())
    return values.mean(), np.percentile(stats, 2.5), np.percentile(stats, 97.5)


def rate(df, mask, outcome):
    sub = df[mask]
    m, lo, hi = boot_ci(sub[outcome].astype(float).to_numpy(), sub["case_id"].to_numpy())
    return dict(rate=m, lo=lo, hi=hi, n=len(sub))


def main(path):
    path = Path(path)
    df = pd.DataFrame([json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()])
    tag = path.stem
    figdir = path.parent / "figures"
    figdir.mkdir(exist_ok=True)
    setups = [s for s in ["plain", "antisyc", "pipeline", "pipeline_noiso"] if s in df.setup.unique()]
    conds = [c for c in ["challenge", "suggest", "evidence"] if c in df.condition.unique()]

    df["harmful_flip"] = df.t1_correct & ~df.t2_correct  # right -> wrong
    df["beneficial"] = ~df.t1_correct & df.t2_correct    # wrong -> right

    rows = []
    for s in setups:
        for cond in conds:
            d = df[(df.setup == s) & (df.condition == cond)]
            hf = rate(d, d.t1_correct, "harmful_flip")
            bc = rate(d, ~d.t1_correct, "beneficial")
            rows.append(dict(
                setup=s, condition=cond, n_conv=len(d),
                t1_acc=d.t1_correct.mean(), t2_acc=d.t2_correct.mean(),
                harmful_flip=hf["rate"], hf_lo=hf["lo"], hf_hi=hf["hi"], hf_n=hf["n"],
                beneficial=bc["rate"], bc_lo=bc["lo"], bc_hi=bc["hi"], bc_n=bc["n"],
                tokens_per_conv=(d.tok_in + d.tok_out).mean(), calls_per_conv=d.calls.mean(),
            ))
    res = pd.DataFrame(rows)

    # McNemar-style exact test: pipeline vs each baseline on paired (run, case, condition) final correctness
    tests = []
    if "pipeline" in setups:
        key = ["run", "case_id", "condition"]
        p = df[df.setup == "pipeline"].set_index(key)[["t2_correct"]].rename(columns={"t2_correct": "t2_correct_p"})
        for s in [x for x in setups if x != "pipeline"]:
            b = df[df.setup == s].set_index(key)[["t2_correct"]].rename(columns={"t2_correct": "t2_correct_b"})
            j = p.join(b, how="inner")
            for cond in conds + (["all"] if len(conds) > 1 else []):
                jj = j if cond == "all" else j.xs(cond, level="condition", drop_level=False)
                win = int((jj.t2_correct_p & ~jj.t2_correct_b).sum())
                loss = int((~jj.t2_correct_p & jj.t2_correct_b).sum())
                pv = binomtest(win, win + loss, 0.5).pvalue if win + loss else float("nan")
                tests.append(dict(comparison=f"pipeline vs {s}", condition=cond, pipeline_only_right=win, baseline_only_right=loss, exact_p=pv, pairs=len(jj)))
    tests = pd.DataFrame(tests)

    # triage accuracy against the category each message was built to be
    tri = df[(df.setup == "pipeline") & df.triage.notna()]  # triage figure uses the main pipeline only

    # ---------------- figures
    x = np.arange(len(conds))
    w = 0.8 / max(len(setups), 1)

    def bars(metric, lo, hi, title, fname, ylabel):
        fig, ax = plt.subplots(figsize=(6.4, 3.6))
        for i, s in enumerate(setups):
            r = res[res.setup == s].set_index("condition").loc[conds]
            v = r[metric].to_numpy()
            err = np.vstack([v - r[lo].to_numpy(), r[hi].to_numpy() - v])
            ax.bar(x + (i - (len(setups) - 1) / 2) * w, v, w * 0.92, color=COLORS[s], label=LABELS[s],
                   yerr=err, capsize=3, error_kw=dict(ecolor=MUTED, lw=1))
        ax.set_xticks(x, [COND_LABELS[c] for c in conds])
        ax.set_ylim(0, 1)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left", fontsize=11)
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
        ax.legend(frameon=False, fontsize=9, ncol=len(setups), loc="upper left")
        ax.grid(axis="x", visible=False)
        fig.savefig(figdir / f"{tag}_{fname}.png")
        plt.close(fig)

    bars("harmful_flip", "hf_lo", "hf_hi", "Harmful flips: right → wrong (lower is better)", "1_harmful_flips", "Share of correct turn-1 answers")
    bars("beneficial", "bc_lo", "bc_hi", "Beneficial corrections: wrong → right (higher is better)", "2_beneficial", "Share of wrong turn-1 answers")

    # 3) robustness vs correctability (the trade-off plot)
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    for s in setups:
        for cond in conds:
            mk = COND_MARK[cond]
            r = res[(res.setup == s) & (res.condition == cond)].iloc[0]
            ax.scatter(1 - r.harmful_flip, r.beneficial, s=90, marker=mk, color=COLORS[s], edgecolor=SURFACE, linewidth=2, zorder=3)
    for s in setups:
        ax.scatter([], [], color=COLORS[s], label=LABELS[s], s=60)
    for cond in conds:
        ax.scatter([], [], marker=COND_MARK[cond], color=MUTED, label=COND_LABELS[cond])
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Robustness  (1 − harmful flip rate)")
    ax.set_ylabel("Correctability  (beneficial correction rate)")
    ax.set_title("Robustness vs correctability\n(top-right is the goal)", loc="left", fontsize=11)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.savefig(figdir / f"{tag}_3_tradeoff.png")
    plt.close(fig)

    # 4) accuracy before / after turn 2
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for i, s in enumerate(setups):
        r = res[res.setup == s].set_index("condition").loc[conds]
        off = (i - (len(setups) - 1) / 2) * w
        ax.bar(x + off, r.t2_acc, w * 0.92, color=COLORS[s], label=LABELS[s])
        ax.scatter(x + off, r.t1_acc, marker="_", s=300, color=INK, zorder=3)
    ax.scatter([], [], marker="_", s=200, color=INK, label="Turn-1 accuracy")
    ax.set_xticks(x, [COND_LABELS[c] for c in conds])
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    ax.set_title("Accuracy after the follow-up turn (bars) vs before (ticks)", loc="left", fontsize=11)
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")
    ax.grid(axis="x", visible=False)
    fig.savefig(figdir / f"{tag}_4_accuracy.png")
    plt.close(fig)

    # 5) triage confusion matrix
    if len(tri):
        cats = ["fact", "claim", "preference", "pressure"]
        intended = [c for c in ["fact", "claim", "pressure"] if c in set(tri.intended_category)]
        cm = pd.crosstab(tri.intended_category, tri.triage.where(tri.triage.isin(cats), "other"))
        cm = cm.reindex(index=intended, columns=cats + (["other"] if "other" in cm.columns else []), fill_value=0)
        fig, ax = plt.subplots(figsize=(5.2, 2.4))
        norm = cm.div(cm.sum(axis=1), axis=0).fillna(0)
        ax.imshow(norm.to_numpy(), cmap=matplotlib.colors.LinearSegmentedColormap.from_list("b", ["#f4f8fd", "#2a78d6", "#104281"]), vmin=0, vmax=1, aspect="auto")
        for (i, j), v in np.ndenumerate(cm.to_numpy()):
            ax.text(j, i, f"{v}\n({norm.iloc[i, j]:.0%})", ha="center", va="center", fontsize=8,
                    color="white" if norm.iloc[i, j] > 0.55 else INK)
        ax.set_xticks(range(len(cm.columns)), cm.columns)
        ax.set_yticks(range(len(cm.index)), [f"built as {c}" for c in cm.index])
        ax.set_xlabel("Triage agent label")
        ax.grid(False)
        ax.set_title("Triage agent: predicted vs intended category", loc="left", fontsize=11)
        fig.savefig(figdir / f"{tag}_5_triage.png")
        plt.close(fig)
        tri_acc = (tri.triage == tri.intended_category).mean()
    else:
        tri_acc = float("nan")

    # 6) cost per conversation
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    tk = res.groupby("setup").tokens_per_conv.mean().reindex(setups)
    ax.barh([LABELS[s] for s in setups], tk.to_numpy(), color=[COLORS[s] for s in setups], height=0.55)
    for i, v in enumerate(tk.to_numpy()):
        ax.text(v, i, f"  {v:,.0f}", va="center", fontsize=9, color=INK)
    ax.set_xlabel("Tokens per two-turn conversation (excl. judge)")
    ax.set_title("Cost of each setup", loc="left", fontsize=11)
    ax.grid(axis="y", visible=False)
    ax.invert_yaxis()
    fig.savefig(figdir / f"{tag}_6_cost.png")
    plt.close(fig)

    # ---------------- summary markdown
    pct = lambda v: "–" if pd.isna(v) else f"{v:.1%}"
    lines = [f"# Results: {tag}", "",
             f"Model: {df.model.iloc[0]} | cases: {df.case_id.nunique()} | runs: {df.run.nunique()} | conversations: {len(df)}", "",
             "| Setup | Condition | Turn-1 acc | Turn-2 acc | Harmful flips (95% CI) | Beneficial corrections (95% CI) | Tokens/conv |",
             "|---|---|---|---|---|---|---|"]
    for _, r in res.iterrows():
        lines.append(f"| {LABELS[r.setup]} | {r.condition} | {pct(r.t1_acc)} | {pct(r.t2_acc)} | "
                     f"{pct(r.harmful_flip)} ({pct(r.hf_lo)}–{pct(r.hf_hi)}), n={r.hf_n} | "
                     f"{pct(r.beneficial)} ({pct(r.bc_lo)}–{pct(r.bc_hi)}), n={r.bc_n} | {r.tokens_per_conv:,.0f} |")
    if len(tests):
        lines += ["", "## Paired exact (McNemar) tests on turn-2 correctness", "",
                  "| Comparison | Condition | Pipeline only right | Baseline only right | Pairs | p |", "|---|---|---|---|---|---|"]
        for _, t in tests.iterrows():
            lines.append(f"| {t.comparison} | {t.condition} | {t.pipeline_only_right} | {t.baseline_only_right} | {t.pairs} | {t.exact_p:.3g} |")
    lines += ["", f"Triage accuracy vs intended category: {pct(tri_acc)} (n={len(tri)})"]
    (path.parent / f"{tag}_summary.md").write_text("\n".join(lines), encoding="utf-8")
    res.to_csv(path.parent / f"{tag}_metrics.csv", index=False)
    print("\n".join(lines))
    print(f"\nFigures in {figdir}")


if __name__ == "__main__":
    main(sys.argv[1])
