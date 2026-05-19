import pytest

from content_disposition_tools import (
    ParsedContentDisposition,
    build_content_disposition,
    parse_content_disposition,
    quote_filename,
    to_ascii_fallback,
)


def test_parse_simple_filename():
    parsed = parse_content_disposition('attachment; filename="report.csv"')
    assert parsed == ParsedContentDisposition(
        disposition="attachment",
        params={"filename": "report.csv"},
        filename="report.csv",
        filename_source="filename",
    )


def test_parse_prefers_extended_filename():
    parsed = parse_content_disposition(
        "attachment; filename=resume.txt; filename*=UTF-8''r%C3%A9sum%C3%A9.txt"
    )
    assert parsed.filename == "résumé.txt"
    assert parsed.filename_source == "filename*"


def test_parse_handles_quoted_semicolon():
    parsed = parse_content_disposition('inline; filename="budget;2026.csv"')
    assert parsed.filename == "budget;2026.csv"


def test_parse_rejects_invalid_segments():
    with pytest.raises(ValueError):
        parse_content_disposition("attachment; broken")


def test_build_ascii_header():
    header = build_content_disposition(filename="report.csv")
    assert header == 'attachment; filename="report.csv"'


def test_build_unicode_header_with_fallback_and_extended_value():
    header = build_content_disposition(filename="résumé 2026.txt")
    assert header == (
        'attachment; filename="resume 2026.txt"; '
        "filename*=UTF-8''r%C3%A9sum%C3%A9%202026.txt"
    )


def test_ascii_fallback_has_default_replacement():
    assert to_ascii_fallback("你好") == "download"


def test_quote_filename_escapes_quotes_and_backslashes():
    assert quote_filename('say "hi" \\ ok.txt') == '"say \\"hi\\" \\\\ ok.txt"'


def test_build_rejects_invalid_disposition_token():
    with pytest.raises(ValueError):
        build_content_disposition(disposition="bad token")
