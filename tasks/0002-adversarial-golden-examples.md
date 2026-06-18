# Task 02: Adversarial Golden Examples

## Objective

Add a small adversarial eval set that tests confusing or hostile support tickets.

## Why This Matters

Production AI systems fail on edge cases before they fail on clean examples. Even before using a real LLM, you should practice writing examples that expose routing ambiguity, prompt-injection style language, and escalation mistakes.

## Files To Touch

- `projects/01-structured-support-triage/data/adversarial.jsonl`
- `projects/01-structured-support-triage/tests/test_evaluator.py`
- Optionally `projects/01-structured-support-triage/support_triage/heuristic_model.py`
- Optionally `projects/01-structured-support-triage/README.md`

## Requirements

- Add `data/adversarial.jsonl` with at least 8 examples.
- Include at least:
  - 2 examples that contain prompt-injection style language, such as "ignore previous instructions"
  - 2 examples with multiple possible categories
  - 2 examples where escalation should be required
  - 2 examples where escalation should not be required despite urgent-sounding language
- Add tests that load and evaluate `data/adversarial.jsonl`.
- Set realistic thresholds. Do not require 100% accuracy unless the baseline genuinely earns it.
- If you adjust the heuristic model, keep changes small and explainable.

## JSONL Format

Each line should match the existing golden dataset format:

```json
{"ticket":"...","expected_category":"account","expected_priority":"high","expected_escalation":false}
```

## Verification

From `projects/01-structured-support-triage`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m support_triage.cli --eval data/adversarial.jsonl --show-failures
```

If `--show-failures` is not implemented yet, complete Task 01 first.

## Acceptance Criteria

- `data/adversarial.jsonl` exists and is valid JSONL.
- Tests prove the adversarial dataset is loadable and measurable.
- The examples are meaningfully harder than `data/golden.jsonl`.
- Any heuristic changes improve the eval without adding brittle one-off hacks for every exact sentence.

## Review Focus

I will check the quality of the adversarial examples, whether expected labels are defensible, and whether any classifier changes generalize instead of memorizing the dataset.
