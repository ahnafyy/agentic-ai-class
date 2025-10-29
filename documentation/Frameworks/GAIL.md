# GAIL – Goals, Actions, Information, Language

## Goals

Defines what the agent (or intern) is supposed to do and how to behave.
Includes the **persona**, **rules**, and **process** that shape its decision-making and output consistency.

* **Persona:** The identity or role the agent should assume (e.g., “You are ActionAgent, a helpful AI assistant”).
* **Rules:** Constraints or behavioral guidelines the agent must follow (e.g., what it can or cannot do).
* **Process:** Step-by-step procedures the agent should always perform before acting (e.g., “First check if an expense already exists before adding a new one”).

## Actions

Specifies what the agent is *allowed to do* within its environment.

* Defines the **tools** or **capabilities** available (e.g., API calls, database lookups, web search).
* Determines **interaction limits**—the agent can only act using approved methods.
* Each action provides **feedback** that informs subsequent steps.

## Information

Covers what the agent *knows* or *receives* to complete the task.

* Includes initial **input data** from the user (context, documents, queries).
* Expands as the session evolves—adding **feedback**, **results of actions**, and **state updates**.
* Represents **ephemeral**, task-specific context that informs decision-making at each iteration.

## Language

Defines how the agent should *communicate* its reasoning and outputs.

* Specifies **output format** (e.g., JSON schema, structured markdown, or “TPS report” style).
* Guides **communication tone** (e.g., concise, customer-service-friendly, analytical).
* Enables structured reasoning through **“stop and think”** or step-by-step explanation blocks.
* Can be combined with **function calling or schema enforcement** to control response fidelity.

### GAIL in Prompt Architecture

When building prompts:

* **System messages** encode **G**, **A**, and **L** — persistent ground rules, capabilities, and communication format.
* **User messages** supply **I** — the task-specific information or feedback.
  Together, these form a stable loop for agent reasoning, action execution, and communication—preventing failure through clarity and structure rather than verbose instruction.
