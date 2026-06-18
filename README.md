# Learn AI Engineering

This workspace tracks a production AI engineering learning path for an experienced software engineer.

Start here:

1. Read [MISSION.md](MISSION.md).
2. Read [ROADMAP.md](ROADMAP.md).
3. Open the first lesson: [lessons/0001-output-contracts-before-prompts.html](lessons/0001-output-contracts-before-prompts.html).
4. Pick an implementation task from [tasks/README.md](tasks/README.md).
5. Run the first project:

```bash
cd projects/01-structured-support-triage
python3 -m unittest discover -s tests
PYTHONPATH=. python3 -m support_triage.cli --eval data/golden.jsonl
```

The roadmap is centered on LLM systems: structured outputs, RAG, evals, tool use, agents, observability, latency, cost, and safety. Model training is treated as an optional specialization after the production app foundations are stable.
