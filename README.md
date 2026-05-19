# content-disposition-tools

Small Python helpers for parsing and building HTTP `Content-Disposition` headers.

This package focuses on a narrow but annoying problem: handling download filenames correctly, including Unicode filenames via `filename*` (RFC 5987 / RFC 6266), while keeping a friendly ASCII fallback for older clients.

## Why this exists

When applications generate file downloads, they often need to:

- parse incoming `Content-Disposition` headers from upstream services;
- extract the effective filename while preferring `filename*` over `filename`;
- build safe `attachment` headers for Unicode filenames;
- keep the implementation tiny and dependency-free.

`content-disposition-tools` provides that in a small, testable package.

## Installation

```bash
pip install content-disposition-tools
```

## Quick start

```python
from content_disposition_tools import (
    build_content_disposition,
    parse_content_disposition,
)

header = build_content_disposition(filename="résumé.pdf")
print(header)
# attachment; filename="resume.pdf"; filename*=UTF-8''r%C3%A9sum%C3%A9.pdf

parsed = parse_content_disposition(header)
print(parsed.filename)
# résumé.pdf
```

## API

### `parse_content_disposition(value: str) -> ParsedContentDisposition`

Parses a header value such as:

```text
attachment; filename="report.csv"
```

Returns:

- `disposition`: normalized lower-case disposition token such as `attachment` or `inline`;
- `params`: parsed parameter dictionary;
- `filename`: effective filename, preferring `filename*` when present;
- `filename_source`: either `filename`, `filename*`, or `None`.

### `build_content_disposition(disposition="attachment", filename=None, fallback_ascii=True) -> str`

Builds a safe header string.

Examples:

```python
build_content_disposition(filename="report.csv")
# attachment; filename="report.csv"

build_content_disposition(filename="résumé 2026.txt")
# attachment; filename="resume 2026.txt"; filename*=UTF-8''r%C3%A9sum%C3%A9%202026.txt
```

### `to_ascii_fallback(filename: str, replacement="download") -> str`

Creates a simple ASCII fallback filename by normalizing and stripping unsupported characters.

### `quote_filename(filename: str) -> str`

Quotes and escapes a filename for use in a `filename="..."` parameter.

## DX goals

- no runtime dependencies;
- one-file core implementation;
- explicit, predictable return types;
- useful defaults for web backends, API gateways, and download proxies.

## Package architecture

```text
src/content_disposition_tools/
  __init__.py
  core.py
tests/
  test_core.py
```

## Development

```bash
python -m venv .venv
. .venv/bin/activate
pip install -U pip pytest build
pip install -e .
pytest
python -m build
```

## Release checklist

- [x] Define MVP around parsing + building only
- [x] Keep implementation dependency-free
- [x] Add tests for ASCII, Unicode, quoting, invalid input
- [x] Add CI workflow for tests
- [x] Document API and scope in English
- [ ] Publish to PyPI (not part of this run)

## Limitations

- This package intentionally covers the common `Content-Disposition` use cases and not every edge case in the RFC ecosystem.
- Parameter ordering is preserved only in the generated output, not as a distinct parse artifact.
- No direct framework integrations are included yet.

## License

MIT
