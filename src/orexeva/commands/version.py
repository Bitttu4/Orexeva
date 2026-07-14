import typer

from orexeva.constants import APP_NAME, VERSION

app = typer.Typer()


@app.callback(invoke_without_command=True)
def version():
    """
    Show the current Orexeva version.
    """
    typer.echo(f"{APP_NAME} v{VERSION}")