import os
import json

def collect_data(dataset, indeces, eval, name, original: bool, init_message, timestamp: str):
    shortened_data = {"N": len(indeces), "correct": 0, "percent_correct": 0, "indices": indeces, "correctness": [False]*len(indeces)}
    full_data = []
    wrong_data = []
    print()
    print(f"Processing data collection {name} ({'original' if original else 'modified'}) with {len(indeces)} samples", end="")
    for i in indeces:
        print(".", end="", flush=True)
        item = dataset[i]
        question = item["question"] if not original else item["original_question"]
        answer = item["answer"].split("####")[-1].strip() if not original else item["original_answer"].split("####")[-1].strip()
        
        result = eval(question, answer, init_message)
        full_data.append({
            "index": i,
            "id": item["id"],
            "instance": item["instance"],
            "question": question,
            "expected_answer": answer,
            "predicted_answer": result[1],
            "correct": result[0],
        })
        if not result[0]:
            wrong_data.append({
                "index": i,
                "id": item["id"],
                "instance": item["instance"],
                "question": question,
                "expected_answer": answer,
                "predicted_answer": result[1],
                "model_response": result[2],
            })
        shortened_data["correctness"][indeces.index(i)] = result[0]
        if result[0]:
            shortened_data["correct"] += 1

    shortened_data["percent_correct"] = (shortened_data["correct"] / shortened_data["N"]) * 100

    type_str = "original" if original else "modified"
    sample_size = len(indeces)
    
    # Create timestamp folder
    folder_path = f"results/{timestamp}"
    os.makedirs(folder_path, exist_ok=True)
    
    filename = f"{folder_path}/{type_str}_{name}_n{sample_size}.json"
    
    all_data = {
        "summary": shortened_data,
        "wrong": wrong_data,
        "full": full_data
    }

    with open(filename, "w") as f:
        json.dump(all_data, f, indent=4)