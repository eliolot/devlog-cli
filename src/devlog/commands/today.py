from rich.console import Console
from rich.table import Table

from devlog.storage import Storage

console = Console()


def today_command() -> None:
    """Show all entries created today."""
    storage = Storage()
    entries = storage.get_today()

    if not entries:
        console.print(
            "[yellow]No entries today yet.[/yellow] Use [bold]devlog add[/bold] to add your first note!"
        )
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Time", style="dim", width=8)
    table.add_column("Note")
    table.add_column("Tags", style="cyan")

    for entry in entries:
        time_str = entry.created_at.astimezone().strftime("%H:%M")
        tags_str = " ".join(f"#{t}" for t in entry.tags) if entry.tags else ""
        table.add_row(time_str, entry.content, tags_str)

    console.print(f"\n[bold]Today's entries[/bold] ({len(entries)})\n")
    console.print(table)
