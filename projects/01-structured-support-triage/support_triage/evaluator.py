from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from .heuristic_model import triage_ticket
from .schema import TriageResult

Predictor = Callable[[str], TriageResult]


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}") from exc
    return rows


def evaluate(rows: Iterable[dict[str, Any]], predictor: Predictor = triage_ticket) -> dict[str, float | int]:
    total = 0
    category_hits = 0
    priority_hits = 0
    escalation_hits = 0
    exact_hits = 0

    for row in rows:
        total += 1
        output = predictor(row["ticket"])

        category_ok = output.category.value == row["expected_category"]
        priority_ok = output.priority.value == row["expected_priority"]
        escalation_ok = output.escalation_required is row["expected_escalation"]

        category_hits += int(category_ok)
        priority_hits += int(priority_ok)
        escalation_hits += int(escalation_ok)
        exact_hits += int(category_ok and priority_ok and escalation_ok)

    if total == 0:
        raise ValueError("cannot evaluate an empty dataset")

    return {
        "total": total,
        "category_accuracy": round(category_hits / total, 3),
        "priority_accuracy": round(priority_hits / total, 3),
        "escalation_accuracy": round(escalation_hits / total, 3),
        "exact_accuracy": round(exact_hits / total, 3),
    }


def format_report(metrics: dict[str, float | int]) -> str:
    return "\n".join(
        [
            f"total: {metrics['total']}",
            f"category_accuracy: {metrics['category_accuracy']}",
            f"priority_accuracy: {metrics['priority_accuracy']}",
            f"escalation_accuracy: {metrics['escalation_accuracy']}",
            f"exact_accuracy: {metrics['exact_accuracy']}",
        ]
    )
