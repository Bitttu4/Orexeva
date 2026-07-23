"""Clean command."""

from __future__ import annotations

import typer

from orexeva.core import run_clean

app = typer.Typer()


@app.callback(invoke_without_command=True)
def clean() -> None:
    """Clean temporary files and caches."""
    typer.echo(run_clean().to_text())
