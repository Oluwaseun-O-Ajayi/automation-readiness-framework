# Changelog

## 2.0.0 (2026-10)

Version 2 turns the scoring script into an installable package,
`automation_readiness`. The `src/` modules were replaced; code written for
version 1 needs its imports updated (see the README). With default settings the
overall score is unchanged from version 1.

### Added
- Optional domain weights (normalized; equal by default, which reproduces version 1).
- Weakest-link rule: a domain below the critical threshold (3 by default) caps the
  classification at Early Stage and is reported as limiting. Configurable or off.
- Ranked priorities with a recommended action for each domain below the target score.
- `assess_many()` to rank several workflows; `read_workflows()` and
  `write_workflows()` for CSV input and output.
- `weight_sensitivity()` to test how stable a ranking is when the weights change.
- Input validation, a test suite and continuous integration on Linux, macOS and Windows.
- Five illustrative workflows (`data/example_workflows.csv`) and four reproducible
  case studies (`examples/CASE_STUDIES.md`).
- MIT license file.

## 1.0.1 (2026-07)

- Maintenance and archival release: metadata and citation updates for Zenodo.

## 1.0.0 (2026-07)

- Initial release: six readiness domains scored 0 to 10, unweighted overall score,
  five readiness categories and a printed report.
