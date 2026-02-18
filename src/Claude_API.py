import anthropic
import os
from dotenv import load_dotenv

# MODEL = "claude-3-haiku-20240307"
MODEL = "claude-haiku-4-5-20251001"

load_dotenv()
client = anthropic.Anthropic()


def init_message_from_messages(messages: list, system_prompt: str = "", stop_sequences: list = []):
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=0,
        system=system_prompt,
        messages=messages,
        stop_sequences=stop_sequences
    )
    
    content_block = message.content[0]
    if content_block.type == "text":
        return message, content_block.text
    return message, ""


def init_message(user_prompt: str, 
                 system_prompt: str = "As an expert problem solver, solve step by step the following mathematical questions. Follow the format in the examples provided.",
                 prefill: str = ""):
    messages = [
        {"role": "user", 
        "content": user_prompt},
        {"role": "assistant", 
        "content": prefill}
    ]
    return init_message_from_messages(messages, system_prompt)
    # message = client.messages.create(
    #     model=MODEL,
    #     max_tokens=1024,
    #     temperature=0,
    #     system=system_prompt,
    #     messages=messages,
    # )

    # content_block = message.content[0]
    # if content_block.type == "text":
    #     return message, content_block.text
    # else:
    #     return message, ""