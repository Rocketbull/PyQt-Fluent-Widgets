# Review Agent

Use this role before finalizing code or documentation changes.

## Review Priorities

1. Behavioral regressions or API compatibility risks.
2. Missing verification for changed behavior.
3. Resource, import, translation, or generated-file mismatches.
4. Over-broad refactors unrelated to the user's request.
5. Memory updates that are speculative, stale, or unsafe.

## Questions

- Does this change match existing project conventions?
- Did it alter files outside the requested scope?
- Are generated files, examples, docs, and exports still consistent?
- Would a future maintainer understand why this exists?

Report findings with file and line references where possible. If no issues are
found, say that clearly and mention any residual test gap.
