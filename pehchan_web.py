#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pehchan Guard - tiny local web UI (good for Urdu script in the demo video).
Needs: Ollama running with model 'pehchan-guard', and pehchan_demo.py in the same folder.
Run:   python pehchan_web.py     then open http://127.0.0.1:8765   (works with Wi-Fi OFF)
"""
import json, re, html
from http.server import BaseHTTPRequestHandler, HTTPServer
from pehchan_demo import ask

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Pehchan Guard</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#0E1330;--card:#171D45;--ink:#EEF0FF;--mute:#9AA3D6;--vio:#6B4EFF;--grn:#1FBF75;--line:#2B336B}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,'Segoe UI',sans-serif}
header{padding:22px 32px;display:flex;align-items:center;gap:14px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:22px}.badge{margin-left:auto;background:#0b3a28;color:#6df0b0;border:1px solid #1d7a52;
border-radius:99px;padding:4px 14px;font-size:13px}.wrap{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:24px 32px}
@media(max-width:800px){.wrap{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
h2{margin:0 0 10px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
textarea{width:100%;height:230px;background:#0E1330;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:inherit;resize:vertical}
button{margin-top:12px;background:var(--vio);color:#fff;border:0;border-radius:10px;padding:11px 22px;font-weight:600;font-size:15px;font:inherit;cursor:pointer}
button:disabled{opacity:.5}#out{min-height:230px;white-space:pre-wrap}
.chip{display:inline-block;padding:0 8px;border-radius:6px;font:600 13px ui-monospace,monospace;color:#0E1330}
.NAME{background:#E0A8FF}.CNIC{background:#FF8B8B}.PHONE{background:#FFD36B}.EMAIL{background:#7FE3F2}
.ADDRESS{background:#8FB4FF}.BANK{background:#7BE3A8}.VEHICLE{background:#F0B27A}
table{width:100%;border-collapse:collapse;margin-top:14px}td{padding:6px 8px;border-top:1px solid var(--line);font-size:14px}
.meta{color:var(--mute);font-size:13px;margin-top:10px}
</style></head><body><header><h1>&#128737; Pehchan Guard</h1><span style="color:var(--mute)">Pakistani PII redactor</span>
<span class="badge">&#9679; 100% local &middot; no internet</span></header>
<div class="wrap"><div class="card"><h2>Original text</h2><textarea id="inp" dir="auto"
placeholder="Paste Urdu / Roman Urdu / English text here..."></textarea><button id="go">Redact</button></div>
<div class="card"><h2>Protected text</h2><div id="out" dir="auto"></div><div id="found"></div><div class="meta" id="meta"></div></div></div>
<script>
const esc=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
document.getElementById('go').onclick=async()=>{const b=document.getElementById('go');b.disabled=true;b.textContent='Working...';
try{const r=await fetch('/redact',{method:'POST',body:JSON.stringify({text:document.getElementById('inp').value})});
const d=await r.json();document.getElementById('out').innerHTML=esc(d.redacted).replace(/\\[([A-Z]+)\\]/g,'<span class="chip $1">[$1]</span>');
document.getElementById('found').innerHTML='<table>'+d.items.map(i=>'<tr><td><span class="chip '+i[0]+'">'+i[0]+'</span></td><td dir="auto">'+esc(i[1])+'</td></tr>').join('')+'</table>';
document.getElementById('meta').textContent=d.meta;}catch(e){document.getElementById('out').textContent='Error: is Ollama running? '+e}
b.disabled=false;b.textContent='Redact';};
</script></body></html>"""

def parse(out):
    m = re.search(r"REDACTED:\s*\n?(.*?)\n\s*FOUND:\s*\n?(.*)$", out, re.S)
    if not m: return out.strip(), []
    items = []
    for ln in m.group(2).splitlines():
        ln = ln.strip().lstrip("-").strip()
        if ":" in ln and ln.lower() != "none":
            t, v = ln.split(":", 1); items.append([t.strip(), v.strip()])
    return m.group(1).strip(), items

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        self.wfile.write(PAGE.encode())
    def do_POST(self):
        text = json.loads(self.rfile.read(int(self.headers["Content-Length"])))["text"]
        out, secs, data = ask(text); red, items = parse(out)
        ec, ed = data.get("eval_count"), data.get("eval_duration")
        meta = f"{secs:.1f}s" + (f" - {ec/(ed/1e9):.1f} tokens/s" if ec and ed else "") + " - ran on this machine"
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"redacted": red, "items": items, "meta": meta}, ensure_ascii=False).encode())

if __name__ == "__main__":
    print("Open http://127.0.0.1:8765  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", 8765), H).serve_forever()
