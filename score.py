#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pehchan Guard scorer.
Usage: python score.py --gold data/test_raw.jsonl --pred preds_base.jsonl [--name base] [--save results/score_base.json]
 gold rows: {"id","input","redacted","items":[{"type","text"}]}
 pred rows: {"id","prediction"}   (prediction = raw model text)
An item counts as correct only if the model lists it in FOUND with the right
label AND the original text no longer appears in the redacted output (no leak).
"""
import json, re, argparse, collections

TYPES = ["NAME","CNIC","PHONE","EMAIL","ADDRESS","BANK","VEHICLE"]

def parse(pred):
    """-> (redacted_text or None, set of (TYPE, text))"""
    m = re.search(r"REDACTED:\s*\n?(.*?)\n\s*FOUND:\s*\n?(.*)$", pred, re.S)
    if not m: return None, set()
    red, found = m.group(1).strip(), m.group(2)
    items = set()
    for line in found.splitlines():
        line = line.strip()
        if not line.startswith("-"): continue
        body = line[1:].strip()
        if body.lower() == "none" or ":" not in body: continue
        t, v = body.split(":", 1)
        t = t.strip().upper()
        if t in TYPES and v.strip(): items.add((t, v.strip()))
    return red, items

def score(gold_rows, pred_rows):
    preds = {p["id"]: p["prediction"] for p in pred_rows}
    tp, fp, fn = (collections.Counter() for _ in range(3))
    n = len(gold_rows); parse_fail = exact = leaks = 0
    clean_n = clean_bad = 0
    for g in gold_rows:
        red, items = parse(preds.get(g["id"], ""))
        gold = {(i["type"], i["text"]) for i in g["items"]}
        if red is None: parse_fail += 1
        if red is not None and red == g["redacted"].strip(): exact += 1
        for t, v in gold:
            ok = (t, v) in items and red is not None and v not in red
            if ok: tp[t] += 1
            else:
                fn[t] += 1
                if red is not None and v in red: leaks += 1
        for t, v in items:
            if (t, v) not in gold: fp[t] += 1
        if not gold:
            clean_n += 1
            if red is None or red != g["input"].strip() or items: clean_bad += 1
    def prf(a, b, c):
        p = a / (a + b) if a + b else 0.0; r = a / (a + c) if a + c else 0.0
        return p, r, (2 * p * r / (p + r) if p + r else 0.0)
    out = {"n": n, "parse_fail_rate": parse_fail / n, "exact_match": exact / n,
           "leaked_items": leaks, "clean_false_redaction_rate": (clean_bad / clean_n if clean_n else None),
           "per_type": {}}
    for t in TYPES:
        p, r, f = prf(tp[t], fp[t], fn[t]); out["per_type"][t] = dict(p=p, r=r, f1=f, tp=tp[t], fp=fp[t], fn=fn[t])
    p, r, f = prf(sum(tp.values()), sum(fp.values()), sum(fn.values()))
    out["overall"] = dict(p=p, r=r, f1=f)
    return out

def show(res, name):
    print(f"\n=== {name} (n={res['n']}) ===")
    print(f"{'type':9}{'P':>7}{'R':>7}{'F1':>7}{'TP':>6}{'FP':>6}{'FN':>6}")
    for t in TYPES:
        d = res["per_type"][t]; print(f"{t:9}{d['p']:7.3f}{d['r']:7.3f}{d['f1']:7.3f}{d['tp']:6}{d['fp']:6}{d['fn']:6}")
    o = res["overall"]; print(f"{'OVERALL':9}{o['p']:7.3f}{o['r']:7.3f}{o['f1']:7.3f}")
    print(f"exact-match {res['exact_match']:.3f} | parse-fail {res['parse_fail_rate']:.3f} | leaked items {res['leaked_items']} | clean false-redaction {res['clean_false_redaction_rate']}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True); ap.add_argument("--pred", required=True)
    ap.add_argument("--name", default="model"); ap.add_argument("--save")
    a = ap.parse_args()
    gold = [json.loads(l) for l in open(a.gold, encoding="utf-8")]
    pred = [json.loads(l) for l in open(a.pred, encoding="utf-8")]
    res = score(gold, pred); show(res, a.name)
    if a.save: json.dump(res, open(a.save, "w"), indent=2)
