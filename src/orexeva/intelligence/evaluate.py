"""
Capability evaluation stage for Orexeva intelligence.
"""

from __future__ import annotations

from orexeva.providers.base import ProviderStatus

from .types import (
    AnalysisResult,
    CapabilityLevel,
    CapabilityScore,
    EvaluationResult,
    RuntimeAssessment,
)


def _score_ram(ram_total_gb: float | None) -> CapabilityScore:
    if ram_total_gb is None:
        return CapabilityScore("ram", CapabilityLevel.UNKNOWN, 0, "RAM data not available.")
    if ram_total_gb < 8:
        return CapabilityScore("ram", CapabilityLevel.LOW, 25, "Suitable for lightweight runtimes only.")
    if ram_total_gb < 16:
        return CapabilityScore("ram", CapabilityLevel.MODERATE, 50, "Can run small and medium local runtimes.")
    if ram_total_gb < 32:
        return CapabilityScore("ram", CapabilityLevel.GOOD, 75, "Well suited for most local AI runtimes.")
    return CapabilityScore("ram", CapabilityLevel.EXCELLENT, 95, "Strong capacity for large local models.")


def _score_storage(storage_free_gb: float | None) -> CapabilityScore:
    if storage_free_gb is None:
        return CapabilityScore("storage", CapabilityLevel.UNKNOWN, 0, "Storage data not available.")
    if storage_free_gb < 50:
        return CapabilityScore("storage", CapabilityLevel.LOW, 20, "Free space is tight for model downloads.")
    if storage_free_gb < 150:
        return CapabilityScore("storage", CapabilityLevel.MODERATE, 55, "Enough space for modest model sets.")
    if storage_free_gb < 300:
        return CapabilityScore("storage", CapabilityLevel.GOOD, 80, "Healthy space for multiple runtimes and models.")
    return CapabilityScore("storage", CapabilityLevel.EXCELLENT, 95, "Plenty of space for larger model libraries.")


def _score_gpu(gpu: str) -> CapabilityScore:
    normalized = gpu.lower()
    if not gpu or gpu == "Unknown GPU":
        return CapabilityScore("gpu", CapabilityLevel.UNKNOWN, 0, "No GPU details detected.")
    if any(token in normalized for token in ("nvidia", "rtx", "gtx")):
        return CapabilityScore("gpu", CapabilityLevel.STRONG, 90, "CUDA-capable NVIDIA GPU detected.")
    if "amd" in normalized or "radeon" in normalized:
        return CapabilityScore("gpu", CapabilityLevel.GOOD, 75, "AMD GPU detected; GPU acceleration may be available.")
    if "apple" in normalized or "m1" in normalized or "m2" in normalized or "m3" in normalized:
        return CapabilityScore("gpu", CapabilityLevel.GOOD, 80, "Apple silicon detected with Metal support.")
    return CapabilityScore("gpu", CapabilityLevel.MODERATE, 50, "GPU detected, but acceleration support is uncertain.")


def _score_cpu(cpu_cores: int | None, cpu_threads: int | None) -> CapabilityScore:
    if cpu_cores is None and cpu_threads is None:
        return CapabilityScore("cpu", CapabilityLevel.UNKNOWN, 0, "CPU data not available.")
    threads = cpu_threads or cpu_cores or 1
    if threads < 4:
        return CapabilityScore("cpu", CapabilityLevel.LOW, 20, "Very small CPU footprint.")
    if threads < 8:
        return CapabilityScore("cpu", CapabilityLevel.MODERATE, 50, "Modest CPU capacity.")
    if threads < 16:
        return CapabilityScore("cpu", CapabilityLevel.GOOD, 75, "Good general-purpose CPU capacity.")
    return CapabilityScore("cpu", CapabilityLevel.EXCELLENT, 90, "Strong CPU capacity for local workloads.")

def evaluate(analysis: AnalysisResult) -> EvaluationResult:
    """Evaluate the analyzed system and assign capability scores."""
    cpu = _score_cpu(analysis.system.cpu_cores, analysis.system.cpu_threads)
    gpu = _score_gpu(analysis.system.gpu)
    ram = _score_ram(analysis.system.ram_total_gb)
    storage = _score_storage(analysis.system.storage_free_gb)

    capability_scores = (cpu, gpu, ram, storage)
    overall_score = round(sum(score.score for score in capability_scores) / len(capability_scores))

    runtime_assessments = []
    for runtime in analysis.runtimes:
        supported = runtime.installed and runtime.status != ProviderStatus.ERROR
        reasons = []
        if runtime.installed:
            reasons.append("Provider detected.")
        else:
            reasons.append("Provider not installed.")
        if runtime.status == ProviderStatus.RUNNING:
            reasons.append("Runtime is responding.")
        runtime_assessments.append(
            RuntimeAssessment(
                name=runtime.name,
                display_name=runtime.display_name,
                supported=supported,
                score=80 if supported else 0,
                status=runtime.status.value,
                reasons=tuple(reasons),
            )
        )

    return EvaluationResult(
        capability_scores=capability_scores,
        runtime_assessments=tuple(runtime_assessments),
        overall_score=overall_score,
        notes=("Evaluation is deterministic and derived from detected machine data.",),
    )
