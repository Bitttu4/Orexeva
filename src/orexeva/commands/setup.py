import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def setup():
    """
    Set up a complete local AI development environment.
    """
    typer.echo("Setup command is under development.")