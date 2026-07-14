import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def recommend():
    """
    Recommend the best development environment for your system.
    """
    typer.echo("Recommend command is under development.")