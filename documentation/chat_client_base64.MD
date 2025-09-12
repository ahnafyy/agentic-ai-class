# Sending Prompts Programmatically & Managing Memory 2

First, let’s take a look at the code again:

```python
from litellm import completion
from typing import List, Dict

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4o",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content

messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)
```

---

## Key Components

- **Importing `completion`**:  
  The `completion` function from the `litellm` library is the primary method for interacting with Large Language Models (LLMs). It serves as the bridge between your code and the LLM, allowing you to send prompts and receive responses efficiently.

### How `completion` Works

- **Input**:  
  You provide a prompt—a list of messages for the model to process. This could be a question, command, or instructions.

- **Output**:  
  The function returns the model’s response, typically as generated text based on your prompt.

- **Messages Parameter**:  
  Follows the ChatML format—a list of dictionaries containing `role` and `content`. The `role` attribute indicates who is “speaking” in the conversation, helping the LLM understand context.

#### Roles

- `"system"`: Sets initial instructions, rules, or configuration for the model (e.g., “You will respond in JSON.”).
- `"user"`: Represents input from the user—your prompts, questions, or instructions.
- `"assistant"`: Represents responses from the AI model. You can use this to provide context or guide the model with sample responses.

- **Model Specification**:  
  Use the provider/model format (e.g., `"openai/gpt-4o"`).

- **Response Content**:  
  The generated text is found in `choices[0].message.content`, similar to what you’d see in a chat interface.

## Quick Exercise

**Practice:**  
Try creating a prompt that only provides the response as a Base64 encoded string and refuses to answer in natural language.   Can you get your LLM to only respond in Base64?
