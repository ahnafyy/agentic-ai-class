# Sending Prompts Programmatically & Managing Memory

To get started building agents, we need to understand how to send prompts to LLMs. Agents require two key capabilities:

## 1. Programmatic Prompting

Automating the prompt-response cycle that humans do manually in a conversation. This forms the foundation of the Agent Loop we’ll explore.

## 2. Memory Management

Controlling what information persists between iterations, like API calls and their results, to maintain context through the agent’s decision-making process.


Programmatically sending prompts is how we move from having a human type in prompts and then take action based on the LLM’s response to having an agent that can do this automatically. The Agent Loop that we will begin building over the next several readings will be programmatically sending prompts to the LLM and then taking action based on the LLM’s response.

We will also need to understand how to manage what the LLM knows or remembers. This is important because we want to be able to control what information the LLM has in each iteration of the loop. For example, if it just called an API, we want it to remember what API it asked to be invoked and what the result of that