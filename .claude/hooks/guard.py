#!/usr/bin/env python3
"""PreToolUse guard for Claude Code.

Exit code 2 blocks the tool call and shows stderr to Claude. Any other failure
(bad input, missing file) exits 0 so a broken guard never wedges a session, which
means the guard fails open: CI is the backstop, not this script.

What it blocks:
  - Claude setting a decision record to approved / rejected / killed (owner only)
  - bypassing git hooks (--no-verify), force pushes, pushes straight to main/master
  - shell reads of secret files (.pem, .key, .env, aws credentials)
  - anything matched by .claude/guard-patterns.txt (project-specific, regex<TAB>reason)
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

OWNER_ONLY = re.compile(
    r"^[ \t]*(status:[ \t]*(approved|rejected|killed)\b|approved_by:[ \t]*[^\s#])",
    re.IGNORECASE | re.MULTILINE,
)
SHELL_OWNER_ONLY = re.compile(
    r"(status:[ \t]*(approved|rejected|killed)\b|approved_by:[ \t]*[^\s#'\"])",
    re.IGNORECASE,
)
SHELL_RULES = [
    (
        re.compile(r"--no-verify\b"),
        "Bypassing git hooks is not allowed. Fix the failing check instead.",
    ),
    (
        re.compile(r"\bgit\s+push\b.*(\s--force(-with-lease)?\b|\s-f\b|\s\+\S)"),
        "Force pushes are not allowed from Claude. Ask the owner to do it if it is really needed.",
    ),
    (
        re.compile(r"\bgit\s+push\b.*(\s|:)(main|master)(\s|$)"),
        "Pushing to main/master is not allowed. Push a branch and open a PR.",
    ),
]
# A read command at the start of a line or after | ; & ( ` $( , and its arguments up to
# the next redirect or separator. Heredoc bodies and redirect targets are not arguments.
SECRET_READ = re.compile(
    r"(?:^|[|;&(`]|\$\()\s*(?:sudo\s+)?(cat|less|more|head|tail|bat|strings|xxd|base64|cp|scp|open)\b"
    r"([^|;&<>\n]*)",
    re.MULTILINE,
)
SECRET_PATH = re.compile(
    r"(\.pem\b|\.key\b|(?<![\w.-])\.env(?!\.(example|sample|template))\b|aws/credentials)"
)


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def project_dir() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def is_decision_record(path: str) -> bool:
    p = Path(path)
    return p.suffix == ".md" and "decisions" in p.parts and p.name.startswith("D-")


def markers(text: str) -> set[str]:
    return {
        re.sub(r"\s+", " ", m.group(0).strip().lower())
        for m in OWNER_ONLY.finditer(text or "")
    }


def owner_only_change(old: str, new: str) -> bool:
    return bool(markers(new) - markers(old))


def check_file_edit(tool: str, ti: dict) -> None:
    path = ti.get("file_path") or ti.get("notebook_path") or ""
    if not is_decision_record(path):
        return
    msg = (
        f"{Path(path).name}: only the owner can set a decision to approved, rejected or killed, "
        "or fill approved_by. Leave status as proposed or board-reviewed and tell the owner it is ready."
    )
    if tool == "Write":
        try:
            existing = Path(path).read_text()
        except OSError:
            existing = ""
        if owner_only_change(existing, ti.get("content", "")):
            block(msg)
    elif tool == "Edit":
        if owner_only_change(ti.get("old_string", ""), ti.get("new_string", "")):
            block(msg)
    elif tool == "MultiEdit":
        for e in ti.get("edits", []):
            if owner_only_change(e.get("old_string", ""), e.get("new_string", "")):
                block(msg)


def project_patterns() -> list[tuple[re.Pattern, str]]:
    f = project_dir() / ".claude" / "guard-patterns.txt"
    rules = []
    try:
        lines = f.read_text().splitlines()
    except OSError:
        return rules
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#") or "\t" not in line:
            continue
        pattern, reason = line.split("\t", 1)
        try:
            rules.append((re.compile(pattern), reason.strip()))
        except re.error:
            continue
    return rules


def check_bash(cmd: str) -> None:
    if "decisions/" in cmd and SHELL_OWNER_ONLY.search(cmd):
        block(
            "Only the owner can approve, reject or kill a decision record, including via the shell."
        )
    for m in SECRET_READ.finditer(cmd):
        if SECRET_PATH.search(m.group(2)):
            block(
                "Reading secret files is not allowed. Ask the owner for the specific non-secret value you need."
            )
    for rx, reason in SHELL_RULES + project_patterns():
        if rx.search(cmd):
            block(reason)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}
    if tool == "Bash":
        check_bash(ti.get("command", ""))
    elif tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        check_file_edit(tool, ti)


if __name__ == "__main__":
    main()
