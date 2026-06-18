# Task 03: Trace Each Triage Run

## Objective

Add lightweight tracing for each triage call so model behavior can be inspected later.

## Why This Matters

In production, an AI output without trace data is difficult to debug. You need to know what ran, how long it took, what contract fields came back, and whether validation passed, without leaking sensitive raw user text into logs by default.

## Files To Touch

- `projects/01-structured-support-triage/support_triage/cli.py`
- `projects/01-structured-support-triage/support_triage/heuristic_model.py`
- New file: `projects/01-structured-support-triage/support_triage/tracing.py`
- New or existing tests under `projects/01-structured-support-triage/tests/`

## Requirements

- Add a small trace object for a single triage run.
- Include:
  - `trace_id`
  - `started_at`
  - `latency_ms`
  - `input_chars`
  - `category`
  - `priority`
  - `confidence`
  - `escalation_required`
  - `predictor`
- Do not store raw ticket text in the trace.
- Add a CLI flag named `--trace`.
- When `--trace` is passed for a single ticket, print the normal result and then the trace as JSON.
- Keep eval mode focused on eval output; do not add tracing to `--eval` yet.

## Suggested Shape

Add a helper that wraps prediction:

```python
result, trace = trace_triage_run(ticket, predictor=triage_ticket)
```

The trace can be a dataclass with `to_dict()`.

## Verification

From `projects/01-structured-support-triage`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m support_triage.cli --trace "Security alert says an unknown device accessed my account."
```

## Acceptance Criteria

- Trace output is valid JSON.
- Trace output does not include the raw ticket text.
- Tests cover trace shape and at least one privacy constraint.
- Normal CLI behavior still works without `--trace`.

## Review Focus

I will check whether tracing is useful, minimal, privacy-aware, and not tangled into the classifier in a way that makes a future model adapter harder.
