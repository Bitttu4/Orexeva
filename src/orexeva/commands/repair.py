"""Repair command."""

from __future__ import annotations

import typer

from orexeva.core import run_repair

app = typer.Typer()


@app.callback(invoke_without_command=True)
def repair() -> None:
    """Repair broken development environments."""
    typer.echo(run_repair().to_text())
