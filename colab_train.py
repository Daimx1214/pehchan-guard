# ===================== Pehchan Guard - Colab training script =====================
# Source of truth = the organizers' starter notebook (finetune-anywhere).
# Keep ITS install cell; paste these cells in place of its dataset/training cells.
# If an API name differs in the current Unsloth/TRL version, follow the notebook.
# Each "# %%" = one Colab cell. pehchan_train.ipynb is generated from this file.
#
# Files to upload into the Colab runtime first (left file panel):
#   train.jsonl, val.jsonl, test_raw.jsonl, hard_set.jsonl, score.py, system_prompt.txt
# Download EVERY output (preds, scores, adapter, GGUF) to Drive/PC immediately.

# %% CELL 1 - install (use the starter notebook's install cell instead if it differs)
# !pip install unsloth

# %% CELL 2 - load data
import json
SYSTEM = open("system_prompt.txt", encoding="utf-8").read().strip()   # same text as generate_dataset.SYSTEM
def load(path): return [json.loads(l) for l in open(path, encoding="utf-8")]
train_rows, val_rows, test_rows = load("train.jsonl"), load("val.jsonl"), load("test_raw.jsonl")
hard_rows = load("hard_set.jsonl")
print(len(train_rows), len(val_rows), len(test_rows), len(hard_rows))

# %% CELL 3 - load base model (4-bit)
from unsloth import FastLanguageModel
import torch
MAX_LEN = 1536
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-1.7B", max_seq_length=MAX_LEN, load_in_4bit=True)

# %% CELL 4 - prompt builder (identical for base eval, training, inference)
def build_prompt(text):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]
    return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                         enable_thinking=False)   # ends with empty <think></think>
def generate_all(rows, out_path, batch_size=16, max_new_tokens=512):
    FastLanguageModel.for_inference(model)
    tokenizer.padding_side = "left"
    with open(out_path, "w", encoding="utf-8") as f:
        for i in range(0, len(rows), batch_size):
            b = rows[i:i + batch_size]
            enc = tokenizer([build_prompt(r["input"]) for r in b], return_tensors="pt",
                            padding=True).to("cuda")
            gen = model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False, use_cache=True)
            for r, g in zip(b, gen):
                text = tokenizer.decode(g[enc["input_ids"].shape[1]:], skip_special_tokens=True)
                f.write(json.dumps({"id": r["id"], "prediction": text}, ensure_ascii=False) + "\n")
    print("wrote", out_path)

# %% CELL 5 - BASE MODEL "before" numbers (do this FIRST, in a fresh runtime, before any training)
generate_all(test_rows, "preds_base.jsonl")
generate_all(hard_rows, "hard_base.jsonl")
# !python score.py --gold test_raw.jsonl --pred preds_base.jsonl --name base --save score_base.json
# !python score.py --gold hard_set.jsonl --pred hard_base.jsonl --name hard-base --save score_hard_base.json
# Download preds_base.jsonl, hard_base.jsonl, score_base.json, score_hard_base.json NOW.
# ---------------- everything below = TRAINING runtime (restart runtime first) ----------------

# %% CELL 6 - add LoRA
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32, lora_dropout=0, bias="none",
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    use_gradient_checkpointing="unsloth", random_state=3407)

# %% CELL 7 - build training text (prompt + answer + <|im_end|>)
from datasets import Dataset
def to_text(row):
    msgs = row["messages"]
    prompt = build_prompt(msgs[1]["content"])
    return {"text": prompt + msgs[2]["content"] + "<|im_end|>\n"}
train_ds = Dataset.from_list(train_rows).map(to_text, remove_columns=list(train_rows[0].keys()))
val_ds = Dataset.from_list(val_rows).map(to_text, remove_columns=list(val_rows[0].keys()))
print(train_ds[0]["text"][:600])

# %% CELL 8 - train
from trl import SFTTrainer, SFTConfig
trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=train_ds, eval_dataset=val_ds,
    args=SFTConfig(
        dataset_text_field="text", max_seq_length=MAX_LEN,
        per_device_train_batch_size=8, gradient_accumulation_steps=2,
        num_train_epochs=3, learning_rate=2e-4, warmup_steps=20, lr_scheduler_type="linear",
        weight_decay=0.01, optim="adamw_8bit", logging_steps=10,
        eval_strategy="epoch", save_strategy="no", seed=3407, report_to="none",
        bf16=torch.cuda.is_bf16_supported(), fp16=not torch.cuda.is_bf16_supported()))
from unsloth.chat_templates import train_on_responses_only
trainer = train_on_responses_only(trainer,
    instruction_part="<|im_start|>user\n",
    response_part="<|im_start|>assistant\n<think>\n\n</think>\n\n")
stats = trainer.train()
print("peak GPU GB:", torch.cuda.max_memory_reserved() / 1e9, "| train secs:", stats.metrics["train_runtime"])

# %% CELL 9 - AFTER numbers on the held-out test set + hard set
generate_all(test_rows, "preds_tuned.jsonl")
generate_all(hard_rows, "hard_tuned.jsonl")
# !python score.py --gold test_raw.jsonl --pred preds_tuned.jsonl --name tuned --save score_tuned.json
# !python score.py --gold hard_set.jsonl --pred hard_tuned.jsonl --name hard --save score_hard.json

# %% CELL 10 - save adapter, merged model, GGUF Q4_K_M
model.save_pretrained("pehchan_lora"); tokenizer.save_pretrained("pehchan_lora")
model.save_pretrained_merged("pehchan_merged", tokenizer, save_method="merged_16bit")
model.save_pretrained_gguf("pehchan_gguf", tokenizer, quantization_method="q4_k_m")
# then download pehchan_gguf/*.gguf, pehchan_lora/, pehchan_merged/ (zip) to Drive/PC immediately
