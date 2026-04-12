import json
from pathlib import Path

from devlog.models import LogEntry

# Path to JSON file in the user's home directory
DEFAULT_STORAGE_PATH = Path.home() / ".devlog" / "entries.json"


class Storage:
    """Handle the saving and loading of log entries to a JSON file."""

    def __init__(self, path: Path = DEFAULT_STORAGE_PATH) -> None:
        self.path = path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the file and directory if they don't exist."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read_all(self) -> list[LogEntry]:
        """Reads all the entries from JSON file."""
        raw = self.path.read_text(encoding="utf-8")
        data = json.loads(raw)
        return [LogEntry.model_validate(entry) for entry in data]

    def _write_all(self, entries: list[LogEntry]) -> None:
        """Writes all the entries in JSON file."""

        data = [entry.model_dump(mode="json") for entry in entries]
        self.path.write_text(
            json.dumps(data, indent=2, default=str),
            encoding="utf-8",
        )

    def add(self, entry: LogEntry) -> None:
        """Adds a new entry to the storage."""
        entries = self._read_all()
        entries.append(entry)
        self._write_all(entries)

    def get_all(self) -> list[LogEntry]:
        """Returns all the entries sorted by creation date (newest first)."""
        entries = self._read_all()
        return sorted(entries, key=lambda e: e.created_at, reverse=True)

    def get_today(self) -> list[LogEntry]:
        """Returns only the entries created today."""
        return [e for e in self.get_all() if e.is_today()]

    def search(self, query: str) -> list[LogEntry]:
        """Returns the entries that contain the query."""
        return [e for e in self.get_all() if e.matches_query(query)]

    def count(self) -> int:
        """Returns the total number of entries in storage."""
        return len(self._read_all())
