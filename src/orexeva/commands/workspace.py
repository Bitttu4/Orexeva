"""Workspace command."""

from __future__ import annotations

import typer

from orexeva.core import run_workspace

app = typer.Typer()


@app.callback(invoke_without_command=True)
def workspace() -> None:
    """Create and manage development workspaces."""
    typer.echo(run_workspace().to_text())

