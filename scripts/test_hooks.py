#!/usr/bin/env python3
"""Self-tests for the guard hook, board status hook and decision gate. Run: python3 scripts/test_hooks.py"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / ".claude/hooks/guard.py"
STATUS = ROOT / ".claude/hooks/board_status.py"
sys.path.insert(0, str(ROOT / "scripts"))
from decision_gate import evaluate  # noqa: E402

failures = 0


def check(name: str, cond: bool) -> None:
    global failures
    print(("ok    " if cond else "FAIL  ") + name)
    failures += 0 if cond else 1


def guard(payload: dict, project: Path) -> int:
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project)}
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=env,
    ).returncode


def bash(cmd: str, project: Path) -> int:
    return guard({"tool_name": "Bash", "tool_input": {"command": cmd}}, project)


with tempfile.TemporaryDirectory() as tmp:
    proj = Path(tmp)
    (proj / ".claude").mkdir()
    (proj / ".claude/guard-patterns.txt").write_text(
        "# comment\n\\bterraform\\s+apply\\b\tNo applies.\n"
    )
    d = proj / "decisions"
    d.mkdir()
    rec = d / "D-0001-x.md"
    rec.write_text("---\nid: D-0001\nstatus: proposed\n---\n")

    check("blocks --no-verify", bash("git commit -m x --no-verify", proj) == 2)
    check("blocks force push", bash("git push --force origin feat/x", proj) == 2)
    check("blocks push to main", bash("git push origin main", proj) == 2)
    check(
        "allows push of feature branch",
        bash("git push -u origin feat/D-0001-main-thing", proj) == 0,
    )
    check("blocks cat of .pem", bash("cat ~/infra-agents-bot.pem", proj) == 2)
    check("blocks cat of .env", bash("cat .env", proj) == 2)
    check("allows cat of .env.example", bash("cat .env.example", proj) == 0)
    check(
        "blocks piped secret read",
        bash("ls && cat ./secrets/server.key | head", proj) == 2,
    )
    check("blocks secret read in subshell", bash("echo $(cat .env)", proj) == 2)
    check(
        "allows heredoc that mentions .env",
        bash("cat > notes.md <<'EOF'\na stray `.env` key\nEOF", proj) == 0,
    )
    check("allows redirect into .env.local", bash("echo X=1 > .env.local", proj) == 0)
    check(
        "blocks shell approval",
        bash(
            "sed -i 's/status: proposed/status: approved/' decisions/D-0001-x.md", proj
        )
        == 2,
    )
    check(
        "project pattern blocks terraform apply",
        bash("terraform apply -auto-approve", proj) == 2,
    )
    check("allows ordinary command", bash("pytest -m 'not live_llm' -q", proj) == 0)

    edit = {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": str(rec),
            "old_string": "status: proposed",
            "new_string": "status: approved",
        },
    }
    check("blocks Edit to approved", guard(edit, proj) == 2)
    edit["tool_input"]["new_string"] = "status: board-reviewed"
    check("allows Edit to board-reviewed", guard(edit, proj) == 0)
    write = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(rec),
            "content": "---\nstatus: rejected\n---\n",
        },
    }
    check("blocks Write to rejected", guard(write, proj) == 2)
    write["tool_input"]["content"] = (
        "---\nstatus: proposed\napproved_by: someone\n---\n"
    )
    check("blocks Write filling approved_by", guard(write, proj) == 2)
    rec.write_text("---\nstatus: approved\napproved_by: owner\n---\nbody\n")
    write["tool_input"]["content"] = (
        "---\nstatus: approved\napproved_by: owner\n---\nbody\n## Outcome\n"
    )
    check(
        "allows editing an already-approved record without changing approval",
        guard(write, proj) == 0,
    )
    new_rec = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(d / "D-0002-new.md"),
            "content": "---\nstatus: proposed   # proposed | approved | rejected\napproved_by:\napproved_on:\n---\n",
        },
    }
    check("allows creating a record with empty approved_by", guard(new_rec, proj) == 0)
    check(
        "allows shell-created record with empty approved_by",
        bash(
            "cat > decisions/D-0002-new.md <<'EOF'\nstatus: proposed\napproved_by:\napproved_on:\nEOF",
            proj,
        )
        == 0,
    )
    other = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": str(proj / "notes.md"),
            "content": "status: approved",
        },
    }
    check("ignores non-decision files", guard(other, proj) == 0)
    check(
        "bad stdin fails open",
        subprocess.run(
            [sys.executable, str(GUARD)],
            input="not json",
            text=True,
            capture_output=True,
        ).returncode
        == 0,
    )

    (d / "BUSINESS.md").write_text(
        "---\nrevenue_target: 2000\nrevenue_deadline: unset\n"
        "token_budget_monthly_usd: 20\ntoken_spend_month_usd: unknown\n---\n"
    )
    rec.write_text("---\nid: D-0001\nstatus: board-reviewed\n---\n")
    out = subprocess.run(
        [sys.executable, str(STATUS)],
        text=True,
        capture_output=True,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(proj)},
    ).stdout
    check("status lists unset fields", "revenue_deadline" in out)
    check("status flags unknown spend", "unknown" in out)
    check("status lists awaiting decision", "D-0001 (board-reviewed)" in out)

    check("gate passes tier-0 branch", evaluate("fix/typo", "", [], d)[0])
    check(
        "gate fails unclassified branch",
        not evaluate("claude/abc", "Add thing", [], d)[0],
    )
    check(
        "gate passes tier-0 label",
        evaluate("claude/abc", "Add thing", ["tier-0"], d)[0],
    )
    check("gate fails unapproved decision", not evaluate("feat/D-0001-x", "", [], d)[0])
    rec.write_text("---\nid: D-0001\nstatus: approved\n---\n")
    check("gate passes approved decision", evaluate("feat/D-0001-x", "", [], d)[0])
    check("gate fails missing record", not evaluate("feat/D-0002-y", "", [], d)[0])

print(f"\n{failures} failure(s)")
sys.exit(1 if failures else 0)
