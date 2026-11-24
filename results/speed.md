# Pehchan Guard — local run measurements (24 Nov 2026)

Model: `pehchan-guard-q4_k_m.gguf` (GGUF Q4_K_M, 1,107,409,312 bytes = 1.03 GiB, md5 `2ae5eb42434563de8e6bb93693bbf163`)
Runtime: Ollama 0.40.17 (llama.cpp), context 2048, temperature 0.

## Hardware

Measured on a shared cloud VM, stated honestly because it is weaker than a normal laptop:

- CPU: AMD EPYC, shared and throttled (≈1.5 vCPU visible to this VM), no GPU
- RAM: 7 GB total
- OS: Linux

## Speed

Median over 5 prompts (English, Roman Urdu, Urdu script, mixed, and one clean prompt):

- **6.5 tokens/sec median** (range 6.3–6.8 tok/s on this throttled shared CPU)

A typical modern laptop CPU (4+ full cores) will run this noticeably faster. The point proven here: the model runs end-to-end, fully offline, on CPU alone.

## Memory

- llama-server process RSS while loaded: ≈1.44 GiB (model 1.03 GiB + context/runtime)
- Ollama serve process: ≈20 MB

## Quantization cross-check (local GGUF vs Colab model)

Same first 20 held-out test examples, same scorer:

| Run | F1 | Exact match | Leaked items |
| --- | --- | --- | --- |
| Colab (Unsloth, 4-bit base + LoRA) | 0.970 | 0.90 | 1 |
| Local Ollama (GGUF Q4_K_M) | 0.970 | 0.90 | 1 |

Identical scores — the GGUF conversion and quantization cost nothing on this sample.
The two demo prompts (English courier example, Urdu salary example) also reproduce the Colab outputs exactly, including the title "صاحب" correctly left outside the name span.
