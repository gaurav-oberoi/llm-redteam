"""CLI: run the jailbreak red-team suite against a local model and print a report."""

from __future__ import annotations

import json
import sys

from .runner import run
from .target import ollama_target


def main() -> None:
    quiet = "--quiet" in sys.argv
    model_fn = ollama_target()
    print("Running jailbreak red-team suite (canary-extraction) against the target model...\n", file=sys.stderr)
    report = run(model_fn)

    print(f"Resisted {report.resisted}/{report.total} attacks  (pass rate {report.pass_rate:.0%})\n")
    for r in report.results:
        mark = "LEAK " if r.leaked else "ok   "
        print(f"  [{mark}] {r.id:<16} ({r.category})")
    if not quiet:
        print("\nBy category:")
        for cat, c in report.by_category().items():
            print(f"  {cat:<22} {c['total'] - c['leaks']}/{c['total']} resisted")
    # Non-zero exit if the model leaked the canary to any attack.
    sys.exit(1 if report.leaks else 0)


if __name__ == "__main__":
    main()
