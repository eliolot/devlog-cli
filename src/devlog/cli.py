import typer
from rich.console import Console

from devlog.commands.add import add_command
from devlog.commands.export import export_command
from devlog.commands.search import search_command
from devlog.commands.stats import stats_command
from devlog.commands.today import today_command

app = typer.Typer(
    name="devlog",
    help="A fast, minimal CLI tool to keep a developer journal.",
    add_completion=False,
)

console = Console()

app.command("add")(add_command)
app.command("today")(today_command)
app.command("search")(search_command)
app.command("export")(export_command)
app.command("stats")(stats_command)

if __name__ == "__main__":
    app()
