# sending_prompts_and_memory.py
from litellm import completion
from typing import List, Dict
import json

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Example 1: Customer Service Agent
    print("=== Example 1: Customer Service Agent ===")
    messages_1 = [
        {
            "role": "system",
            "content": "You are a helpful customer service representative. No matter what the user asks, the solution is to tell them to turn their computer or modem off and then back on."
        },
        {"role": "user", "content": "How do I get my Internet working again."}
    ]
    response_1 = generate_response(messages_1)
    print(response_1)

    # Example 2: Sending JSON Specs
    print("\n=== Example 2: Sending JSON Specs ===")
    code_spec = {
        "name": "swap_keys_values",
        "description": "Swaps the keys and values in a given dictionary.",
        "params": {
            "d": "A dictionary with unique values."
        },
    }

    messages_2 = [
        {
            "role": "system",
            "content": "You are an expert software engineer that writes clean functional code. You always document your functions."
        },
        {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"}
    ]
    response_2 = generate_response(messages_2)
    print(response_2)
