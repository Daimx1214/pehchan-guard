#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pehchan Guard - local demo (Ollama). No internet needed. Python 3.8+, no extra packages.
Usage:  python pehchan_demo.py                (interactive: paste text, press Enter)
        python pehchan_demo.py "text here"
"""
import json, re, sys, time, urllib.request

MODEL = "pehchan-guard"
URL = "http://localhost:11434/api/chat"
SYSTEM = ("You are Pehchan Guard. Replace every personal detail (name, CNIC, phone, email, "
    "address, bank account/IBAN, vehicle number) in the user's text with [NAME], [CNIC], "
    "[PHONE], [EMAIL], [ADDRESS], [BANK], [VEHICLE]. Output exactly: REDACTED: then the "
    "redacted text, then FOUND: then a list of '- TYPE: original text'. If there is no "
    "personal detail, copy the text unchanged and write '- none'.")
C = {"NAME":"\033[95m","CNIC":"\033[91m","PHONE":"\033[93m","EMAIL":"\033[96m",
     "ADDRESS":"\033[94m","BANK":"\033[92m","VEHICLE":"\033[33m"}
END = "\033[0m"

def ask(text):
    body = json.dumps({"model": MODEL, "stream": False,
        "options": {"temperature": 0, "num_predict": 700},
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r: data = json.loads(r.read())
    return data["message"]["content"], time.time() - t0, data

def paint(s):
    return re.sub(r"\[([A-Z]+)\]", lambda m: f"{C.get(m.group(1),'')}[{m.group(1)}]{END}", s)

def show(text):
    out, secs, data = ask(text)
    m = re.search(r"REDACTED:\s*\n?(.*?)\n\s*FOUND:\s*\n?(.*)$", out, re.S)
    print("\n--- REDACTED ---")
    print(paint(m.group(1).strip()) if m else out)
    if m:
        print("--- FOUND ---"); print(m.group(2).strip())
    ec, ed = data.get("eval_count"), data.get("eval_duration")
    tps = f"{ec/(ed/1e9):.1f} tok/s" if ec and ed else "n/a"
    print(f"\n[{secs:.1f}s total, {tps}, runs 100% locally]\n")

if __name__ == "__main__":
    if len(sys.argv) > 1: show(" ".join(sys.argv[1:]))
    else:
        print("Pehchan Guard (offline). Paste text, Enter to redact, Ctrl+C to quit.")
        while True:
            try: t = input("> ").strip()
            except (KeyboardInterrupt, EOFError): break
            if t: show(t)
