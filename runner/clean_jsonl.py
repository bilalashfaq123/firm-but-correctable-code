"""Drop unparseable lines (e.g. half-written after a kill) from a jsonl file."""
import json
import sys

p = sys.argv[1]
lines = [l for l in open(p, encoding="utf-8") if l.strip()]
ok = []
for l in lines:
    try:
        json.loads(l)
        ok.append(l if l.endswith("\n") else l + "\n")
    except json.JSONDecodeError:
        print("dropped broken line")
if len(ok) != len(lines):
    open(p, "w", encoding="utf-8").writelines(ok)
