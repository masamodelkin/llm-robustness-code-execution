import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Load all 6 datasets: {original, modified} × {cot, pal, sbsc}
with open(DATA_DIR / "original_cot_n1000.json") as f:
    original_cot = json.load(f)

with open(DATA_DIR / "modified_cot_n1000.json") as f:
    modified_cot = json.load(f)

with open(DATA_DIR / "original_pal_n1000.json") as f:
    original_pal = json.load(f)

with open(DATA_DIR / "modified_pal_n1000.json") as f:
    modified_pal = json.load(f)

with open(DATA_DIR / "original_sbsc_n1000.json") as f:
    original_sbsc = json.load(f)

with open(DATA_DIR / "modified_sbsc_n1000.json") as f:
    modified_sbsc = json.load(f)

results = {
    "percentage":{
        "cot": (round(original_cot["summary"]["percent_correct"], 1), round(modified_cot["summary"]["percent_correct"], 1)),
        "pal": (round(original_pal["summary"]["percent_correct"], 1), round(modified_pal["summary"]["percent_correct"], 1)),
        "sbsc": (round(original_sbsc["summary"]["percent_correct"], 1), round(modified_sbsc["summary"]["percent_correct"], 1))
    },
    "percentage_drop": {
        "cot": round(original_cot["summary"]["percent_correct"] - modified_cot["summary"]["percent_correct"], 1),
        "pal": round(original_pal["summary"]["percent_correct"] - modified_pal["summary"]["percent_correct"], 1),
        "sbsc": round(original_sbsc["summary"]["percent_correct"] - modified_sbsc["summary"]["percent_correct"], 1),
    },
    "robustness": {
        "cot": {"broke": 0, "fixed": 0, "stayed": 0},
        "pal": {"broke": 0, "fixed": 0, "stayed": 0},
        "sbsc": {"broke": 0, "fixed": 0, "stayed": 0},
        "voting": {"broke": 0, "fixed": 0, "stayed": 0}
    },
    "stats_data": {
        "cot": {
            "original": {"right": original_cot["summary"]["correct"], "wrong": original_cot["summary"]["N"] - original_cot["summary"]["correct"]},
            "modified": {"right": modified_cot["summary"]["correct"], "wrong": modified_cot["summary"]["N"] - modified_cot["summary"]["correct"]}
        },
        "pal": {
            "original": {"right": original_pal["summary"]["correct"], "wrong": original_pal["summary"]["N"] - original_pal["summary"]["correct"]}, 
            "modified": {"right": modified_pal["summary"]["correct"], "wrong": modified_pal["summary"]["N"] - modified_pal["summary"]["correct"]}
        },
        "sbsc": {
            "original": {"right": original_sbsc["summary"]["correct"], "wrong": original_sbsc["summary"]["N"] - original_sbsc["summary"]["correct"]}, 
            "modified": {"right": modified_sbsc["summary"]["correct"], "wrong": modified_sbsc["summary"]["N"] - modified_sbsc["summary"]["correct"]}
        }
    },
    "wrong questions": {}
}


# Create a voting ensemble result for each question
original_voting = {"summary": {"correctness": []}}
modified_voting = {"summary": {"correctness": []}}
for i in range(len(original_cot["full"])):
    original_correctness = [original_cot["full"][i]["correct"], 
                      original_pal["full"][i]["correct"], 
                      original_sbsc["full"][i]["correct"]]
    modified_correctness = [modified_cot["full"][i]["correct"], 
                      modified_pal["full"][i]["correct"], 
                      modified_sbsc["full"][i]["correct"]]

    original_voting["summary"]["correctness"].append(original_correctness.count(True) >= 2)  # Majority vote
    modified_voting["summary"]["correctness"].append(modified_correctness.count(True) >= 2)  # Majority vote

def update_robustness(original_data, modified_data, method):
    for i in range(len(original_data["summary"]["correctness"])):
        original_correct = original_data["summary"]["correctness"][i]
        modified_correct = modified_data["summary"]["correctness"][i]
        if original_correct and not modified_correct:
            results["robustness"][method]["broke"] += 1
        elif not original_correct and modified_correct:
            results["robustness"][method]["fixed"] += 1
        else:
            results["robustness"][method]["stayed"] += 1


update_robustness(original_cot, modified_cot, "cot")
update_robustness(original_pal, modified_pal, "pal")
update_robustness(original_sbsc, modified_sbsc, "sbsc")
update_robustness(original_voting, modified_voting, "voting")

def add_wrong_questions(data, method, original):
    for i in data["wrong"]:
        if i["id"] not in results["wrong questions"]:
            results["wrong questions"][i["id"]] = {
                "original": {
                    "question": i["question"],
                    "expected_answer": i["expected_answer"] if original else None,
                    "total_count": 0,
                    "wrong_count": 0,
                    "cot_count": 0,
                    "pal_count": 0,
                    "sbsc_count": 0,
                    "cot": [],
                    "pal": [],
                    "sbsc": []
                },
                "modified": {
                    "total_count": 0,
                    "wrong_count": 0,
                    "cot": 0,
                    "pal": 0,
                    "sbsc": 0
                }
            }
        results["wrong questions"][i["id"]]["original" if original else "modified"]["wrong_count"] += 1
        if original:
            results["wrong questions"][i["id"]]["original"][method].append(i["predicted_answer"])
            results["wrong questions"][i["id"]]["original"]["expected_answer"] = i["expected_answer"]
            results["wrong questions"][i["id"]]["original"]["question"] = i["question"]
            results["wrong questions"][i["id"]]["original"][method + "_count"] += 1
        else:
            results["wrong questions"][i["id"]]["modified"][method] += 1

add_wrong_questions(original_cot, "cot", True)
add_wrong_questions(original_pal, "pal", True)
add_wrong_questions(original_sbsc, "sbsc", True)
add_wrong_questions(modified_cot, "cot", False)
add_wrong_questions(modified_pal, "pal", False)
add_wrong_questions(modified_sbsc, "sbsc", False)

# Calculate total counts for each question that at least one method got wrong
for i in original_cot["full"]:
    qid = i["id"]
    if qid in results["wrong questions"]:
        results["wrong questions"][qid]["original"]["total_count"] += 1
        results["wrong questions"][qid]["modified"]["total_count"] += 1


# Save results to a JSON file
with open(Path(__file__).parent / "analysis_results.json", "w") as f:
    json.dump(results, f, indent=4)