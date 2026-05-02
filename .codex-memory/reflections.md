# Reflection Memory

Use this file for compact, dated lessons that future sessions should remember.
Each entry should pass `guard.md`.

## Template

```md
## YYYY-MM-DD: Short Title

- Context: what task produced this lesson.
- Lesson: what should future agents do differently or remember.
- Evidence: source file, command, test, or explicit user instruction.
```

## 2026-04-25: Initial AI Workflow Added

- Context: user requested an Andrej Karpathy-style AI workflow with agents,
  memory, reflection, and memory guard.
- Lesson: keep the workflow as plain markdown so it is inspectable, portable,
  and easy for future AI sessions to load selectively.
- Evidence: `.codex-workflow.md`, `.codex-agents/`, `.codex-memory/`.

## 2026-04-25: Production Widgets Added In Groups

- Context: user asked to add production-quality GUI framework widgets, then
  continue through state, form, data grid, charting, workspace, and gallery
  navigation work.
- Lesson: when adding widget families, pair each group with exports, standalone
  examples, and gallery pages/navigation so the library remains discoverable.
- Evidence: `qfluentwidgets/components/widgets/state_widget.py`,
  `form.py`, `data_grid.py`, `chart.py`, `workspace.py`, and gallery pages
  under `examples/gallery/app/view/`.
