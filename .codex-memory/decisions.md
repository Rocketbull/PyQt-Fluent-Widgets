# Decision Memory

## 2026-04-25: Repo-Local AI Workflow

Adopt a markdown-based AI workflow in the repository instead of adding runtime
dependencies. The workflow uses:

- `.codex-workflow.md` as the primary operating manual.
- `.codex-agents/` for lightweight role definitions.
- `.codex-memory/` for durable project memory.
- `.codex-memory/guard.md` as the required safety gate for memory writes.

Rationale: the user asked for an Andrej Karpathy-style AI workflow with agents,
memory, reflection, and memory guard. Karpathy's public LLM-wiki pattern favors
plain, accumulating knowledge files that agents can read and maintain.
