"""
Orexeva Command Registry

Responsible for registering all CLI commands.
"""

import typer

from orexeva.commands.clean import app as clean_app
from orexeva.commands.doctor import app as doctor_app
from orexeva.commands.models import app as models_app
from orexeva.commands.recommend import app as recommend_app
from orexeva.commands.repair import app as repair_app
from orexeva.commands.setup import app as setup_app
from orexeva.commands.update import app as update_app
from orexeva.commands.version import app as version_app
from orexeva.commands.workspace import app as workspace_app
from orexeva.constants import DESCRIPTION

app = typer.Typer(
    name="orexeva",
    help=DESCRIPTION,
    no_args_is_help=True,
)

app.add_typer(
    setup_app,
    name="setup",
    help="Set up a complete local AI development environment.",
)

app.add_typer(
    doctor_app,
    name="doctor",
    help="Analyze the current development environment.",
)

app.add_typer(
    recommend_app,
    name="recommend",
    help="Recommend the best tools and AI models for your system.",
)

app.add_typer(
    workspace_app,
    name="workspace",
    help="Create and manage development workspaces.",
)

app.add_typer(
    models_app,
    name="models",
    help="Manage local AI models.",
)

app.add_typer(
    update_app,
    name="update",
    help="Update installed development tools.",
)

app.add_typer(
    repair_app,
    name="repair",
    help="Repair broken development environments.",
)

app.add_typer(
    clean_app,
    name="clean",
    help="Clean temporary files and caches.",
)

app.add_typer(
    version_app,
    name="version",
    help="Show Orexeva version.",
)