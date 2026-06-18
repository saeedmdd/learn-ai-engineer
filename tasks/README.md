# Implementation Tasks

Work through these tasks in order. They are designed to make the first project feel like a production AI dependency rather than a prompt demo.

Each task should be implemented in `projects/01-structured-support-triage`.

## Review Workflow

1. Pick one task.
2. Implement only that task.
3. Run the verification commands listed in the task.
4. Send me the task number and ask for review.

Example:

```text
I finished Task 01. Please review it.
```

When I review, I will look for correctness, contract clarity, test quality, and whether the implementation keeps the code easy to replace with a real model later.

## Task Order

1. [Task 01: Eval Failure Reporting](0001-eval-failure-reporting.md)
2. [Task 02: Adversarial Golden Examples](0002-adversarial-golden-examples.md)
3. [Task 03: Trace Each Triage Run](0003-trace-each-triage-run.md)
4. [Task 04: Predictor Boundary](0004-predictor-boundary.md)
5. [Task 05: Implementation Reflection](0005-implementation-reflection.md)

## Ground Rules

- Do not add paid API dependencies yet.
- Keep the public behavior runnable with the standard library.
- Prefer tests over manual checks when behavior is important.
- Keep each task small; do not jump ahead to later roadmap phases.
- If a task feels ambiguous, write down your assumption in the implementation notes or commit message before coding.
