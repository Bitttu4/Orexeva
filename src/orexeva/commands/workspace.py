import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def update():
    """
    Update installed development tools.
    """
    typer.echo("Update command is under development.")