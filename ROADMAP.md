# Production AI Engineering Roadmap

This is a 16-week path at about 6 hours per week. Each phase produces a working artifact, an eval artifact, and a short learning record when something non-obvious becomes durable.

## Phase 1: LLM App Contracts (Weeks 1-2)

Goal: make one model call behave like a production dependency.

- Learn: model APIs, tokens, structured outputs, function/tool calling, retries, rate limits, and prompt contracts.
- Build: structured support triage.
- Done when: outputs are validated, bad outputs fail loudly, and a golden eval set measures behavior.
- Workspace artifact: [projects/01-structured-support-triage](projects/01-structured-support-triage).

## Phase 2: RAG Systems (Weeks 3-5)

Goal: answer from owned knowledge instead of model memory.

- Learn: document loading, chunking, embeddings, vector search, metadata filters, reranking, citations, and refusal behavior.
- Build: a knowledge-base assistant over local docs.
- Done when: answers cite source snippets, unsupported questions are refused, and retrieval quality is measured.

## Phase 3: Evaluation And Reliability (Weeks 6-8)

Goal: make AI behavior change measurable before changing prompts, models, or retrieval settings.

- Learn: golden sets, rubric graders, regression thresholds, adversarial cases, model comparison, and prompt/version tracking.
- Build: an eval runner and report for the RAG assistant.
- Done when: one command compares variants across quality, latency, and estimated cost.

## Phase 4: Tool-Using Agents (Weeks 9-11)

Goal: build agents as stateful workflows, not magical loops.

- Learn: tool definitions, tool results, idempotency, permissions, state, human approval, retries, and resumability.
- Build: a developer-workflow agent that can inspect files, call safe tools, and pause before risky actions.
- Done when: every tool call is traceable and risky actions require approval.

## Phase 5: Production Capstone (Weeks 12-16)

Goal: ship a complete AI feature as if it will be maintained.

- Build one of: support copilot, document operations assistant, repo-maintenance agent, analytics copilot, or another real workflow.
- Include: auth or user identity, API/UI, trace logs, evals, prompt/version history, rate limiting, cost budget, latency budget, safety tests, deployment notes, and failure-mode documentation.
- Done when: the app can be demoed from a clean checkout and has an eval report explaining what works and what still fails.

## Weekly Routine

- 2 hours: read a primary source and summarize what changed in your mental model.
- 3 hours: implement the current project slice.
- 1 hour: run evals, inspect failures, and write down what should change next.
