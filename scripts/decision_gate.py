#!/usr/bin/env python3
"""CI gate: Tier 1/2 pull requests need an owner-approved decision record.

Inputs (env): HEAD_REF (branch), PR_TITLE, PR_LABELS (comma-separated).
Passes when:
  - the branch has a Tier 0 prefix (fix/, chore/, docs/, test/, refactor/, ci/, deps/, dependabot/, revert-), or
  - the PR has the `tier-0` label (owner override, visible on the PR), or
  - the branch or title names D-NNNN and decisions/D-NNNN-*.md has status approved, shipped or reviewed.
Limitation: CI cannot tell whether the owner or an agent wrote `status: approved`.
The Claude Code guard hook blocks agents from writing it; this gate checks it exists.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

TIER0_PREFIXES = (
    "fix/",
    "chore/",
    "docs/",
    "test/",
    "refactor/",
    "ci/",
    "deps/",
    "dependabot/",
    "revert-",
)
OK_STATUSES = {"approved", "shipped", "reviewed"}


def status_of(record: Path) -> str:
    m = re.search(r"^status:\s*([\w-]+)", record.read_text(), re.M)
    return m.group(1).lower() if m else ""


def evaluate(
    branch: str, title: str, labels: list[str], decisions_dir: Path
) -> tuple[bool, str]:
    if branch.startswith(TIER0_PREFIXES):
        return True, f"Tier 0 branch '{branch}': no decision record needed."
    if "tier-0" in labels:
        return True, "Labelled tier-0 by a maintainer: no decision record needed."
    ids = sorted(set(re.findall(r"D-\d{4}", f"{branch} {title}")))
    if not ids:
        return False, (
            f"Branch '{branch}' is not a Tier 0 prefix and neither the branch nor the title names a decision "
            "(D-NNNN). Rename the branch (fix/, chore/, docs/, test/, refactor/, ci/, deps/), put the approved "
            "decision ID in the title, or have the owner add the `tier-0` label."
        )
    for did in ids:
        matches = sorted(decisions_dir.glob(f"{did}-*.md"))
        if not matches:
            return False, f"{did}: no decisions/{did}-*.md in this branch."
        status = status_of(matches[0])
        if status not in OK_STATUSES:
            return (
                False,
                f"{did}: status is '{status or 'missing'}'. The owner must set it to approved before merge.",
            )
    return True, f"Decision(s) {', '.join(ids)} approved."


def main() -> int:
    branch = os.environ.get("HEAD_REF", "")
    title = os.environ.get("PR_TITLE", "")
    labels = [
        x.strip() for x in os.environ.get("PR_LABELS", "").split(",") if x.strip()
    ]
    ok, msg = evaluate(branch, title, labels, Path("decisions"))
    print(("PASS: " if ok else "FAIL: ") + msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
