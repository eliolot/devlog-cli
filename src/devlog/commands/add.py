from typing import Annotated

import typer
from rich.console import Console

from devlog.models import LogEntry
from devlog.storage import Storage

console = Console()


def add_command(
    content: Annotated[str, typer.Argument(help="The note content")],
    tag: Annotated[
        list[str] | None, typer.Option("--tag", "-t", help="Tag for the note")
    ] = None,
) -> None:
    """Add a new entry to your dev journal."""
    tags = tag or []
    storage = Storage()
    entry = LogEntry(content=content, tags=tags)
    storage.add(entry)

    console.print(
        f"[green]✓[/green] Note saved at [dim]{entry.created_at.strftime('%H:%M')}[/dim]"
    )
    if tags:
        console.print(f"  Tags: {' '.join(f'[cyan]#{t}[/cyan]' for t in tags)}")
