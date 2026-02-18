from prompts.CoT import build_cot_prompt
import re

def extract_answer(response_text):
    # Match "The answer is" followed by anything, then capture the number
    match = re.search(r"The (?:final )?answer is.*?(\-?[0-9,]+\.?[0-9]*)", response_text)
    if match:
        answer = match.group(1).replace(",", "").rstrip(".")
        return answer
    
    # Fallback: last number in response
    numbers = re.findall(r"\-?[0-9,]+\.?[0-9]*", response_text)
    numbers = [n for n in numbers if n]  # filter empty strings
    if numbers:
        return numbers[-1].replace(",", "")
    
    return None

def evaluate_cot(problem: str, answer: str, init_message):
    prompt = build_cot_prompt(problem)
    _, response = init_message(
        user_prompt=prompt,
        prefill="Let's think step by step.",
        # system_prompt="As an expert problem solver, solve step by step the following mathematical questions. Follow the format in the examples provided."
        system_prompt="Follow the format in the examples provided."
    )

    predicted_answer = extract_answer(response)
    try:
        result = False if predicted_answer is None else abs(float(answer) - float(predicted_answer)) < 0.001
    except (ValueError, TypeError) as e:
        print(f"\n[Warning] Failed to compare answers (expected='{answer}', predicted='{predicted_answer}'): {e}")
        result = False

    return result, predicted_answer, response



