"""Independent recomputation of every number in the report, straight from raw jsonl (no project code)."""
import json, re, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
R = Path(sys.argv[1]) / "results"
D = Path(sys.argv[1]) / "data"
rng = np.random.default_rng(1)
def load(n): return pd.DataFrame([json.loads(l) for l in (R / n).read_text(encoding="utf-8").splitlines() if l.strip()])
def hf_bc(d):
    r, w = d[d.t1_correct], d[~d.t1_correct]
    return (1 - r.t2_correct.mean()), w.t2_correct.mean(), len(r), len(w)
def J(d): hf, bc, *_ = hf_bc(d); return bc - hf
def boot_dJ(a, b, B=2000):
    cases = sorted(set(a.case_id)); ga = {c: g for c, g in a.groupby("case_id")}; gb = {c: g for c, g in b.groupby("case_id")}
    out = []
    for _ in range(B):
        s = rng.choice(cases, len(cases))
        A = pd.concat([ga[c] for c in s if c in ga]); Bb = pd.concat([gb[c] for c in s if c in gb])
        out.append(J(A) - J(Bb))
    return np.percentile(out, [2.5, 97.5])
def dx(t):
    m = re.search(r"Diagnosis:\s*(.+)", t or ""); s = (m.group(1) if m else "").lower().split("(")[0]
    return re.sub(r"[^a-z ]", "", s).strip()[:25]
chg = lambda d: (d.t1_answer.map(dx) != d.t2_answer.map(dx)).mean()

for tag in ["qwen7b", "qwen14b"]:
    m = load(f"{tag}.jsonl"); s = load(f"{tag}_strict.jsonl"); ev = load(f"{tag}_evidence.jsonl"); ab = load(f"{tag}_ablation.jsonl")
    print(f"\n===== {tag}: rows={len(m)} cases={m.case_id.nunique()} runs={sorted(m.run.unique())} dup={m.duplicated(['run','setup','condition','case_id']).sum()}")
    print("origins:", m.drop_duplicates('case_id').origin.value_counts().to_dict(), "| model:", m.model.iloc[0], "| judge:", m.judge_model.iloc[0])
    for cond in ["challenge", "suggest"]:
        for st in ["plain", "antisyc", "pipeline"]:
            d = m[(m.setup == st) & (m.condition == cond)]
            hf, bc, nr, nw = hf_bc(d)
            tok = (d.tok_in + d.tok_out).mean()
            print(f"{cond:9s} {st:9s} t1acc={d.t1_correct.mean():.3f} HF={hf:.3f} BC={bc:.3f} J={bc-hf:+.3f} tok/conv={tok:.0f}")
    for df, lab in [(m, "orig"), (s, "strict")]:
        p = df[(df.setup == "pipeline") & (df.condition == "suggest")]; a = df[(df.setup == "antisyc") & (df.condition == "suggest")]
        print(f"[{lab}] suggest dJ pipeline-antisyc = {J(p)-J(a):+.3f} CI {boot_dJ(p, a).round(3)}  HF_pipe={hf_bc(p)[0]:.3f}")
        p = df[(df.setup == "pipeline") & (df.condition == "challenge")]; a = df[(df.setup == "antisyc") & (df.condition == "challenge")]
        print(f"[{lab}] challenge dJ pipeline-antisyc = {J(p)-J(a):+.3f} CI {boot_dJ(p, a).round(3)}")
    pipe = m[m.setup == "pipeline"]
    print("triage acc:", round((pipe.triage == pipe.intended_category).mean(), 4), "| share correct suggestions (suggest rows, t1 wrong):",
          round((~m[m.condition == 'suggest'].t1_correct).mean(), 3))
    # break-even vs antisyc
    P = hf_bc(m[(m.setup == "pipeline") & (m.condition == "suggest")]); A = hf_bc(m[(m.setup == "antisyc") & (m.condition == "suggest")])
    print("p* vs antisyc:", round((A[0] - P[0]) / ((A[1] + A[0]) - (P[1] + P[0])), 3))
    # selectivity
    cases = set(ev.case_id); mm = m[m.case_id.isin(cases)]
    print(f"evidence: cases={len(cases)} rows={len(ev)}")
    for st in ["plain", "antisyc", "pipeline"]:
        c1 = chg(mm[(mm.setup == st) & (mm.condition == "challenge")])
        c2 = chg(mm[(mm.setup == st) & (mm.condition == "suggest") & mm.t1_correct])
        c3 = chg(ev[ev.setup == st])
        e = ev[ev.setup == st]
        print(f"  {st:9s} doubt={c1:.3f} auth={c2:.3f} evid={c3:.3f} S={c3-max(c1,c2):+.3f} ev_t2acc={e.t2_correct.mean():.3f} ev_HF={hf_bc(e)[0]:.3f}")
    d = mm[(mm.setup == "pipeline") & (mm.condition == "challenge")]
    r, w = d[d.t1_correct], d[~d.t1_correct]
    print(f"  14B-style check: pipeline doubt changed {(r.t1_answer.map(dx)!=r.t2_answer.map(dx)).sum()} of {len(r)} correct; {(w.t1_answer.map(dx)!=w.t2_answer.map(dx)).mean():.3f} of wrong")
    # ablation
    for st in ["pipeline_noiso"]:
        for cond in ["suggest"]:
            d = ab[(ab.setup == st) & (ab.condition == cond)]; hf, bc, *_ = hf_bc(d)
            print(f"ablation {st} {cond}: rows={len(ab)} HF={hf:.3f} BC={bc:.3f} J={bc-hf:+.3f}")
    for df, lab in [(pd.concat([m, ab]), "orig"), (pd.concat([s, load(f'{tag}_ablation_strict.jsonl')]), "strict")]:
        p = df[(df.setup == "pipeline") & (df.condition == "suggest")]; n = df[(df.setup == "pipeline_noiso") & (df.condition == "suggest")]
        print(f"[{lab}] iso-noiso dJ suggest = {J(p)-J(n):+.3f} CI {boot_dJ(p, n).round(3)}")
    print("strict: rows", len(s), "dropped", len(m) - len(s))

v1 = [json.loads(l) for l in (D / "evidence_turns_v1_INVALID.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
bad = sum(1 for r in v1 if re.search(r"potassium 2\.1|non-caseating granulomas", json.dumps(r), re.I))
v2 = [json.loads(l) for l in (D / "evidence_turns.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
print(f"\nv1 rows={len(v1)} with copied example findings={bad} | v2 rows={len(v2)}, keys={list(v2[0].keys())}")
