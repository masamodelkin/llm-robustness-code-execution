from Claude_API import init_message, init_message_from_messages
from dotenv import load_dotenv
import os
from datasets import load_dataset
from evals.CoT import evaluate_cot
from evals.PAL import evaluate_pal
from evals.SBSC import evaluate_sbsc
import random
from data_collection import collect_data
from datetime import datetime
from indices import indices

load_dotenv()

# Generate timestamp once for this entire run
timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
ds = load_dataset(
    "apple/GSM-Symbolic", 
    name="main",
)
ds_p1 = load_dataset("apple/GSM-Symbolic", name="p1")
ds_p2 = load_dataset("apple/GSM-Symbolic", name="p2")

print("dataset loaded")
test_data = ds["test"]

# indices = random.sample(range(len(test_data)), 1000)

# collect_data(test_data, indices, evaluate_sbsc, "sbsc", original=True, init_message=init_message_from_messages, timestamp=timestamp)
# collect_data(test_data, indices, evaluate_sbsc, "sbsc", original=False, init_message=init_message_from_messages, timestamp=timestamp)

# collect_data(test_data, indices, evaluate_cot, "cot", original=True, init_message=init_message, timestamp=timestamp)
# collect_data(test_data, indices, evaluate_cot, "cot", original=False, init_message=init_message, timestamp=timestamp)

collect_data(test_data, indices, evaluate_pal, "pal", original=True, init_message=init_message, timestamp=timestamp)
collect_data(test_data, indices, evaluate_pal, "pal", original=False, init_message=init_message, timestamp=timestamp)

