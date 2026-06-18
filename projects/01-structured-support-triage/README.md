# Project 01: Structured Support Triage

This project teaches the first production AI engineering habit: define and test the output contract before you tune prompts.

The code intentionally starts with a deterministic baseline instead of a paid model API. That keeps the engineering loop visible:

- `support_triage/schema.py` validates the output contract.
- `support_triage/heuristic_model.py` is a replaceable stand-in for an LLM call.
- `support_triage/evaluator.py` scores behavior against golden examples.
- `data/golden.jsonl` is the starting eval set.

## Run

```bash
python3 -m unittest discover -s tests
PYTHONPATH=. python3 -m support_triage.cli --eval data/golden.jsonl
PYTHONPATH=. python3 -m support_triage.cli "My laptop keyboard stopped working after an update."
```

## Exercise

Replace `triage_ticket()` in `support_triage/heuristic_model.py` with a real model call later, but keep this interface:

```python
def triage_ticket(text: str) -> TriageResult:
    ...
```

The schema and evals should not care whether the implementation is a heuristic, an OpenAI call, a local model, or a mocked test double.

## Acceptance Criteria

- Unit tests pass.
- Eval command prints category, priority, escalation, and exact-match metrics.
- New examples can be added to `data/golden.jsonl` without changing evaluator code.
- Invalid outputs are rejected by `TriageResult.from_mapping()`.
