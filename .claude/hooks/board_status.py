#!/usr/bin/env python3
"""SessionStart hook: print a short factual board status into Claude's context.

Reads decisions/BUSINESS.md and decisions/D-*.md frontmatter. Prints nothing if the
project has no decisions/ directory. Never fails the session.
"""
from __future__ import annotations

import datetime as dt
import os
import re
from pathlib import Path

STALE_DAYS = 7


def frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text()
    except OSError:
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.split("#", 1)[0].strip().strip('"')
    return out


def as_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def as_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()) / "decisions"
    if not root.is_dir():
        return
    today = dt.date.today()
    lines = ["Board status (from decisions/):"]

    biz = frontmatter(root / "BUSINESS.md")
    if not biz:
        lines.append("- decisions/BUSINESS.md is missing or has no frontmatter; business goals are undefined.")
    else:
        unset = [k for k, v in biz.items() if v.lower() in ("", "unset", "unknown", "tbd")]
        if unset:
            lines.append(f"- BUSINESS.md fields not set: {', '.join(unset)}.")
        budget = as_float(biz.get("token_budget_monthly_usd"))
        spent = as_float(biz.get("token_spend_month_usd"))
        updated = as_date(biz.get("token_spend_updated"))
        if spent is None or updated is None or (today - updated).days > STALE_DAYS:
            lines.append(
                f"- Token spend this month is not recorded in the last {STALE_DAYS} days, so it is unknown. "
                "Paid runs (live-LLM tests, real-agent runs, board runs on API billing) need owner confirmation."
            )
        elif budget:
            lines.append(f"- Token spend recorded {updated}: US${spent:g} of US${budget:g}/month.")
            if spent >= 0.8 * budget:
                lines.append("- Spend is at or above 80% of budget. Only Tier 0 work without paid calls.")
        lines.append(
            f"- Revenue: {biz.get('revenue_to_date', '?')} of target {biz.get('revenue_target', '?')} "
            f"{biz.get('revenue_currency', '')} by {biz.get('revenue_deadline', '?')}; "
            f"paying clients: {biz.get('paying_clients', '?')}."
        )

    awaiting, approved, due = [], [], []
    for f in sorted(root.glob("D-*.md")):
        fm = frontmatter(f)
        status = fm.get("status", "").lower()
        m = re.match(r"D-\d+", f.stem)
        did = fm.get("id") or (m.group(0) if m else f.stem)
        if status in ("proposed", "board-reviewed"):
            awaiting.append(f"{did} ({status})")
        elif status == "approved":
            approved.append(did)
        elif status == "shipped":
            rd = as_date(fm.get("review_date"))
            if rd and rd <= today:
                due.append(f"{did} (review date {rd})")
    lines.append(f"- Awaiting owner decision: {', '.join(awaiting) or 'none'}.")
    lines.append(f"- Approved, not yet shipped: {', '.join(approved) or 'none'}.")
    lines.append(f"- Outcome reviews due: {', '.join(due) or 'none'}.")
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception:  # a status banner must never break session start
        pass
