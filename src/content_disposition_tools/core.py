from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
import unicodedata
from urllib.parse import quote, unquote_to_bytes

_TOKEN_RE = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
_ATTR_CHAR_SAFE = "!#$&+-.^_`|~"


@dataclass(frozen=True)
class ParsedContentDisposition:
    disposition: str
    params: dict[str, str]
    filename: str | None = None
    filename_source: str | None = None


def _split_parts(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    in_quotes = False
    escape = False
    for ch in value:
        if escape:
            current.append(ch)
            escape = False
            continue
        if ch == "\\" and in_quotes:
            escape = True
            current.append(ch)
            continue
        if ch == '"':
            in_quotes = not in_quotes
            current.append(ch)
            continue
        if ch == ";" and not in_quotes:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    if current:
        parts.append("".join(current).strip())
    return [part for part in parts if part]


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        inner = value[1:-1]
        result: list[str] = []
        escape = False
        for ch in inner:
            if escape:
                result.append(ch)
                escape = False
            elif ch == "\\":
                escape = True
            else:
                result.append(ch)
        if escape:
            result.append("\\")
        return "".join(result)
    return value


def _decode_extended_value(value: str) -> str:
    try:
        charset, _language, encoded = value.split("'", 2)
    except ValueError as exc:
        raise ValueError("Invalid RFC 5987 extended parameter") from exc
    charset = charset or "utf-8"
    raw = unquote_to_bytes(encoded)
    try:
        return raw.decode(charset)
    except LookupError as exc:
        raise ValueError(f"Unknown charset: {charset}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Could not decode value using charset {charset}") from exc


def parse_content_disposition(value: str) -> ParsedContentDisposition:
    if not value or not value.strip():
        raise ValueError("Content-Disposition value must not be empty")

    parts = _split_parts(value)
    disposition = parts[0].strip().lower()
    if not _TOKEN_RE.match(disposition):
        raise ValueError(f"Invalid disposition token: {disposition!r}")

    params: dict[str, str] = {}
    filename = None
    filename_source = None

    for part in parts[1:]:
        if "=" not in part:
            raise ValueError(f"Invalid parameter segment: {part!r}")
        key, raw = part.split("=", 1)
        key = key.strip().lower()
        raw = raw.strip()
        if not _TOKEN_RE.match(key.rstrip("*")):
            raise ValueError(f"Invalid parameter name: {key!r}")
        params[key] = _unquote(raw)

    if "filename*" in params:
        filename = _decode_extended_value(params["filename*"])
        filename_source = "filename*"
    elif "filename" in params:
        filename = params["filename"]
        filename_source = "filename"

    return ParsedContentDisposition(
        disposition=disposition,
        params=params,
        filename=filename,
        filename_source=filename_source,
    )


def to_ascii_fallback(filename: str, replacement: str = "download") -> str:
    normalized = unicodedata.normalize("NFKD", filename)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_only = re.sub(r"[\r\n]+", " ", ascii_only)
    ascii_only = re.sub(r"[^ !#$%&+.^_`|~'(){}\[\],;=@0-9A-Za-z-]+", "_", ascii_only)
    ascii_only = re.sub(r"\s+", " ", ascii_only).strip(" .")
    return ascii_only or replacement


def quote_filename(filename: str) -> str:
    sanitized = filename.replace("\\", "\\\\").replace('"', r'\"')
    sanitized = sanitized.replace("\r", " ").replace("\n", " ")
    return f'"{sanitized}"'


def build_content_disposition(
    disposition: str = "attachment",
    filename: str | None = None,
    fallback_ascii: bool = True,
) -> str:
    disposition = disposition.strip().lower()
    if not _TOKEN_RE.match(disposition):
        raise ValueError(f"Invalid disposition token: {disposition!r}")

    if filename is None:
        return disposition

    pieces = [disposition]
    ascii_filename = to_ascii_fallback(filename) if fallback_ascii else filename
    pieces.append(f"filename={quote_filename(ascii_filename)}")

    try:
        filename.encode("ascii")
    except UnicodeEncodeError:
        encoded = quote(filename, safe=_ATTR_CHAR_SAFE)
        pieces.append(f"filename*=UTF-8''{encoded}")

    return "; ".join(pieces)
