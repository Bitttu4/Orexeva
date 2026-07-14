import typer

from orexeva.commands.version import app as version_app

app = typer.Typer(
    name="orexeva",
    help="Developer Infrastructure Platform for Local AI Development",
    no_args_is_help=True,
)

app.add_typer(
    version_app,
    name="version",
    help="Show version information.",
)