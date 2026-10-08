# Working rules

- **Plan only when it pays.** Plan first for Tier 1 and 2 work, or changes touching more than about 3 files or a public interface. Otherwise just do it. If a task goes sideways, stop and re-plan.
- **Bug reports:** fix them without asking for hand-holding, unless the fix is Tier 1 or 2.
- **Subagents** cost tokens. Use one only when it saves more context than it costs, one focused task each. Never for a lookup you can do in one or two tool calls.
- **Verify before done:** run the project's checks (see CLAUDE.md, Commands), re-read every edited file, and name any adjacent code the change could break.
- **Simplicity:** make the smallest change that solves the root cause. No temporary fixes.
- **Style:** no comments unless the why is non-obvious. No emojis unless asked. Read before writing; never assume structure.
- **Corrections:** when the owner corrects you, add one line to `.claude/rules/lessons.md` with the rule that would have prevented it. Keep that file under 40 lines; merge duplicates instead of appending.
