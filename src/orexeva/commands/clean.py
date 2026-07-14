import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def clean():
    """
    Clean temporary files and caches.
    """
    typer.echo("Clean command is under development.")