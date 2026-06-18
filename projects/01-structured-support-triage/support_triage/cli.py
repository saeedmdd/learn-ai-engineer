from __future__ import annotations

import argparse
import json

from .evaluator import evaluate, format_report, load_jsonl
from .heuristic_model import triage_ticket


def main() -> None:
    parser = argparse.ArgumentParser(description="Structured support triage starter.")
    parser.add_argument("ticket", nargs="?", help="Ticket text to classify.")
    parser.add_argument("--eval", dest="eval_path", help="Path to a JSONL golden dataset.")
    args = parser.parse_args()

    if args.eval_path:
        rows = load_jsonl(args.eval_path)
        print(format_report(evaluate(rows)))
        return

    if not args.ticket:
        parser.error("provide a ticket or --eval")

    result = triage_ticket(args.ticket)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
