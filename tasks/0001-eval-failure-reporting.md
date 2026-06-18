# Task 01: Eval Failure Reporting

## Objective

Make eval failures inspectable. A metric like `exact_accuracy: 0.875` is not enough; an engineer needs to know which examples failed and why.

## Why This Matters

AI engineering depends on tight feedback loops. When a prompt, model, retrieval setting, or classifier changes, you need fast visibility into regressions. This task turns the current eval runner from a score printer into a debugging tool.

## Files To Touch

- `projects/01-structured-support-triage/support_triage/evaluator.py`
- `projects/01-structured-support-triage/support_triage/cli.py`
- `projects/01-structured-support-triage/tests/test_evaluator.py`

## Requirements

- Add per-example failure reporting to the evaluator.
- A failure should include:
  - the input ticket text
  - expected category, priority, and escalation values
  - actual category, priority, and escalation values
  - which fields failed
- Keep the existing metrics output stable by default.
- Add a CLI flag named `--show-failures`.
- When `--show-failures` is passed, print the metrics first, then a readable failure section.
- If there are no failures, print `failures: none`.

## Suggested Shape

You may return a richer object from `evaluate()`, such as:

```python
{
    "metrics": {...},
    "failures": [...]
}
```

If you choose a different shape, keep it simple and testable.

## Verification

From `projects/01-structured-support-triage`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m support_triage.cli --eval data/golden.jsonl
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m support_triage.cli --eval data/golden.jsonl --show-failures
```

## Acceptance Criteria

- Existing tests pass.
- New tests cover at least one failed example.
- Existing CLI eval output still prints the same metric names.
- `--show-failures` is useful when there is a failure and quiet when there is not.

## Review Focus

I will check whether the failure report is easy to use, whether the data shape is stable enough for later automation, and whether tests would catch a regression in failure reporting.
