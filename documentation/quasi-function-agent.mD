
# Possible Solution for Building a Quasi-Agent

Take a minute to scroll to the bottom to look at the complete solution. Once you are done, come back here and we will walk through the solution.

## Understanding the Architecture

Our quasi-agent works through three key steps:

1. Initial code generation  
2. Documentation enhancement  
3. Test case creation  

The magic happens in how we maintain context between these steps, ensuring each builds on the previous results.

## Core Components

### LLM Interaction
```python
def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="openai/gpt-4",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content
````

This function handles our LLM interactions using ChatML format. Each message includes a role (“system”, “user”, or “assistant”) and content.

### Output Cleaning

````python
def extract_code_block(response: str) -> str:
    """Extract code block from response"""
    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:]

    return code_block
````

The LLM often includes commentary with its code. This function extracts just the code block, making it easier to build upon in subsequent prompts.

## The Development Process

The main function `develop_custom_function()` orchestrates three phases of development.

### Phase 1: Initial Code Generation

````python
messages = [
    {"role": "system", "content": "You are a Python expert helping to develop a function."}
]

messages.append({
    "role": "user",
    "content": f"Write a Python function that {function_description}. Output the function in a ```python code block```."
})
````

We start with a system message establishing the LLM’s role, then request initial code based on the user’s description.

### Phase 2: Documentation Enhancement

````python
messages.append({
    "role": "assistant", 
    "content": "```python\n\n"+initial_function+"\n\n```"
})

messages.append({
    "role": "user",
    "content": "Add comprehensive documentation to this function..."
})
````

We feed back only the code (no commentary), keeping the LLM focused on the code structure.

### Phase 3: Test Case Generation

````python
messages.append({
    "role": "assistant", 
    "content": "```python\n\n"+documented_function+"\n\n```"
})

messages.append({
    "role": "user",
    "content": "Add unittest test cases for this function..."
})
````

We maintain clean context by showing only the documented code.

## Memory Management Through Message History

We manage “memory” through the `messages` list. Each step builds on previous responses, but we carefully control what the LLM sees:

* Only the code, not the commentary
* Each message gives a focused instruction
* Context builds progressively

For example, when adding documentation, the LLM sees:

* It’s a Python expert (system message)
* The original code (assistant message)
* The request for documentation (user message)

This focused context ensures consistent, high-quality output.

## Usage Example

```python
>>> function_code, tests, filename = develop_custom_function()
What kind of function would you like to create?
Example: 'A function that calculates the factorial of a number'
Your description: Calculate fibonacci sequence up to n
```

**Initial Function**

```python
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence
```

**Documented Function**
\[... function with added documentation ...]

**Test Cases**
\[... unittest test cases ...]

**Output**

```
Final code has been saved to calculate_fibonacci_sequence_up.py
```

## Learning from This Design

This quasi-agent illustrates several key principles:

* **Prompt Chaining**: Break complex tasks into sequential steps
* **Context Management**: Control what the LLM sees to maintain focus
* **Output Processing**: Clean LLM output before reuse
* **Progressive Enhancement**: Build features incrementally (code → docs → tests)

These principles apply even when building more complex, fully agentic systems.



