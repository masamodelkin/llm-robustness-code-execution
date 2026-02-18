from prompts.PAL import build_pal_prompt
import re

def extract_code(response_text):
    # Extract code between ```python and ``` or just the def solution() block
    match = re.search(r"```python\s*(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: look for def solution()
    match = re.search(r"(def solution\(\):.*?)(?=\n\n|\Z)", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return response_text  # assume whole response is code

def execute_code(code):
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        if "solution" in local_vars:
            result = local_vars["solution"]()
            return str(result), None
        return None, "No solution function found"
    except Exception as e:
        return None, str(e)

def evaluate_pal(problem: str, answer: str, init_message):
    prompt = build_pal_prompt(problem)
    _, response = init_message(
        user_prompt=prompt,
        system_prompt="",  # PAL uses no system prompt
        prefill="def solution():"
    )
    
    # Prepend the prefill since it's not in response
    full_code = "def solution():" + response
    code = extract_code(full_code)
    
    predicted_answer, error = execute_code(code)
    
    if predicted_answer is None:
        return False, None, response, error
    
    try:
        correct = abs(float(answer) - float(predicted_answer)) < 0.001
    except (ValueError, TypeError):
        correct = False
    
    return correct, predicted_answer, response, error