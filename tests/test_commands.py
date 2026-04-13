from pathlib import Path

import pytest
from typer.testing import CliRunner

from devlog.cli import app
from devlog.models import LogEntry
from devlog.storage import Storage

runner = CliRunner()


@pytest.fixture
def storage(tmp_path: Path) -> Storage:
    """Storage instance with a temporary file."""
    return Storage(path=tmp_path / "test_entries.json")


@pytest.fixture
def populated_storage(tmp_path: Path) -> Storage:
    s = Storage(path=tmp_path / "entries.json")
    s.add(LogEntry(content="Studied async/await", tags=["python"]))
    s.add(LogEntry(content="Fixed a nasty bug", tags=["debug"]))
    s.add(LogEntry(content="Reviewed a PR", tags=["git"]))
    return s


# -------------------------------------------------------------------------
# Test: add
# -------------------------------------------------------------------------


def test_add_command_success(storage: Storage, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("devlog.commands.add.Storage", lambda: storage)
    result = runner.invoke(app, ["add", "test note"])

    assert result.exit_code == 0
    assert "✓" in result.output
    assert storage.count() == 1


def test_add_command_with_tags(
    storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.add.Storage", lambda: storage)
    result = runner.invoke(
        app, ["add", "note with tags", "--tag", "python", "--tag", "cli"]
    )

    assert result.exit_code == 0
    entries = storage.get_all()
    assert entries[0].tags == ["python", "cli"]


def test_add_command_empty_content(
    storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.add.Storage", lambda: storage)
    result = runner.invoke(app, ["add", ""])

    assert result.exit_code != 0


# ------------------------------------------------------------------------
# Test: today
# ------------------------------------------------------------------------


def test_today_command_no_entries(
    storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.today.Storage", lambda: storage)
    result = runner.invoke(app, ["today"])

    assert result.exit_code == 0
    assert "No entries today" in result.output


def test_today_command_with_entries(
    storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    storage.add(LogEntry(content="Morning note"))
    monkeypatch.setattr("devlog.commands.today.Storage", lambda: storage)
    result = runner.invoke(app, ["today"])

    assert result.exit_code == 0
    assert "Morning note" in result.output


# ------------------------------------------------------------------------
# Test: search
# ------------------------------------------------------------------------


def test_search_command_finds_results(
    populated_storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.search.Storage", lambda: populated_storage)
    result = runner.invoke(app, ["search", "async"])

    assert result.exit_code == 0
    assert "async" in result.output.lower()


def test_search_command_no_results(
    populated_storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.search.Storage", lambda: populated_storage)
    result = runner.invoke(app, ["search", "rust"])

    assert result.exit_code == 0
    assert "No entries found" in result.output


# ------------------------------------------------------------------------
# Test: stats
# ------------------------------------------------------------------------


def test_stats_command_no_entries(
    storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.stats.Storage", lambda: storage)
    result = runner.invoke(app, ["stats"])

    assert result.exit_code == 0
    assert "No entries yet" in result.output


def test_stats_command_with_entries(
    populated_storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.stats.Storage", lambda: populated_storage)
    result = runner.invoke(app, ["stats"])

    assert result.exit_code == 0
    assert "3" in result.output  # total entries


# ------------------------------------------------------------------------
# Test: export
# ------------------------------------------------------------------------


def test_export_command_markdown(
    populated_storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.export.Storage", lambda: populated_storage)
    result = runner.invoke(app, ["export", "--format", "md"])

    assert result.exit_code == 0
    assert "# devlog export" in result.output


def test_export_command_json(
    populated_storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    import json

    monkeypatch.setattr("devlog.commands.export.Storage", lambda: populated_storage)
    result = runner.invoke(app, ["export", "--format", "json"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 3


def test_export_command_no_entries(
    storage: Storage, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("devlog.commands.export.Storage", lambda: storage)
    result = runner.invoke(app, ["export"])

    assert result.exit_code == 1
