from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class ValidationError(ValueError):
    """Raised when a model output does not match the triage contract."""


class Category(str, Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    BILLING = "billing"
    ACCOUNT = "account"
    OTHER = "other"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


_ALLOWED_FIELDS = {
    "category",
    "priority",
    "summary",
    "suggested_reply",
    "confidence",
    "escalation_required",
}


@dataclass(frozen=True)
class TriageResult:
    category: Category
    priority: Priority
    summary: str
    suggested_reply: str
    confidence: float
    escalation_required: bool

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TriageResult":
        missing = _ALLOWED_FIELDS - set(data)
        if missing:
            raise ValidationError(f"missing required field(s): {sorted(missing)}")

        extra = set(data) - _ALLOWED_FIELDS
        if extra:
            raise ValidationError(f"unknown field(s): {sorted(extra)}")

        return cls(
            category=_coerce_enum(Category, data["category"], "category"),
            priority=_coerce_enum(Priority, data["priority"], "priority"),
            summary=_coerce_text(data["summary"], "summary", max_length=200),
            suggested_reply=_coerce_text(data["suggested_reply"], "suggested_reply", max_length=500),
            confidence=_coerce_confidence(data["confidence"]),
            escalation_required=_coerce_bool(data["escalation_required"], "escalation_required"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category.value,
            "priority": self.priority.value,
            "summary": self.summary,
            "suggested_reply": self.suggested_reply,
            "confidence": self.confidence,
            "escalation_required": self.escalation_required,
        }


def _coerce_enum(enum_type: type[Enum], value: Any, field: str) -> Any:
    if isinstance(value, enum_type):
        return value
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    try:
        return enum_type(value.strip().lower())
    except ValueError as exc:
        allowed = ", ".join(item.value for item in enum_type)
        raise ValidationError(f"{field} must be one of: {allowed}") from exc


def _coerce_text(value: Any, field: str, max_length: int) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    normalized = " ".join(value.split())
    if not normalized:
        raise ValidationError(f"{field} must not be empty")
    if len(normalized) > max_length:
        raise ValidationError(f"{field} must be at most {max_length} characters")
    return normalized


def _coerce_confidence(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError("confidence must be a number")
    confidence = float(value)
    if not 0.0 <= confidence <= 1.0:
        raise ValidationError("confidence must be between 0.0 and 1.0")
    return confidence


def _coerce_bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValidationError(f"{field} must be a boolean")
    return value
