"""Orexeva core orchestration layer."""

from __future__ import annotations

from .context import ExecutionContext
from .engine import (
    run_clean,
    run_doctor,
    run_models,
    run_recommend,
    run_repair,
    run_setup,
    run_version,
    run_update,
    run_workspace,
)
from .exceptions import (
    CoreError,
    CoreExecutionError,
    CoreUnavailableError,
)
from .result import (
    CleanResult,
    DoctorResult,
    ModelResult,
    RecommendationResult,
    RepairResult,
    ReportResult,
    SetupResult,
    VersionResult,
    UpdateResult,
    WorkspaceResult,
)

__all__ = [
    "ExecutionContext",
    "CoreError",
    "CoreExecutionError",
    "CoreUnavailableError",
    "ReportResult",
    "DoctorResult",
    "SetupResult",
    "VersionResult",
    "RecommendationResult",
    "ModelResult",
    "WorkspaceResult",
    "UpdateResult",
    "RepairResult",
    "CleanResult",
    "run_doctor",
    "run_setup",
    "run_version",
    "run_recommend",
    "run_models",
    "run_workspace",
    "run_update",
    "run_repair",
    "run_clean",
]
