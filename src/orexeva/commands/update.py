"""Update command."""

from __future__ import annotations

import typer

from orexeva.core import run_update

app = typer.Typer()


@app.callback(invoke_without_command=True)
def update() -> None:
    """Update installed development tools."""
    typer.echo(run_update().to_text())
