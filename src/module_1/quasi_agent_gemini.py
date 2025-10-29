from litellm import completion
from typing import List, Dict
import sys

def generate_response(messages: List[Dict]) -> str:
   """Call LLM to get response"""
   response = completion(
      model="gemini/gemini-2.5-flash",
      messages=messages,
      max_tokens=1024
   )
   return response.choices[0].message.content

def extract_code_block(response: str) -> str:
   """Extract code block from response"""
   if not '```' in response:
      return response
   code_block = response.split('```')[1].strip()
   if code_block.startswith("python"):
      code_block = code_block[6:]
      # remove a leading newline if present after the language marker
      if code_block.startswith('\n'):
         code_block = code_block[1:]
   return code_block

def develop_custom_function():
   print("\nWhat kind of function would you like to create?")
   print("Example: 'A function that calculates the factorial of a number'")
   print("Your description: ", end='')
   function_description = input().strip()

   messages = [
      {"role": "system", "content": "You are a Python expert helping to develop a function."}
   ]

   messages.append({
      "role": "user",
      "content": f"Write a Python function that {function_description}. Output the function in a ```python code block```."
   })
   initial_function = generate_response(messages)
   initial_function = extract_code_block(initial_function)
   print("\n=== Initial Function ===")
   print(initial_function)

   messages.append({"role": "assistant", "content": "```python\n\n"+initial_function+"\n\n```"})
   messages.append({
      "role": "user",
      "content": "Add comprehensive documentation to this function, including description, parameters, "
                 "return value, examples, and edge cases. Output the function in a ```python code block```."
   })
   documented_function = generate_response(messages)
   documented_function = extract_code_block(documented_function)
   print("\n=== Documented Function ===")
   print(documented_function)

   messages.append({"role": "assistant", "content": "```python\n\n"+documented_function+"\n\n```"})
   messages.append({
      "role": "user",
      "content": "Add unittest test cases for this function, including tests for basic functionality, "
                 "edge cases, error cases, and various input scenarios. Output the code in a ```python code block```."
   })
   test_cases = generate_response(messages)
   test_cases = extract_code_block(test_cases)
   print("\n=== Test Cases ===")
   print(test_cases)

   filename = function_description.lower()
   filename = ''.join(c for c in filename if c.isalnum() or c.isspace())
   filename = filename.replace(' ', '_')[:30] + '.py'

   with open(filename, 'w') as f:
      f.write(documented_function + '\n\n' + test_cases)

   return documented_function, test_cases, filename

if __name__ == "__main__":
   function_code, tests, filename = develop_custom_function()
   print(f"\nFinal code has been saved to {filename}")
