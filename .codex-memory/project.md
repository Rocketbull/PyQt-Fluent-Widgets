# Project Memory

## Repository

PyQt-Fluent-Widgets is a Python Qt widget library with examples and
documentation.

## Stable Layout

- `qfluentwidgets/`: library package.
- `examples/gallery/`: gallery application entry point and app package.
- `examples/*/*/demo.py`: standalone component demos.
- `docs/source/`: documentation source.
- `.github/workflows/`: repository automation.

## Commands

- Inspect files with `rg` and targeted reads.
- Run focused Python checks for touched modules when possible.
- For gallery behavior, start from `examples/gallery/demo.py` and
  `examples/gallery/app/view/main_window.py`.

## Cautions

- The repo contains generated resource/UI Python files. Check nearby `.qrc`,
  `.ui`, or resource patterns before editing generated output.
- Examples may rely on local relative imports and resources; preserve their
  launch paths.
