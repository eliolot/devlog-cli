import pytest

from devlog.models import LogEntry


@pytest.fixture
def simple_entry() -> LogEntry:
    """Base LogEntry reusable in tests."""
    return LogEntry(content="Test Note")


@pytest.fixture
def entry_with_tags() -> LogEntry:
    """LogEntry with tags, reusable in tests."""
    return LogEntry(content="Study of design pattern", tags=["python", "architecture"])


@pytest.fixture
def entry_list() -> list[LogEntry]:
    """List of LogEntry objects to test operation on collections."""
    return [
        LogEntry(content="First Note", tags=["python"]),
        LogEntry(content="Second Note", tags=["git"]),
        LogEntry(content="Note on advanced Python", tags=["python", "advanced"]),
    ]
