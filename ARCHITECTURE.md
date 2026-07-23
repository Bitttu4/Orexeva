# Orexeva Architecture Report

## 1. Purpose

Orexeva is a production-quality Python CLI for managing local AI development environments.
Its role is to turn a fresh machine into a usable developer workstation by coordinating
configuration, platform detection, provider management, registry data, and CLI workflows.

This report describes the architecture as it exists in the repository today and keeps the
scope aligned with the project vision described in `what is this.md`.

## 2. Product Summary

Orexeva is designed to be:

- A single command interface for environment setup and maintenance
- Cross-platform across Windows, macOS, and Linux
- Deterministic in its core decisions
- Modular and easy to extend
- Local-first and privacy-preserving

It is not an IDE, not a package manager replacement, and not an AI assistant that makes
system-critical decisions. The codebase reflects that separation clearly.

## 3. Current Repository Shape

The repository is organized as a Python package under `src/orexeva` with command modules,
supporting subsystems, and a small test suite.

### Top-level layout

- `src/orexeva/`
- `tests/`
- `pyproject.toml`
- `README.md`
- `ARCHITECTURE.md`

### Key package areas

- `commands/` for CLI command implementations
- `config/` for configuration loading and persistence
- `platform/` for OS-specific system detection
- `providers/` for provider abstractions and runtime adapters
- `registry/` for registry load/save/reset logic
- `runtime/`, `core/`, `database/`, `installer/`, `intelligence/`, `recommender/`, `models/`, `utils/` as package boundaries already reserved in the tree

## 4. Layered Architecture

Orexeva follows a simple layered structure.

### CLI layer

The CLI layer is the public entry point for users.

- `src/orexeva/cli.py` exposes the Typer application
- `src/orexeva/cli_registry.py` registers command groups
- `src/orexeva/__main__.py` allows `python -m orexeva`

This layer should stay thin and delegate real work to command modules.

### Command layer

Command modules translate user intent into calls to the underlying services.

Current commands include:

- `setup`
- `doctor`
- `recommend`
- `workspace`
- `models`
- `update`
- `repair`
- `clean`
- `version`

The command layer is where CLI-specific parsing and output formatting belong.

### Supporting subsystems

- `config/` manages persisted settings
- `platform/` detects OS and machine details
- `providers/` abstracts external runtimes and tools
- `registry/` stores file-backed catalogue data

These modules provide the operational foundation for the CLI commands.

## 5. Configuration Architecture

The configuration subsystem is intentionally small and explicit.

### Modules

- `config/defaults.py` defines the default configuration object
- `config/storage.py` reads, writes, and resets config data
- `config/manager.py` wraps the storage functions in a `Config` class
- `config/paths.py` centralizes path resolution

### Behavior

The current implementation:

- loads config on instantiation
- returns values via `get()`
- updates values via `set()`
- persists with `save()`
- restores defaults with `reset()`
- returns a shallow copy with `all()`

The design is straightforward and easy to test, which matches the project style.

## 6. Registry Architecture

Orexeva treats registry data as file-backed state with a small management API.

### Modules

- `registry/schema.py` defines the default registry structure
- `registry/storage.py` handles on-disk JSON I/O
- `registry/loader.py` loads, merges, saves, and resets registry data
- `registry/manager.py` exposes the `Registry` wrapper class

### Current registry shape

The default registry stores:

- registry version
- models
- providers
- downloads
- runtime state
- metadata

This is the foundation for future model catalogues, provider listings, and runtime state
tracking.

## 7. Platform Architecture

The platform layer is already present and provides OS-specific detection.

### Modules

- `platform/detector.py` dispatches to the active platform
- `platform/windows.py` collects Windows details
- `platform/linux.py` collects Linux details
- `platform/macos.py` collects macOS details

### Returned information

The detector returns a dictionary containing fields such as:

- operating system
- OS version
- architecture
- CPU information
- core and thread counts
- RAM total
- GPU name
- storage totals
- Python version

This is enough for doctor-style reporting and future recommendation logic.

## 8. Provider Architecture

The provider layer is the current bridge between Orexeva and external runtime tools.

### Base types

- `providers/base.py` defines provider categories, capabilities, metadata, and abstract base classes
- `providers/exceptions.py` defines provider-specific errors
- `providers/catalog.py` stores provider registration state
- `providers/manager.py` is reserved for lifecycle orchestration

### Runtime providers

The repository already contains runtime adapter modules under `providers/runtimes/`:

- `ollama.py`
- `lmstudio.py`
- `llamacpp.py`
- `jan.py`
- `koboldcpp.py`
- `mistralrs.py`
- `text_generation_webui.py`
- `vllm.py`

The Ollama adapter is the most complete runtime implementation at present and covers:

- executable detection
- version retrieval
- runtime health checks
- model listing
- model pulling and removal
- runtime lifecycle helpers

### Architecture rule

Runtime providers should remain adapters. They should not become places for product logic,
recommendation logic, or CLI presentation.

## 9. CLI Flow

The current command flow is simple and intentional.

1. User runs `orexeva`
2. Typer loads `cli.py`
3. `cli_registry.py` registers command groups
4. A command module in `commands/` handles the request
5. The command module calls into the relevant subsystem
6. Results are returned to the CLI for display

This keeps user-facing parsing separate from reusable business logic.

## 10. Testing Architecture

The current test suite is intentionally small and module-focused.

### Existing tests

- `tests/test_config.py`
- `tests/test_registry.py`
- `tests/test_detection.py`
- `tests/test_providers.py`

### Test style

The tests are currently direct and lightweight, which fits the repository stage.
They validate public behavior by importing the package surfaces and exercising the current
module APIs.

### Current gap

The test files are still very thin, so the next practical step after architecture
stabilization is to convert them into real unit tests with assertions and mocks.

## 11. Current Architectural Observations

### What is working well

- The package boundaries are already clear
- The CLI entry point is isolated
- Configuration and registry each have their own storage/manager split
- Platform detection is separated by OS
- Provider abstractions already exist, even before every adapter is finished

### What is still immature

- Several package directories exist as placeholders for future work
- Most commands are still thin stubs
- Some provider modules are not yet fully implemented
- The test suite needs proper assertion-based coverage

These are normal for the current stage of the project and do not require redesign.

## 12. Recommended Module Order

Based on the repository state, the next modules to complete should be:

1. Provider manager
2. Runtime provider adapters beyond Ollama
3. Command layer implementations
4. Core workflow modules
5. Recommendation engine and registry expansion

This keeps the project moving from the edges inward without rewriting frozen modules.

## 13. Constraints and Principles

The architecture follows the project rules already stated in the repository:

- Do not rewrite completed modules
- Do not change public interfaces unless explicitly required
- Keep modules simple and readable
- Implement one module at a time
- Prefer explicit behavior over clever abstractions
- Keep the CLI thin and the logic reusable

## 14. Summary

Orexeva is currently a clean Python CLI skeleton with strong package boundaries and a
clear direction:

- CLI entry points are in place
- Configuration and registry modules exist
- Platform detection works per operating system
- Provider architecture is established
- Ollama is the most developed runtime adapter

The codebase is ready for incremental completion without architectural overhaul.

