"""Version command."""

from __future__ import annotations

import typer

from orexeva.core import run_version

app = typer.Typer()


@app.callback(invoke_without_command=True)
def version() -> None:
    """Show the current Orexeva version."""
    typer.echo(run_version().to_text())
