# Acceptance

## Repository structure check

Expected structure:

- `src/content_disposition_tools/` — package code
- `tests/` — pytest coverage for core cases
- `README.md` — English package documentation
- `pyproject.toml` — package metadata and test config
- `.github/workflows/ci.yml` — CI workflow
- `docs/PLAN.md` — PM/spec notes
- `LICENSE` — MIT license

## Verification completed

- Unit tests passed locally: `9 passed`
- Source distribution build passed
- Wheel build passed
- Public repository creation + push pending at authoring time of this file

## Explicit limitations

- Scope is intentionally narrow: parsing/building `Content-Disposition` only.
- No framework adapters for Django, Flask, FastAPI, requests, or httpx yet.
- Parser is aimed at common real-world headers, not exhaustive recovery from every malformed variant.
- Extended parameter decoding currently expects RFC 5987-style values and raises `ValueError` on malformed charset/value payloads.

## Unverified runtime assumptions

- CI workflow was prepared but not executed locally on GitHub Actions yet.
- Cross-version runtime behavior is based on local Python 3.12 execution plus syntax compatibility targets in metadata; remote matrix execution is still unverified until GitHub Actions runs.
- No PyPI publish/install verification was performed in this run.
