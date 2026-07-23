"""Doctor command."""

from __future__ import annotations

import typer

from orexeva.core import run_doctor

app = typer.Typer()


@app.callback(invoke_without_command=True)
def doctor() -> None:
    """Analyze the current development environment."""
    typer.echo(run_doctor().to_text())
