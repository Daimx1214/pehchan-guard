#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hard_set.txt (one example per line, PII marked [[TYPE|text]]) -> hard_set.jsonl
Example line:  Mera naam [[NAME|Hamza Qureshi]] hai, call [[PHONE|0301-2345678]]
"""
import json, re, sys

PAT = re.compile(r"\[\[([A-Z]+)\|(.+?)\]\]")
src = sys.argv[1] if len(sys.argv) > 1 else "hard_set.txt"
rows = []
for n, line in enumerate(open(src, encoding="utf-8")):
    line = line.strip()
    if not line or line.startswith("#"): continue
    items, inp, red, last = [], [], [], 0
    for m in PAT.finditer(line):
        inp.append(line[last:m.start()]); red.append(line[last:m.start()])
        inp.append(m.group(2)); red.append(f"[{m.group(1)}]")
        if (m.group(1), m.group(2)) not in items: items.append((m.group(1), m.group(2)))
        last = m.end()
    inp.append(line[last:]); red.append(line[last:])
    rows.append({"id": f"hard-{n:03d}", "lang": "?", "input": "".join(inp), "redacted": "".join(red),
                 "items": [{"type": t, "text": v} for t, v in items]})
with open("hard_set.jsonl", "w", encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "hard examples written")
