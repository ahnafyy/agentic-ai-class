# LLMs Do Not Have Memory

## Why Memory Matters for Agents
When building an Agent, it must remember its actions and the results of those actions.  
For example, if it tries to create a calendar event and the API call fails due to an incorrect parameter, the Agent must remember that failure and why it happened. This allows it to correct the mistake and try again.  
For multi-step tasks, the Agent must also remember the result of each step to continue from where it left off.  
This need for memory contrasts with how LLMs work.

---

## LLMs Are Stateless
LLMs do **not** inherently remember previous conversations or responses.  
Each call to the model generates a response solely from what is included in the `messages` parameter. If previous context is not passed, the model will not know it existed.

To simulate continuity, you must explicitly include all relevant prior messages (system, user, and assistant) in every request.

---

## Example 1 — Missing Context
```python
messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

# Second query without context
messages = [
    {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)
````

**Output:**

```
# First response
def swap_keys_values(d):
    return {v: k for k, v in d.items()}

# Second response
I'm not sure what function you're referring to. Can you clarify?
```

**Explanation:** The model does not remember its previous output because it wasn’t included in the second request.

---

## Example 2 — Including Previous Responses for Continuity

```python
messages = [
   {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
   {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

# Include the assistant's previous response for context
messages = [
   {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
   {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."},
   {"role": "assistant", "content": response},
   {"role": "user", "content": "Update the function to include documentation."}
]

response = generate_response(messages)
print(response)
```

**Output (excerpt):**

```python
def swap_keys_values(d):
    """
    Swaps the keys and values in the given dictionary.
    ...
    """
    if len(d.values()) != len(set(d.values())):
        raise ValueError("Duplicate values detected.")
    return {v: k for k, v in d.items()}
```

**Explanation:** By including the assistant’s prior response, the model can see what it wrote before and build on it.

---

## Key Takeaways

* **No Inherent Memory:** The LLM does not retain past interactions unless you explicitly include them.
* **Provide Full Context:** Always pass all relevant prior `messages` for continuity.
* **Assistant Role Usage:** Adding previous responses as `assistant` messages lets the model build on earlier outputs.
* **Memory Management:** You control what the model “remembers” by choosing what to include or omit from `messages`. You can also make it “forget” if needed to break out of unhelpful behavior.

---

## Why This Matters

LLMs are stateless. Designing multi-step agents requires explicit memory handling.
Developers must manage and provide context so the model can generate accurate and relevant responses.

