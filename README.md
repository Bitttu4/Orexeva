# Orexeva

> Developer Infrastructure Platform for Local AI Development

Orexeva is a cross-platform developer platform designed to simplify local AI development. It provides a unified interface for installing, managing, configuring, and running local AI models across multiple providers while maintaining a clean, production-quality architecture.

> **Current Status:** 🚧 Active Development

---

# Features

- Cross-platform support (Windows, Linux, macOS)
- Automatic platform detection
- Local AI model management
- Multiple provider support
- Intelligent recommendations
- Configuration management
- Registry management
- Developer-friendly CLI
- Zero cloud dependency
- Production-quality architecture

---

# Project Goals

Orexeva aims to provide a single command-line interface for everything related to local AI.

Instead of manually configuring different tools, Orexeva will manage:

- AI providers
- Local models
- Runtime configuration
- Downloads
- Updates
- Workspaces
- Development environment

---

# Current Project Structure

```text
src/
└── orexeva/
    ├── commands/
    ├── config/
    ├── core/
    ├── database/
    ├── installer/
    ├── intelligence/
    ├── platform/
    ├── recommender/
    ├── registry/
    ├── utils/
    ├── cli.py
    ├── constants.py
    └── __main__.py
```

---

# Requirements

- Python 3.11+
- Windows, Linux or macOS

---

# Installation

Clone the repository.

```bash
git clone <repository-url>
```

Move into the project.

```bash
cd Orexeva
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -e .
```

---

# Running

Show CLI help.

```bash
python -m orexeva --help
```

Show version.

```bash
python -m orexeva version
```

---

# Development

Current completed modules:

- ✅ Environment
- ✅ Platform
- ✅ Config
- ✅ Registry

Modules under development:

- Installer
- Database
- Intelligence
- Recommender
- CLI
- Runtime

---

# Testing

Run platform tests.

```bash
python -m tests.test_detection
```

Run configuration tests.

```bash
python -m tests.test_config
```

Run registry tests.

```bash
python -m tests.test_registry
```

---

# License

Licensed under the MIT License.

See the LICENSE file for details.

---

# Authors

- Aarya Patel
- Ruchi Tanwar