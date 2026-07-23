"""Setup command."""

from __future__ import annotations

import typer

from orexeva.core import run_setup

app = typer.Typer()


@app.callback(invoke_without_command=True)
def setup() -> None:
    """Set up a complete local AI development environment."""
    typer.echo(run_setup().to_text())
