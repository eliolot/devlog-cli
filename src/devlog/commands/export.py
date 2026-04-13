import json
from enum import Enum
from typing import Annotated

import typer
from rich.console import Console

from devlog.storage import Storage

console = Console()


class ExportFormat(str, Enum):
    markdown = "md"
    json = "json"


def export_command(
    format: Annotated[
        ExportFormat,
        typer.Option("--format", "-f", help="Export format: md or json"),
    ] = ExportFormat.markdown,
) -> None:
    """Export all entries to stdout in Markdown or JSON format."""
    storage = Storage()
    entries = storage.get_all()

    if not entries:
        console.print("[yellow]No entries to export.[/yellow]")
        raise typer.Exit(1)

    if format == ExportFormat.json:
        data = [entry.model_dump(mode="json") for entry in entries]
        typer.echo(json.dumps(data, indent=2, default=str))

    elif format == ExportFormat.markdown:
        lines: list[str] = ["# devlog export\n"]
        current_date = ""
        for entry in reversed(entries):
            date_str = entry.created_at.astimezone().strftime("%Y-%m-%d")
            if date_str != current_date:
                current_date = date_str
                lines.append(f"\n## {date_str}\n")
            time_str = entry.created_at.astimezone().strftime("%H:%M")
            tags_str = f" `{'` `'.join(entry.tags)}`" if entry.tags else ""
            lines.append(f"- **{time_str}**{tags_str} — {entry.content}")
        typer.echo("\n".join(lines))
