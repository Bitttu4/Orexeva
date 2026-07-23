"""Recommendation command."""

from __future__ import annotations

import typer

from orexeva.core import run_recommend

app = typer.Typer()


@app.callback(invoke_without_command=True)
def recommend() -> None:
    """Recommend the best development environment for your system."""
    typer.echo(run_recommend().to_text())
