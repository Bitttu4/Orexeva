"""Core orchestration engine."""

from __future__ import annotations

from .context import ExecutionContext
from .result import (
    CleanResult,
    DoctorResult,
    ModelResult,
    RecommendationResult,
    RepairResult,
    SetupResult,
    VersionResult,
    UpdateResult,
    WorkspaceResult,
)
from .services import (
    CleanService,
    DoctorService,
    ModelsService,
    RecommendService,
    RepairService,
    SetupService,
    VersionService,
    UpdateService,
    WorkspaceService,
)


def _context(context: ExecutionContext | None) -> ExecutionContext:
    """Return the provided context or build a new one."""
    return context if context is not None else ExecutionContext.create()


def run_doctor(context: ExecutionContext | None = None) -> DoctorResult:
    """Run the doctor workflow."""
    return DoctorService().run(_context(context))


def run_setup(context: ExecutionContext | None = None) -> SetupResult:
    """Run the setup workflow."""
    return SetupService().run(_context(context))


def run_version(context: ExecutionContext | None = None) -> VersionResult:
    """Run the version workflow."""
    return VersionService().run(_context(context))


def run_recommend(context: ExecutionContext | None = None) -> RecommendationResult:
    """Run the recommendation workflow."""
    return RecommendService().run(_context(context))


def run_models(context: ExecutionContext | None = None) -> ModelResult:
    """Run the models workflow."""
    return ModelsService().run(_context(context))


def run_workspace(context: ExecutionContext | None = None) -> WorkspaceResult:
    """Run the workspace workflow."""
    return WorkspaceService().run(_context(context))


def run_update(context: ExecutionContext | None = None) -> UpdateResult:
    """Run the update workflow."""
    return UpdateService().run(_context(context))


def run_repair(context: ExecutionContext | None = None) -> RepairResult:
    """Run the repair workflow."""
    return RepairService().run(_context(context))


def run_clean(context: ExecutionContext | None = None) -> CleanResult:
    """Run the clean workflow."""
    return CleanService().run(_context(context))
