from prompts.SBSC import build_sbsc_prompt, SBSC_SYSTEM_PROMPT
import re
import io
import sys

def extract_code(response_text):
    # Extract code between ```python and ``` or ``` and ```
    match = re.search(r"```python\s*(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    match = re.search(r"```\s*(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return None

def execute_code(code):
    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        exec(code, {"__builtins__": __builtins__})
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        return output.strip() if output.strip() else "Code executed successfully.", None
    except Exception as e:
        sys.stdout = old_stdout
        return None, str(e)

def extract_final_answer(response_text):
    # "The final answer is X"
    match = re.search(r"The final answer is.*?(\-?[0-9,]+\.?[0-9]*)", response_text)
    if match:
        return match.group(1).replace(",", "")
    
    # "boxed{X}"
    match = re.search(r"boxed\{(\-?[0-9,]+\.?[0-9]*)\}", response_text)
    if match:
        return match.group(1).replace(",", "")
    
    # Fallback: last number in response
    numbers = re.findall(r"\-?[0-9,]+\.?[0-9]*", response_text)
    numbers = [n for n in numbers if n]
    if numbers:
        return numbers[-1].replace(",", "")
    
    return None

def evaluate_sbsc(problem: str, answer: str, init_message_from_messages, max_turns=15):
    system_prompt, user_prompt = build_sbsc_prompt(problem)
    
    messages = [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": "\nStep 1:"}
    ]
    
    # full_trajectory = []
    predicted_answer = None
    
    for turn in range(max_turns):
        # Get model response
        message, response = init_message_from_messages(
            messages=messages,
            system_prompt=system_prompt,
            stop_sequences=["```output", "```\noutput"]
        )
        
        # full_trajectory.append({"role": "assistant", "content": response})
        messages.append({"role": "assistant", "content": response})
        
        # Check if done
        if "###END OF CODE" in response:
            # Execute the final code to get actual output
            code = extract_code(response)
            if code:
                output, error = execute_code(code)
                if output and not error:
                    predicted_answer = extract_final_answer(output)
            
            # If no code in this response, check the last user message for output
            if predicted_answer is None:
                for msg in reversed(messages):
                    if msg["role"] == "user" and ">>> output" in msg["content"]:
                        output = msg["content"].replace(">>> output\n", "")
                        predicted_answer = extract_final_answer(output)
                        break

            # Fallback to response text if execution failed
            if predicted_answer is None:
                predicted_answer = extract_final_answer(response)
            break
        
        # Extract and execute code
        code = extract_code(response)
        if code:
            output, error = execute_code(code)
            if error:
                user_msg = f">>> output\nError: {error}"
            else:
                user_msg = f">>> output\n{output}"
        else:
            user_msg = ">>> output\nNo code found. Please provide a code snippet."
        
        # full_trajectory.append({"role": "user", "content": user_msg})
        messages.append({"role": "user", "content": user_msg})
    
    # print("Full interaction:")
    # for msg in messages:
    #     print(f"{msg['role']}: {msg['content']}")

    if predicted_answer is None:
        return False, None, messages, "No answer extracted or max turns reached"
    
    try:
        correct = abs(float(answer) - float(predicted_answer)) < 0.001
    except (ValueError, TypeError):
        correct = False
    
    # print(f"Predicted answer: {predicted_answer}, Correct: {correct}")
    return correct, predicted_answer, messages, None