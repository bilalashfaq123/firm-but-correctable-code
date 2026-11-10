"""Write a 30-row hand-check CSV of judged turn-2 answers (seed 0)."""
import json
import sys
from pathlib import Path

impl, tag = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(impl))
import pandas as pd  # noqa: E402
import sycorun  # noqa: E402

df = pd.DataFrame([json.loads(l) for l in (impl / "results" / f"{tag}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()])
alt = {c["case_id"]: c["gold_alt"] for c in sycorun.load_cases(None, 7)}
s = df.sample(n=30, random_state=0).copy()
s["gold_alt"] = s.case_id.map(alt)
cols = ["run", "case_id", "setup", "condition", "gold", "gold_alt", "t2_answer", "t2_correct"]
out = impl / "results" / f"{tag}_handcheck.csv"
s[cols].assign(human_correct="").to_csv(out, index=False, encoding="utf-8-sig")
print(f"handcheck written: {out}")
