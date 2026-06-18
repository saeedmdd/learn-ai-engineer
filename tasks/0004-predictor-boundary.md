# Task 04: Predictor Boundary

## Objective

Create a clean boundary between the application contract and the thing that produces predictions.

## Why This Matters

Today the predictor is a heuristic. Later it may be an OpenAI call, a local model, a mock, or a replay fixture. The evaluator, CLI, and tracing code should not care which implementation is behind the boundary.

## Files To Touch

- `projects/01-structured-support-triage/support_triage/heuristic_model.py`
- `projects/01-structured-support-triage/support_triage/evaluator.py`
- `projects/01-structured-support-triage/support_triage/cli.py`
- New file: `projects/01-structured-support-triage/support_triage/predictors.py`
- Tests under `projects/01-structured-support-triage/tests/`

## Requirements

- Add a predictor protocol or interface with one operation:

```python
predict(ticket: str) -> TriageResult
```

- Wrap the existing heuristic classifier behind that predictor boundary.
- Keep the existing `triage_ticket(text: str) -> TriageResult` function available for compatibility.
- Update evaluator and CLI internals to use the predictor boundary.
- Add a fake predictor in tests to prove evaluator logic is not tied to the heuristic implementation.

## Constraints

- Do not add a real model API yet.
- Do not add third-party dependencies.
- Keep the boundary boring. This is an interface exercise, not a framework exercise.

## Verification

From `projects/01-structured-support-triage`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m support_triage.cli --eval data/golden.jsonl --show-failures
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m support_triage.cli "The desktop app crashes every time I export a CSV."
```

## Acceptance Criteria

- Existing public commands keep working.
- Tests use a fake predictor for at least one evaluator scenario.
- The heuristic predictor is replaceable without changing schema validation.
- The code still reads like standard Python, not an overbuilt abstraction layer.

## Review Focus

I will check whether the boundary is genuinely useful, whether compatibility was preserved, and whether the abstraction is smaller than the problem it solves.
