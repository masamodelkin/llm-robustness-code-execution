from dotenv import load_dotenv
import anthropic
import os
from datasets import load_dataset
from prompts.PAL import build_pal_prompt
from prompts.CoT import build_cot_prompt

ds = load_dataset(
    "apple/GSM-Symbolic", 
    name="main",
    cache_dir="./cache"
)
print("dataset loaded")
test_data = ds["test"]

load_dotenv()
client = anthropic.Anthropic()
item = test_data[0]

original_q = item["original_question"]
original_a = item["original_answer"].split("####")[-1].strip()
print(test_data[0]["original_question"] == test_data[1]["original_question"])
print()
print("prompt:", build_cot_prompt(original_q))
print()
print("expected answer:", original_a)
print()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0,
    system="Answer in the same format as the examples below.",
    messages=[
        {"role": "user", 
         "content": build_cot_prompt(original_q)},
        {"role": "assistant", 
         "content": "Let's think step by step."}
    ],
)

print(message.content)