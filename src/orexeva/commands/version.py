import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def version():
    """
    Show the current Orexeva version.
    """
    typer.echo("Orexeva v0.1.0")