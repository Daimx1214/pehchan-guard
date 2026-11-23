#!/usr/bin/env python3
"""Regex-only baseline (no names, no addresses, no plain account numbers).
Makes preds in the same format as the model so score.py can compare:
  python baseline_regex.py data/test_raw.jsonl results/preds_regex.jsonl"""
import json, re, sys

RULES = [("CNIC", r"\b\d{5}-\d{7}-\d\b|\b\d{13}\b"),
         ("BANK", r"\bPK\d{2}(?: ?[A-Z0-9]{4}){5}\b"),
         ("EMAIL", r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
         ("PHONE", r"(?:\+92[\s-]?|\b0)3\d{2}[\s-]?\d{7}\b|\b0\d{2}-\d{7,8}\b"),
         ("VEHICLE", r"\b[A-Z]{2,3}[- ]?(?:\d{2}-)?\d{3,4}\b")]

def redact(text):
    items = []
    for label, pat in RULES:
        def sub(m):
            items.append((label, m.group(0))); return f"[{label}]"
        text = re.sub(pat, sub, text)
    seen = []; [seen.append(i) for i in items if i not in seen]
    found = "\n".join(f"- {t}: {v}" for t, v in seen) or "- none"
    return f"REDACTED:\n{text}\nFOUND:\n{found}"

if __name__ == "__main__":
    rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps({"id": r["id"], "prediction": redact(r["input"])}, ensure_ascii=False) + "\n")
