---
license: apache-2.0
base_model: Qwen/Qwen3-1.7B
language:
  - ur
  - en
tags:
  - pii
  - redaction
  - privacy
  - urdu
  - gguf
  - ollama
  - qwen3
  - lora
pipeline_tag: text-generation
---

# Pehchan Guard — Pakistani PII redactor (Qwen3-1.7B LoRA, GGUF Q4_K_M)

Pehchan Guard removes personal details from Pakistani text — Urdu script, Roman Urdu, and English — and runs **100% offline** on a normal laptop. Paste text in; get the same text back with every personal detail replaced by a label, plus a list of what was found.

It redacts 7 types: **names, CNIC numbers, phone numbers, email addresses, home addresses, bank account numbers / IBANs, and vehicle registration numbers**.

Built for the Qwen Local Hackathon 2026 (Qwen Pakistan). Code, data generator, scorer and demos: https://github.com/Daimx1214/pehchan-guard

## Why

People paste text full of names, CNIC numbers and phone numbers into online tools every day. A cloud redactor sees the private data first, which defeats the purpose. A regex script is not enough either: on our held-out test set it scores F1 0.615 and finds **zero** names and **zero** addresses — exactly the riskiest items in Urdu and Roman Urdu text. The base Qwen3-1.7B, asked zero-shot, scores F1 0.008. So this needed a fine-tune, and it needed to run locally.

## Results (held-out test set, n=400, 1,267 personal items)

Scored with a strict automatic scorer: an item counts only if it is listed in the FOUND list with the right label **and** no longer appears in the redacted text. A listed-but-not-removed item counts as a leak.

| Model | Overall F1 | Exact match | Leaked items | Clean text wrongly changed |
| --- | --- | --- | --- | --- |
| Regex only | 0.615 | 8.7% | 686 | 0% |
| Qwen3-1.7B base (zero-shot) | 0.008 | 1.3% | 486 | 84% |
| **Pehchan Guard** | **0.970** | **89.2%** | **5** | **0%** |

Per-type F1 (Pehchan Guard): CNIC 0.996 · PHONE 0.991 · EMAIL 0.995 · ADDRESS 1.000 · VEHICLE 1.000 · BANK 0.984 · NAME 0.940.

On a separate **60-example hand-written hard set** (messy real-style text: typos, strange spacing like `35202 1234567 1`, titles such as Dr. and Chaudhry, names that are also common words), Pehchan Guard scores **F1 0.883** with **zero leaked items** (base model: 0.000). Names are the weakest type there (F1 0.831). The full failure list is published in the project repo (`results/failures.md`) — we report it rather than hide it.

## Run it locally

```bash
# Download pehchan-guard-q4_k_m.gguf (this repo) and the Modelfile from the project repo
ollama create pehchan-guard -f Modelfile
ollama run pehchan-guard "Mera naam Ali Raza hai, mera CNIC 35202-1234567-1 hai, number 0300-1234567"
```

- Runtime: Ollama (llama.cpp), quantization GGUF Q4_K_M, file size 1.03 GiB
- Hardware tested: AMD EPYC shared cloud VM (≈1.5 throttled vCPU, CPU-only, 7 GB RAM, Linux) with Ollama 0.40.17 — **6.5 tokens/sec median** over 5 prompts and ≈1.44 GiB RAM while loaded. This VM is deliberately stated as-is: it is weaker than a normal laptop, and a typical modern laptop CPU runs the model noticeably faster. Local GGUF scores match the Colab model exactly on a 20-example cross-check (F1 0.970 both).
- Context 2048, temperature 0. Nothing in the pipeline makes a network call.

## Data

100% synthetic — no real person's data anywhere. A generator script in the project repo builds examples from name/area/city lists and sentence templates with format-correct random values (real CNIC structure, Pakistani mobile/landline patterns, IBANs with valid check digits). 3,200 train / 400 validation / 400 held-out test; every fifth name, area and city and every fourth template is test-only and never appears in training (verified: zero train/test input overlap). Language mix ≈ 40% English, 35% Roman Urdu, 25% Urdu script; ~1 in 10 examples is clean text, so the model learns to leave clean text alone.

## Training

LoRA (QLoRA) on `Qwen/Qwen3-1.7B` with Unsloth + TRL: r=16, alpha=32, all linear layers, loss on responses only, thinking mode off, max length 1536, batch 8 × grad-accum 2, 3 epochs, lr 2e-4. Trained on a free Google Colab T4 in 29.5 minutes (peak GPU memory 5.9 GB). One system prompt and one output format are used in training, scoring, the Modelfile and the demos — what is measured is what ships.

## Limits

- Synthetic training data is cleaner than real text; the hard-set score (0.883) is the more honest estimate for messy input.
- Names with titles, names that double as common words, and broken spacing are the main remaining errors.
- It redacts the 7 listed types only. Company names, order numbers, amounts and dates are intentionally left unchanged.
- Always review the output before sharing redacted text — no redactor is perfect, and 5 of 1,267 test items still leaked.

## Credits

Base model Qwen3 (Alibaba, Apache-2.0). Fine-tune, data generator, scorer and demos by Daim Ali for the Qwen Local Hackathon 2026.
