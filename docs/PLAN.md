# PM + Spec Notes

## Chosen stack

Python

## Product idea

A tiny dependency-free helper library for parsing and building HTTP `Content-Disposition` headers, with first-class support for Unicode filenames via `filename*`.

## Why this idea won

- Small enough for a one-run MVP.
- Useful in real HTTP/file-download workflows.
- Easy to explain and verify.
- Clean public API with low maintenance burden.

## MVP

- Parse `Content-Disposition` header values.
- Extract effective filename.
- Prefer `filename*` over `filename`.
- Build `attachment`/`inline` header values.
- Generate ASCII fallback + RFC 5987 extended filename.
- Ship tests, README, and CI.

## Developer experience

- One import path.
- Dependency-free.
- Minimal API surface.
- Dataclass parse result for clarity.

## README structure

1. What it does
2. Why it exists
3. Installation
4. Quick start
5. API reference
6. DX goals
7. Architecture
8. Development
9. Release checklist
10. Limitations

## Release checklist

- [x] Pick package idea and scope MVP
- [x] Specify API and architecture
- [x] Implement code
- [x] Write tests
- [x] Write README in English
- [x] Prepare CI workflow
- [x] Push repository

Note: the CI workflow had to be kept under `omitted/ci.yml` in the published repository because the available GitHub token could not push workflow files without extra `workflow` scope.
