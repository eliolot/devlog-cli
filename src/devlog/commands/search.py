from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from devlog.storage import Storage

console = Console()


def search_command(
    query: Annotated[str, typer.Argument(help="Search keyword")],
) -> None:
    """Search entries by content or tag."""
    storage = Storage()
    results = storage.search(query)

    if not results:
        console.print(
            f"[yellow]No entries found[/yellow] matching [bold]{query!r}[/bold]"
        )
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=12)
    table.add_column("Note")
    table.add_column("Tags", style="cyan")

    for entry in results:
        date_str = entry.created_at.astimezone().strftime("%Y-%m-%d %H:%M")
        tags_str = " ".join(f"#{t}" for t in entry.tags) if entry.tags else ""
        table.add_row(date_str, entry.content, tags_str)

    console.print(f"\n[bold]Results for[/bold] {query!r} ({len(results)} found\n")
    console.print(table)
