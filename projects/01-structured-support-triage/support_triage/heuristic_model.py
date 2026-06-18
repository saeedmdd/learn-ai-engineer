from __future__ import annotations

from .schema import Category, Priority, TriageResult


_CATEGORY_KEYWORDS: list[tuple[Category, tuple[str, ...]]] = [
    (
        Category.ACCOUNT,
        (
            "account",
            "password",
            "mfa",
            "login",
            "log in",
            "unknown device",
            "accessed",
        ),
    ),
    (
        Category.BILLING,
        (
            "invoice",
            "charged",
            "refund",
            "payment",
            "billing",
            "card",
            "address",
        ),
    ),
    (
        Category.SOFTWARE,
        (
            "app",
            "software",
            "crash",
            "crashes",
            "csv",
            "export",
            "install",
            "update",
        ),
    ),
    (
        Category.HARDWARE,
        (
            "monitor",
            "laptop",
            "keyboard",
            "mouse",
            "printer",
            "screen",
            "hdmi",
            "device",
        ),
    ),
]


def triage_ticket(text: str) -> TriageResult:
    normalized = _normalize(text)
    category, category_score = _classify_category(normalized)
    priority = _classify_priority(normalized)
    escalation_required = _needs_escalation(normalized, priority)

    return TriageResult(
        category=category,
        priority=priority,
        summary=_summary(text),
        suggested_reply=_reply_for(category, priority, escalation_required),
        confidence=_confidence(category_score, priority),
        escalation_required=escalation_required,
    )


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _classify_category(text: str) -> tuple[Category, int]:
    best_category = Category.OTHER
    best_score = 0

    for category, keywords in _CATEGORY_KEYWORDS:
        score = sum(1 for keyword in keywords if keyword in text)
        if score > best_score:
            best_category = category
            best_score = score

    return best_category, best_score


def _classify_priority(text: str) -> Priority:
    urgent_terms = (
        "security alert",
        "breach",
        "unknown device",
        "production down",
        "data loss",
    )
    high_terms = (
        "charged twice",
        "refund",
        "cannot log in",
        "can't log in",
        "crashes every time",
        "blocked",
    )
    low_terms = (
        "please update",
        "next invoice",
        "when possible",
    )

    if any(term in text for term in urgent_terms):
        return Priority.URGENT
    if any(term in text for term in high_terms):
        return Priority.HIGH
    if any(term in text for term in low_terms):
        return Priority.LOW
    return Priority.NORMAL


def _needs_escalation(text: str, priority: Priority) -> bool:
    escalation_terms = (
        "security alert",
        "breach",
        "unknown device",
        "charged twice",
        "refund",
    )
    return priority is Priority.URGENT or any(term in text for term in escalation_terms)


def _summary(text: str) -> str:
    normalized = " ".join(text.strip().split())
    if not normalized:
        return "No ticket text provided."
    return normalized[:157] + "..." if len(normalized) > 160 else normalized


def _reply_for(category: Category, priority: Priority, escalation_required: bool) -> str:
    if escalation_required:
        return "Thanks for the details. I am escalating this so a specialist can review it with priority."

    replies = {
        Category.ACCOUNT: "Thanks for reporting this. Please confirm the affected email address and the last successful login time.",
        Category.BILLING: "Thanks for reaching out. Please share the invoice number so we can review the billing details.",
        Category.HARDWARE: "Thanks for the report. Please confirm the device model and any troubleshooting steps already tried.",
        Category.SOFTWARE: "Thanks for the report. Please share the app version, operating system, and the exact error if one appears.",
        Category.OTHER: "Thanks for the details. Please share any extra context that would help us route this correctly.",
    }
    if priority is Priority.LOW:
        return "Thanks for the update. We will handle this as a low-priority account request."
    return replies[category]


def _confidence(category_score: int, priority: Priority) -> float:
    base = 0.55 + min(category_score, 3) * 0.1
    if priority in {Priority.HIGH, Priority.URGENT}:
        base += 0.08
    return round(min(base, 0.95), 2)
