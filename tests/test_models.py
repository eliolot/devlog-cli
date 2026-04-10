from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from devlog.models import LogEntry

# ------------------------------------------------------------
# Test: base creation
# ------------------------------------------------------------


def test_log_entry_creation_with_valid_content() -> None:
    """LogEntry correctly created with valid content."""
    # Arrange + Act
    entry = LogEntry(content="I fixed a bug in the code")

    # Assert
    assert entry.content == "I fixed the parser".replace(
        "the parser", "a bug in the code"
    )
    assert entry.tags == []
    assert entry.id is not None
    assert entry.created_at is not None


def test_log_entry_creation_with_tags() -> None:
    """LogEntry correctly created with tags."""
    # Arrange + Act
    entry = LogEntry(content="I added a new feature.", tags=["python", "learning"])

    # Assert
    assert entry.tags == ["python", "learning"]


def test_log_entry_unique_id() -> None:
    "two LogEntry instances should have different ids."
    entry1 = LogEntry(content="First entry")
    entry2 = LogEntry(content="Second note")

    assert entry1.id != entry2.id


# ------------------------------------------------------------
# Test: Pydantic validation
# ------------------------------------------------------------


def test_log_entry_creation_with_empty_content() -> None:
    """LogEntry with no content raises ValidationError."""
    with pytest.raises(ValidationError):
        LogEntry(content="")


def test_log_entry_creation_with_too_long_content() -> None:
    """a LogEntry with content > 2000 characters raises ValidationError."""
    with pytest.raises(ValidationError):
        LogEntry(content="x" * 2001)


# ------------------------------------------------------------
# Test: method matches_query
# ------------------------------------------------------------


def test_matches_query_finds_in_content() -> None:
    entry = LogEntry(content="I have studied async/await in Python")
    assert entry.matches_query("async") is True


def test_matches_query_finds_in_tags() -> None:
    entry = LogEntry(content="Study session", tags=["python", "learning"])
    assert entry.matches_query("learning") is True


def test_matches_query_case_insensitive() -> None:
    entry = LogEntry(content="I have used FastAPI today")

    assert entry.matches_query("fastapi") is True
    assert entry.matches_query("FASTAPI") is True


def test_matches_query_not_found() -> None:
    entry = LogEntry(content="I have studied Rust")

    assert entry.matches_query("python") is False


# ------------------------------------------------------------
# Test: method is_today
# ------------------------------------------------------------


def test_is_today_true_for_just_created_note() -> None:
    entry = LogEntry(content="Note now")

    assert entry.is_today() is True


def test_is_today_false_for_old_note() -> None:
    yesterday = datetime.now(UTC) - timedelta(days=1)
    entry = LogEntry(content="Note yesterday", created_at=yesterday)

    assert entry.is_today() is False
