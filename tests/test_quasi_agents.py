import os
import pytest

from types import SimpleNamespace
import sys
from pathlib import Path


def make_choice_message(content: str):
    # helper to create a fake completion response object similar to litellm
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


@pytest.mark.parametrize("response_content, expected",
                         [
                             ("Just some plain text answer", "Just some plain text answer"),
                             ("```python\nprint(\"hi\")\n```", "print(\"hi\")"),
                             ("```\nnot python code\n```", "not python code"),
                             ("""Some text
```python
print("multi")
```
More text""", 'print("multi")'),
                         ])
def test_extract_code_block_variants(response_content, expected):
    # test the extract_code_block behavior in both modules by importing function directly
    # ensure repo root is in sys.path so `src` package is importable
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from src.module_1.quasi_agent import extract_code_block as extract1
    from src.module_1.quasi_agent_gemini import extract_code_block as extract2

    assert extract1(response_content) == expected
    assert extract2(response_content) == expected


def test_multi_block_and_assistant_role(tmp_path, monkeypatch):
    """Test handling of responses where the assistant role appears in messages and the
    model returns multiple fenced code blocks or assistant-style messages.
    """
    # Prepare a response that includes assistant content and multiple code blocks
    assistant_like = (
        'assistant: Here is the function you asked for.\n'
        '```python\ndef foo():\n    return "a"\n```\n'
        'Some commentary\n'
        '```python\ndef bar():\n    return "b"\n```'
    )

    # We'll return the assistant_like as the first completion and then documented/tests
    documented = "```python\ndef foo():\n    \"\"\"Docs\n    \"\"\"\n    return 'a'\n```"
    tests = "```python\n# tests\n```"

    seq = [assistant_like, documented, tests]

    def fake_completion(*, model, messages, max_tokens):
        return make_choice_message(seq.pop(0))

    # load quasi_agent module and patch completion
    from src.module_1 import quasi_agent as qa
    monkeypatch.setattr(qa, 'completion', lambda **kwargs: fake_completion(**kwargs))

    # simulate input
    monkeypatch.setattr('builtins.input', lambda: 'Create two small functions foo and bar')

    # run in tmp dir
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        documented_code, tests_code, filename = qa.develop_custom_function()
        content = (tmp_path / filename).read_text()
        # Expect at least one of the generated functions to be present
        assert 'def foo' in content or 'def bar' in content
    finally:
        os.chdir(cwd)


def test_generate_response_and_file_write(tmp_path, monkeypatch):
    # This test will mock litellm.completion to return structured responses for the gemini
    # module and then run develop_custom_function with simulated user input. We check the written file
    # and basic contents.

    # Prepare fake responses for the sequence: initial function, documented function, tests
    initial = "```python\ndef add(a, b):\n    return a + b\n```"
    documented = "```python\ndef add(a, b):\n    \"\"\"Add two numbers\n\n    Parameters\n    ----------\n    a: int\n    b: int\n    \n    Returns\n    -------\n    int\n    \"\"\"\n    return a + b\n```"
    tests = "```python\nimport unittest\n\nclass TestAdd(unittest.TestCase):\n    def test_basic(self):\n        self.assertEqual(add(1, 2), 3)\n```"

    seq = [initial, documented, tests]

    def fake_completion(*, model, messages, max_tokens):
        # pop from seq
        return make_choice_message(seq.pop(0))

    # import quasi_agent module normally
    from src.module_1 import quasi_agent as qa

    # monkeypatch the completion used inside quasi_agent
    monkeypatch.setattr(qa, 'completion', lambda **kwargs: fake_completion(**kwargs))

    # simulate user input for function description
    monkeypatch.setattr('builtins.input', lambda: 'A function that adds two numbers')

    # change cwd to tmp_path so files are written to tmp
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        documented_code, tests_code, filename = qa.develop_custom_function()

        # validate file exists and contents include the documented function and tests
        written = tmp_path / filename
        assert written.exists()
        content = written.read_text()
        assert 'def add' in content
        assert 'TestAdd' in content or 'unittest' in content

    finally:
        os.chdir(cwd)
