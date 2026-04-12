from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from devlog.models import LogEntry
from devlog.storage import Storage


@pytest.fixture
def tmp_storage(tmp_path: Path) -> Storage:
    """Temporary folder for storage."""
    return Storage(path=tmp_path / "test_entries.json")


# --------------------------------------------------------------------------
# Test: Initialization
# --------------------------------------------------------------------------


def test_storage_create_file_if_not_exists(tmp_path: Path) -> None:
    """Storage creates the JSON file at the first initialization."""
    storage_path = tmp_path / "subdir" / "entries.json"
    Storage(path=storage_path)

    assert storage_path.exists()
    assert storage_path.read_text() == "[]"


def test_storage_not_overwrite_existing_file(tmp_storage: Storage) -> None:
    """Storage does not cancel existing data when initialized."""
    entry = LogEntry(content="Existing note")
    tmp_storage.add(entry)

    # Re-initialize with the same path
    storage2 = Storage(path=tmp_storage.path)
    assert storage2.count() == 1


# --------------------------------------------------------------------------
# Test: add and get_all
# --------------------------------------------------------------------------


def test_add_persisting_entry(tmp_storage: Storage) -> None:
    """A entry added can be retrieved with get_all."""
    entry = LogEntry(content="I have learned Pydantic")
    tmp_storage.add(entry)

    all_entries = tmp_storage.get_all()
    assert len(all_entries) == 1
    assert all_entries[0].content == "I have learned Pydantic"


def test_get_all_sorted_by_date(tmp_storage: Storage) -> None:
    """get_all returns entries from the newest to the oldest."""
    old = LogEntry(
        content="old Note",
        created_at=datetime.now(UTC) - timedelta(hours=2),
    )
    new = LogEntry(content="new Note")

    tmp_storage.add(old)
    tmp_storage.add(new)

    entries = tmp_storage.get_all()
    assert entries[0].content == "new Note"
    assert entries[1].content == "old Note"


def test_corret_count(tmp_storage: Storage) -> None:
    """count returns the exact number of entries."""
    tmp_storage.add(LogEntry(content="First"))
    tmp_storage.add(LogEntry(content="Second"))
    tmp_storage.add(LogEntry(content="Third"))

    assert tmp_storage.count() == 3


# --------------------------------------------------------------------------
# Test: get_today
# --------------------------------------------------------------------------


def test_get_today_returns_only_today_entries(tmp_storage: Storage) -> None:
    """get_today correctly filter today's entries."""

    today = LogEntry(content="Today's note")
    yesterday = LogEntry(
        content="Yesterday's note",
        created_at=datetime.now(UTC) - timedelta(days=1),
    )

    tmp_storage.add(today)
    tmp_storage.add(yesterday)

    today_entries = tmp_storage.get_today()
    assert len(today_entries) == 1
    assert today_entries[0].content == "Today's note"


# --------------------------------------------------------------------------
# Test: search
# --------------------------------------------------------------------------


def test_search_finds_by_content(tmp_storage: Storage) -> None:
    tmp_storage.add(LogEntry(content="I have studied async/await"))
    tmp_storage.add(LogEntry(content="I have done the refactoring"))

    results = tmp_storage.search("async")
    assert len(results) == 1
    assert results[0].content == "I have studied async/await"


def test_search_finds_by_tags(tmp_storage: Storage) -> None:
    tmp_storage.add(LogEntry(content="Study session", tags=["python"]))
    tmp_storage.add(LogEntry(content="Other note", tags=["git"]))

    results = tmp_storage.search("python")
    assert len(results) == 1
    assert results[0].content == "Study session"


def test_search_no_results(tmp_storage: Storage) -> None:
    tmp_storage.add(LogEntry(content="Generic note"))

    results = tmp_storage.search("rust")
    assert results == []
