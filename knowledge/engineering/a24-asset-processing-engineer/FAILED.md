# FAILED — A24 (never delete entries)

## X-a24-001: pytest / jsonschema based test suite (2026-11-28)
- **Tried:** planned pytest + jsonschema validation of sidecars.
- **Result:** neither module exists in `.venv-analysis`; no installs allowed.
- **Why it failed:** environment constraint (high confidence).
- **Lesson / do instead:** unittest (pytest-compatible) plus a small subset validator in the test file; full Draft 2020-12 validation is not performed.
- **Revisit if:** director approves adding jsonschema/pytest to the pinned setup.
