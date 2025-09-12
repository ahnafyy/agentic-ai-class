from litellm import completion
from typing import List, Dict

# function that will take in messages and call the gpt api
# and then destructure the response from the payload
def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # First call: model writes a function
    first_messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": "Write a Python function to reverse a string."}
    ]
    first_response = generate_response(first_messages)
    print("=== First Response ===")
    print(first_response)

    # Second call: no previous context (model forgets)
    second_messages = [
        {"role": "user", "content": "Add type hints to the function."}
    ]
    second_response = generate_response(second_messages)
    print("\n=== Second Response (No Context) ===")
    print(second_response)

    # Third call: includes previous context (model remembers)
    third_messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": "Write a Python function to reverse a string."},
        {"role": "assistant", "content": first_response},
        {"role": "user", "content": "Add type hints to the function."}
    ]
    third_response = generate_response(third_messages)
    print("\n=== Third Response (With Context) ===")
    print(third_response)
