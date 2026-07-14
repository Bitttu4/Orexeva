import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def doctor():
    """
    Analyze the current development environment.
    """
    typer.echo("Doctor command is under development.")