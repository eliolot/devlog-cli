from collections import Counter
from datetime import UTC, datetime, timedelta

from rich.console import Console
from rich.table import Table

from devlog.storage import Storage

console = Console()


def stats_command() -> None:
    """Show usage statistics."""
    storage = Storage()
    all_entries = storage.get_all()

    if not all_entries:
        console.print(
            "[yellow]No entries yet.[/yellow] Use [bold]devlog add[/bold] to get started."
        )
        return

    # Compute statistics
    total = len(all_entries)
    today_count = len(storage.get_today())

    week_ago = datetime.now(UTC) - timedelta(days=7)
    this_week = [e for e in all_entries if e.created_at >= week_ago]

    all_tags = [tag for entry in all_entries for tag in entry.tags]
    tag_counts = Counter(all_tags).most_common(5)

    # Output
    console.print("\n[bold]devlog stats[/bold]\n")

    summary = Table(show_header=False, box=None, padding=(0, 2))
    summary.add_column("Metric", style="dim")
    summary.add_column("Value", style="bold")
    summary.add_row("Total entries", str(total))
    summary.add_row("Today", str(today_count))
    summary.add_row("This week", str(len(this_week)))
    console.print(summary)

    if tag_counts:
        console.print("\n[bold]Top tags[/bold]\n")
        tag_table = Table(show_header=False, box=None, padding=(0, 2))
        tag_table.add_column("Tag", style="cyan")
        tag_table.add_column("Count", style="bold")
        for tag, count in tag_counts:
            tag_table.add_row(f"#{tag}", str(count))
        console.print(tag_table)
