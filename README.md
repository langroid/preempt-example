# Example of preempt usage

```
uv venv --python 3.11
. ./.venv/bin/activate
uv sync --all-extras --all-groups --upgrade-package langroid --upgrade-package preempt
```

Run the test

```
uv run tests/test-round-trip.py
```

# Run the LLM-chat test using pytest

```bash
pytest tests/test-llm-chat.py
```
