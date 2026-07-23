"""Models command."""

from __future__ import annotations

import typer

from orexeva.core import run_models

app = typer.Typer()


@app.callback(invoke_without_command=True)
def models() -> None:
    """Manage local AI models."""
    typer.echo(run_models().to_text())
