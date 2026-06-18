from __future__ import annotations

import unittest

from support_triage.schema import Category, Priority, TriageResult, ValidationError


class TriageResultSchemaTests(unittest.TestCase):
    def test_accepts_valid_mapping(self) -> None:
        result = TriageResult.from_mapping(
            {
                "category": "Hardware",
                "priority": "NORMAL",
                "summary": "Monitor will not turn on.",
                "suggested_reply": "Please share the monitor model.",
                "confidence": 0.8,
                "escalation_required": False,
            }
        )

        self.assertEqual(result.category, Category.HARDWARE)
        self.assertEqual(result.priority, Priority.NORMAL)
        self.assertEqual(result.confidence, 0.8)

    def test_rejects_missing_fields(self) -> None:
        with self.assertRaises(ValidationError):
            TriageResult.from_mapping({"category": "hardware"})

    def test_rejects_unknown_fields(self) -> None:
        with self.assertRaises(ValidationError):
            TriageResult.from_mapping(
                {
                    "category": "hardware",
                    "priority": "normal",
                    "summary": "Monitor issue.",
                    "suggested_reply": "Please share more details.",
                    "confidence": 0.7,
                    "escalation_required": False,
                    "raw_model_text": "{}",
                }
            )

    def test_rejects_invalid_confidence(self) -> None:
        with self.assertRaises(ValidationError):
            TriageResult.from_mapping(
                {
                    "category": "hardware",
                    "priority": "normal",
                    "summary": "Monitor issue.",
                    "suggested_reply": "Please share more details.",
                    "confidence": 1.5,
                    "escalation_required": False,
                }
            )


if __name__ == "__main__":
    unittest.main()
