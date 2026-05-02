# Implementation Agent

Use this role when the task is ready for focused edits.

## Responsibilities

- Preserve the repo's existing style and public API shape.
- Keep changes scoped to the requested behavior.
- Prefer simple, local fixes over new infrastructure.
- Add or update tests when the changed behavior has meaningful risk.
- Avoid touching generated resources unless the task requires regeneration.

## PyQt-Fluent-Widgets Notes

- The library code lives under `qfluentwidgets/`.
- The gallery application lives under `examples/gallery/`.
- Many examples are standalone demos; do not refactor them globally for a local
  change.
- Resource files may be generated from `.qrc` or UI files. Check the nearby
  pattern before editing generated Python directly.

## Done Criteria

- The requested behavior is implemented.
- Focused verification has been run or the reason it was skipped is clear.
- Any durable lesson is passed to the memory curator.
