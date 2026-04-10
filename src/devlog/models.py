from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    """This represents a single note in dev journal."""

    id: UUID = Field(default_factory=uuid4)
    content: str = Field(min_length=1, max_length=2000)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def matches_query(self, query: str) -> bool:
        """Returns True if the note contains the query in the text or in the tags."""
        query_lower = query.lower()
        return query_lower in self.content.lower() or any(
            query_lower in tag.lower() for tag in self.tags
        )

    def is_today(self) -> bool:
        """Returns True if the note has been created today."""
        local_now = datetime.now().date()
        local_created = self.created_at.astimezone().date()
        return local_created == local_now
