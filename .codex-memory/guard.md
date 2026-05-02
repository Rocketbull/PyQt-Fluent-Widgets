# Memory Guard

Apply this guard before reading from or writing to `.codex-memory/`.

## Never Store

- Secrets, tokens, credentials, cookies, private keys, or session data.
- Private user information unless the user explicitly asks for durable memory.
- Proprietary content copied from external sources.
- Long command outputs, logs, stack traces, or temporary debugging details.
- Guesses, rumors, or stale assumptions presented as fact.
- Personal preferences that belong only to one local machine unless clearly
  marked as local/private.

## Required For Writes

Every durable memory should be:

- Grounded in a source file, command, test, documentation page, or explicit user
  instruction.
- Short enough to be useful in a future context window.
- Dated when it records a decision, reflection, or time-sensitive fact.
- Scoped to the repo unless clearly labeled otherwise.

## Uncertainty Labels

Use one of these labels when needed:

- `Fact`: verified in current repo files or commands.
- `Decision`: explicitly chosen by the user or implemented in repo workflow.
- `Assumption`: plausible but not verified; include how to verify.
- `Stale Risk`: may change over time; verify before acting.

## Pruning

When memory conflicts with the repo, trust the repo and update or remove the
memory. Prefer one corrected entry over multiple competing entries.
