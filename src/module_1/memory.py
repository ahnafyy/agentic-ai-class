# prove_stateless_simple.py
from openai import OpenAI

client = OpenAI()

def generate(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

def main():
    # First call — model writes a function
    first_messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": "Write a Python function to reverse a string."}
    ]
    first_response = generate(first_messages)
    print("=== First Response ===")
    print(first_response)

    # Second call — no previous context (model forgets)
    second_messages = [
        {"role": "user", "content": "Add type hints to the function."}
    ]
    second_response = generate(second_messages)
    print("\n=== Second Response (No Context) ===")
    print(second_response)

    # Third call — includes the previous response for context
    third_messages = [
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": "Write a Python function to reverse a string."},
        {"role": "assistant", "content": first_response},
        {"role": "user", "content": "Add type hints to the function."}
    ]
    third_response = generate(third_messages)
    print("\n=== Third Response (With Context) ===")
    print(third_response)

if __name__ == "__main__":
    main()
