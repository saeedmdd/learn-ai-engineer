from __future__ import annotations

import unittest
from pathlib import Path

from support_triage.evaluator import evaluate, load_jsonl


class EvaluatorTests(unittest.TestCase):
    def test_evaluates_golden_dataset(self) -> None:
        data_path = Path(__file__).parents[1] / "data" / "golden.jsonl"
        metrics = evaluate(load_jsonl(data_path))

        self.assertEqual(metrics["total"], 8)
        self.assertGreaterEqual(metrics["category_accuracy"], 0.875)
        self.assertGreaterEqual(metrics["priority_accuracy"], 0.875)
        self.assertGreaterEqual(metrics["escalation_accuracy"], 0.875)

    def test_rejects_empty_dataset(self) -> None:
        with self.assertRaises(ValueError):
            evaluate([])


if __name__ == "__main__":
    unittest.main()
