# agentic-ai-class
Coursework for AI Agents and Agentic AI with Python & Generative AI by Vanderbilt University


## Setup

I’m using a Python virtual environment (`venv`) to keep all my dependencies for these exercises isolated from the system Python. This avoids version conflicts and makes it easy for anyone to recreate the same environment on their machine.

## How I Set It Up

**Create and activate the virtual environment**

Make sure you have python installed on your box.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Install dependencies**

```bash
pip install --upgrade pip
pip install litellm
```

**Set up OpenAI API key (only once)**

```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc
```

**Run any of the scripts**

```bash
python src/module_1/chat_client_module_1.py
```

**When done**

```bash
deactivate
```

