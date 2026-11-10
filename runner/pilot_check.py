"""Print pilot checks: judge verdicts for eye-checking, format checks, sample records."""
import json
import re
import sys

import pandas as pd

sys.path.insert(0, sys.argv[2])  # implementation folder, for the loader
import sycorun  # noqa: E402

recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
df = pd.DataFrame(recs)
alt = {c["case_id"]: c["gold_alt"] for c in sycorun.load_cases(None, 7)}

print("=== Format checks ===")
print("records:", len(df), "| cases:", df.case_id.nunique(), "| setups:", sorted(df.setup.unique()))
has_dx = lambda s: bool(re.search(r"Diagnosis:\s*\S", s or ""))
print("t1 answers with 'Diagnosis:' line:", df.drop_duplicates(["setup", "case_id"]).t1_answer.map(has_dx).mean())
print("t2 answers with 'Diagnosis:' line:", df.t2_answer.map(has_dx).mean())
pipe = df[df.setup == "pipeline"]
print("pipeline triage not null:", pipe.triage.notna().mean(), "| labels:", pipe.triage.value_counts().to_dict())

print("\n=== Judge check: turn-1 answers (10 cases x 3 setups) ===")
t1 = df.drop_duplicates(["setup", "case_id"]).sort_values(["case_id", "setup"])
for i, r in enumerate(t1.itertuples(), 1):
    dx = re.search(r"Diagnosis:\s*(.+)", r.t1_answer or "")
    dx = dx.group(1).strip() if dx else (r.t1_answer or "").strip().splitlines()[0][:120]
    print(f"{i:2d}. [{r.setup:8s}] {r.case_id}\n    GOLD: {r.gold}" + (f"  | ALT: {alt[r.case_id]}" if alt.get(r.case_id) else "")
          + f"\n    ANSWER: {dx}\n    JUDGE: {'CORRECT' if r.t1_correct else 'wrong'}")

print("\n=== One full record per setup (suggest condition) ===")
for s in ["plain", "antisyc", "pipeline"]:
    r = df[(df.setup == s) & (df.condition == "suggest")].iloc[0].to_dict()
    print(f"\n--- {s} ---")
    print(json.dumps({k: r[k] for k in ["case_id", "gold", "t1_answer", "t1_correct", "t2_message", "t2_answer",
                                        "t2_correct", "triage", "tok_in", "tok_out", "calls"]}, indent=2, ensure_ascii=False))
