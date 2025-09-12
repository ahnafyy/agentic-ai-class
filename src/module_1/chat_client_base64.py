from litellm import completion
from typing import List, Dict

# function that will take it messages and call the gpt api
# and then destructure the response from the payload
def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        # adding messages
        messages=messages,
        max_tokens=1024
    )
    # return the content of the message in base64
    # return response.choices[0].message.content.encode('utf-8').hex()
    return response.choices[0].message.content

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are an expert software engineer that prefers functional programming. You only respond in Base64 encoded strings."},
        {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
    ]

    response = generate_response(messages)
    print(response)
