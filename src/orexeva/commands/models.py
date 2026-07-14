import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def models():
    """
    Manage local AI models.
    """
    typer.echo("Models command is under development.")