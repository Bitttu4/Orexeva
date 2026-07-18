# Orexeva  

*Everything your development environment needs.*

``` diagram
     ________________________________________________
    |   Orexeva – Developer Infrastructure Platform  |
    |________________________________________________|
           \  ^__^
            \ (oo)\_______
              (__)\       )\/\
                  ||----w |
                  ||     ||
```

**Document Type**: Software Architecture & Product Vision Blueprint  
**Audience**: Core Team, Contributors, Future Maintainers  
**Status**: Pre-Development Deep Dive (Final)  
**Language**: Hinglish (Hindi + English Technical Terms)

---

## Project Background

### Shuruaat – Ek Simple Idea

Shuru mein humne socha, *"Chalo Ollama install karte hain, local AI models use karenge."*  
Lekin jab humne baith ke discussion kiya, tab realize hua – ye sirf Ollama ka problem nahi hai.  
Har baar ek fresh machine le kar baitho, chahe wo naya laptop ho, cloud VM ho, ya kisi dost ka computer, toh wahi same boring setup repeat hota hai.

Socho:

- Git install karo
- Python set karo (right version, PATH variable)
- Node.js, npm
- VS Code, uske extensions
- Docker, WSL2 agar Windows pe ho
- Windows Terminal, PowerShell 7
- GPU drivers, CUDA, cuDNN
- Ollama, models pull karo
- Environment variables, config files
- SSH keys, GPG keys
- Tools like `ffmpeg`, `make`, `cmake`

Yeh sab karne mein **ghanto lag jaate hain**, aur fir bhi kuch na kuch chhoot jaata hai.  
Fir YouTube tutorials, blog posts, Stack Overflow – mental energy waste.

### Evolution – From Single Tool to Developer Infrastructure Platform

Tab humne socha – kyun na ek **single command** se poori developer environment ready ho jaaye?  
Lekin hum ruke nahi. Socha, developer ke liye ab AI local hona hi future hai.  
To isiliye humara focus sirf setup nahi, balki **Local AI Development Workstation** banana hai.

Ab Orexeva ka goal hai:

> Ek bilkul blank machine ko **fully configured AI-powered development environment** mein convert karna, minutes mein, bina kisi manual headache ke.

Simple installation script se bahut aage ki soch hai ye. Yeh ek **platform** hai. Orexeva koi AI assistant, chatbot ya AI wrapper nahi hai. Orexeva ek **Developer Infrastructure Platform** hai jo AI ko sirf optional helper ki tarah use karta hai. Platform bina AI ke bhi perfectly kaam karega.

---

## Project Vision

**Orexeva — Everything your development environment needs.**

Jab tum fresh OS install karte ho, toh first thing you install is a browser, right?  
Humara vision hai ki future mein pehla software jo log install karein, wo **Orexeva** ho.

Kyun? Kyunki uske baad:

- Browser? Setup ho jayega.
- IDE? Setup.
- Runtimes? Setup.
- AI models? Setup.
- Sab kuch personalized, optimized, ready to code.

### Kyun Important Hai Yeh Vision?

- **Time bachao**: Developer ka time expensive hai. Har setup mein 4–8 ghante waste karna galat hai.
- **Consistency**: Team ke sabhi log same environment use karein, "mere machine pe to chal raha tha" problem khatam.
- **AI Democratization**: Har developer local AI use kare, bina cloud cost ke, bina privacy compromise ke.
- **Onboarding**: Naye team member ko bas ek command run karni hai, turant productive.

Orexeva sirf installer nahi, **developer ka digital twin setup assistant** hai.

---

## Project Scope

Scope define karna isliye zaroori hai taake product focused rahe aur feature creep na ho. Hum clearly batayenge ki Orexeva kya karega aur kya nahi karega.

### In Scope

Orexeva ki zimmedariyan:

- **Development Environment Setup**: Required tools, runtimes, package managers, IDE extensions ki automatic installation aur configuration.
- **Local AI Setup**: Ollama jaisi local AI runtimes install karna, models pull karna, unhe verify karna.
- **AI Team Recommendation**: Hardware aur developer profile ke hisaab se role-based AI model team suggest karna (fully deterministic, AI involved nahi).
- **Environment Verification**: `orexeva doctor` se health check, missing dependencies pakadna, repair suggestions dena.
- **Project Bootstrap**: Templates se naye projects scaffold karna (workspace command).
- **Workspace Management**: Project-specific configurations, AI assistants ko manage karna.
- **Configuration Management**: Sab kuch version-controlled YAML/JSON configs se drive karna; profiles import/export karna.
- **Backup & Restore**: Poori development environment ki state capture karna, doosri machine pe restore.
- **Update Management**: Tools, configs, model database, plugins ko update rakhna.
- **Plugin System**: Community contributions ke liye extension points provide karna.
- **Reporting & Logging**: Setup reports, doctor output, logs generate karna.
- **Future Dashboard**: Terminal-based TUI dashboard for live monitoring and interaction.

### Out of Scope

Orexeva ye nahi banne wala:

- **Not an IDE**: Orexeva IDE nahi hai. Code editor ya IDE ka replacement nahi. VS Code, IntelliJ jaise tools ko configure karega, but unki functionality provide nahi karega.
- **Not an Operating System**: OS-level kernel, drivers, ya system services develop nahi karega. Existing OS ke upar layer hai.
- **Not a Cloud Platform**: Cloud infrastructure provision (AWS, Azure) iska core kaam nahi. Ha, future mein remote VM setup ke liye integration ho sakta hai, lekin khud cloud platform nahi banega.
- **Not a Package Manager Replacement**: Winget, Homebrew, Apt ko replace nahi karega, balki unke upar ek intelligent abstraction hai. Apna khud ka package format nahi banayega.
- **Not a Git Replacement**: Version control khud provide nahi karega. Git config set karega, but Git itself nahi.
- **Not a Docker Replacement**: Docker install aur basic config help karega, container orchestration nahi.

Is scope clarity se hum focused development kar sakte hain aur users ko bhi pata hoga ki Orexeva se kya expect karna hai.

---

## Cross Platform Vision

### Platform-Agnostic Promise

Humara command hamesha same rahega:

```bash
orexeva setup
```

Chahe tum Windows pe ho, macOS, ya future mein Linux.

### Internal OS Detection

Orexeva khud detect karega OS:

- **Windows**: Package manager `winget` (native), fallback `chocolatey`
- **macOS**: `homebrew`
- **Linux**: Distro-specific (`apt`, `dnf`, `pacman`, etc.)

User ko package manager ki tension nahi leni. Wo bas command run kare, Orexeva decide karega “ab is OS pe ye tool kaise install hoga”.

### Kyun Better Hai Separate Installers Se?

- **Single Codebase Logic**: Algorithm same, sirf low-level install commands badalte hain.
- **Maintainability**: Ek jagah fix karoge, sab platforms pe reflect hoga.
- **User Experience**: Har platform ke liye alag docs nahi padhne padenge. Same CLI, same wizard, same output.
- **Future-Proof**: Jab naya OS aaye (say, Windows 12, Asahi Linux), bas ek adapter likho.

Architecture mein hum **Adapter Pattern** use karenge. Platform-specific module honge jo ek common interface implement karenge. Isse testing bhi easy hogi.

---

## Technology Decisions

Har ek technology choice ke peeche solid reasoning hai. Chalo detail mein samjhte hain.

### Why Python?

Python is liye choose kiya kyunki:

- **Readability**: Syntax simple hai, contributors ko samajhne mein aasan.
- **Rich Ecosystem**: `typer`, `rich`, `textual`, `requests`, `psutil`, `platform`, `subprocess` sab milta hai.
- **Cross-Platform**: Python khud har OS pe chalta hai, bina recompile kiye.
- **AI/ML Integration**: Future mein agar Intelligence Layer ko local models se jodna ho toh seamlessly integrate hoga.
- **Packaging**: `pipx`, `poetry`, `pyinstaller` se single binary bana sakte hain install ke liye.

### Why PowerShell Was Rejected as Primary Language?

- Windows-centric: macOS/Linux pe PowerShell available hai par native feel nahi deta.
- Scripting ke liye theek hai, lekin complex workflows, configuration handling, rich UI ke liye suitable nahi.
- Community support for CLI frameworks PowerShell mein limited hai compared to Python.
- Kuch commands PowerShell mein verbose hote hain, Python mein clearer automation milti hai.

PowerShell sirf tab use karenge jab Windows-specific system calls ki zaroorat hogi (e.g., WSL integration), aur wo bhi Python se `subprocess` ke through call honge.

### Why CLI (Typer) Better Than a Setup Script?

Bash script ya `.bat` file limitations:

- No structured argument parsing, validation, auto-completion.
- Error handling bakwas hoti hai.
- Interactive prompts implement karna mushkil.
- State manage karna, resume karna possible nahi.

**Typer** kyun:

- Python mein likhte hain, automatically CLI generate hota hai.
- Commands, subcommands, options, arguments — sab clean.
- Auto help text, shell completion built-in.
- **Rich** integration for beautiful output: colors, progress bars, tables, panels.
- Future mein **Textual** add karke TUI dashboard bana sakte hain — same Python codebase.

### Rich: Beautiful Console Output

Logs, steps, warnings, errors — sab visually distinct. Spinner while installing, progress bar for downloads, tree view for installed tools. This makes CLI feel premium.

### Textual (Future GUI/TUI)

Textual ek Python framework hai terminal-based UI ke liye. Jab hume interactive dashboard chahiye (model usage, system resources, recommendations), tab CLI commands se hatke ek TUI application de sakte hain — bina electron ya web stack ke. Same Python, same logic.

### Architecture Advantage for Future GUI

Humara design **business logic ko CLI se alag** rakhega. Core functionality as Python library hogi, CLI sirf uska frontend. Future mein agar koi GUI (desktop app) banana ho, toh wahi library import karke use kar sakte hain. This is clean separation.

---

## Core Philosophy

Humari har decision in philosophies pe based hai. Ye humare guiding principles hain.

### 1. Automation First

Har wo cheez jo repeatable hai, automate honi chahiye.  
Setup, configuration, verification, model pulling, even recommendations — sab auto.  
User bas intent bataaye, Orexeva execute kare.  
Goal: *Zero manual steps*.

### 2. Developer First

End user ek developer hai. Uski needs ko priority.  
Ease of use, speed, reliability, customization — sab important.  
Hum assumption nahi lagayenge ki user expert hai ya beginner; wizard adapt karega.

### 3. Local AI First

Cloud AI expensive hai, data privacy risk hai, aur latency high.  
Hum local AI ko promote karenge.  
Har machine capable ho, chaahe CPU-only ho, chhoti RAM, ya powerful GPU.  
Hum recommendation denge aise models ki jo chal sakein, aur useful lagein.

### 4. Cross Platform

Ek baar likho, har jagah chalao.  
User ka OS matter nahi karna chahiye.  
Experience consistent rahe.  
Isliye architecture platform-agnostic abstraction layers rakhta hai.

### 5. Modular Design

Har feature ek independent module hoga.  
Setup module, Detection module, Recommendation engine, Model manager — sab alag.  
Fayda: Testability, Reusability, Easy to maintain, Plug and play future extensions.

### 6. Configuration Driven

Har tool, setting, model, profile ek YAML/JSON configuration mein define hogi.  
Isse naye tools add karna ho toh code change nahi, bas config file update karo.  
User ke apne configs bhi merge honge, custom dev profiles banane ke liye.

### 7. Plugin Friendly

Bahut saare developers ke specific tools hote hain (Neovim, Emacs, special compilers).  
Hum plugin system denge jisse koi bhi community member “Orexeva plugin” likh sake.  
Architecture mein hook points predefined honge.

### 8. Open Source Friendly

Project open source rahega.  
Contribution easy ho: clear docs, good issue labels, architecture diagrams.  
Humari documentation-first approach isiliye hai.

### 9. Maintainability

Code clean, well-tested, statically typed (Python type hints).  
Separation of concerns.  
Automated CI/CD for testing on multiple OS.  
Documentation ke saath code changes sync mein rahenge.

### 10. Scalability

Abhi hum 50 tools support karte hain, kal 500 ho sakte hain.  
Rule engine, configuration design, aur plugin architecture scale karne ke liye bana hai.  
Performance bhi dhyan rakhenge: parallel downloads, caching.

### 11. Documentation First

Code likhne se pehle documentation likho. Architecture decision records (ADR), module specs, user guides — sab ready hona chahiye. Isse contributors ko clarity milti hai, aur design flaws early catch hote hain.

### 12. Architecture First

Design socho, fir implement karo. Layered architecture pehle define karo, boundaries clear karo. Isse future changes limited impact rakhte hain.

### 13. Offline First

Developer hamesha internet se connected nahi rahega. Orexeva maximum functionality offline dega — local models, offline config templates, cached installers. Online hone par sync karega, lekin core offline chale.

### 14. Configuration First

Har behavior configurable hona chahiye. Hard-coding minimize karo. Users apni needs ke hisaab se override kar sakein bina code touch kiye.

### 15. Developer Experience First

CLI prompts natural hon, error messages helpful hon, progress feedback clear ho. Har interaction delightful feel ho. "Wow, it just works" — yahi target hai.

### 16. Extensibility

Plugin system, hook points, custom providers — sab kuch extendable. Community naye use-cases add kare, ecosystem grow kare.

### 17. Reliability

Deterministic rules, thorough verification, idempotent operations. Orexeva kabhi unpredictable na ho. Jo guarantee kare, wo poora kare.

### 18. Security

Sensitive data (tokens, keys) encrypted store ho. Permissions least privilege follow karein. Audit logging ho. Security-first mindset.

### 19. Reproducibility

Kisi bhi machine pe same `orexeva setup` same result de. Configuration as code se environments version-control ho, team-wide consistency mile.

### 20. Deterministic Correctness, Intelligent Communication

**System correctness must always come from deterministic software engineering. Intelligence should only improve user experience.** Orexeva ke core decisions — compatibility, recommendations, installation — kabhi AI par depend nahi karenge. Intelligence layer sirf explanation, natural language interaction, aur formatting ke liye hai. Isse platform reliable, debuggable, aur predictable banta hai.

---

## Architecture: Layered Design

Orexeva ek **layered architecture** follow karega. Har layer ki apni responsibility, apna boundary. Ye design scalable, testable aur future-proof hai.

``` flow diagram
┌──────────────────────────────────────┐
│               CLI Layer              │   (orexeva setup, doctor, ...)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│       Configuration Engine           │   (YAML/JSON profiles, rules, settings)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│           Core Engine                │   (Orchestration, workflow state)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│         Platform Layer               │   (OS detection, adapter dispatch)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│         Installer Engine             │   (Package managers, direct downloads)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│       Verification Engine            │   (Doctor, smoke tests)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│     Recommendation Engine            │   (Rule engine + scoring, fully deterministic)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│     Intelligence Layer (Optional)    │   (Explanation, formatting, NL input only)
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│      Reports & Dashboard             │   (Outputs, logging, TUI)
└──────────────────────────────────────┘
```

### Layer Responsibilities

- **CLI Layer**: User commands parse karta hai, Rich se beautiful output. Bus request forward karta hai neeche.
- **Configuration Engine**: Sabhi definitions — tools, profiles, models, rules, templates — YAML files mein. Dynamic loading, validation, merging. Bina code change kiye naya tool add karo.
- **Core Engine**: Business workflow ko orchestrate karta hai. Konse order mein kya hoga, state machine, error recovery. Ye brain hai.
- **Platform Layer**: OS aur package manager detect karta hai, correct adapter choose karta hai. Adapter pattern use karta hai taake Windows/macOS/Linux ka logic encapsulated rahe.
- **Installer Engine**: Actual installation commands execute karta hai — `winget install`, `brew install`, `apt-get`, etc. Parallel execution, retry, rollback support.
- **Verification Engine**: Har tool ki installation verify karta hai using defined check commands. Failed hone par repair suggest karta hai. `orexeva doctor` isi ka face hai.
- **Recommendation Engine**: Hardware + profile + rule engine + scoring engine se optimal AI model set suggest karta hai. Purely deterministic, no AI.
- **Intelligence Layer (Optional Enhancement)**: Sirf natural language understanding, explanation generation, aur output formatting ke liye. Kabhi core decisions influence nahi karta.
- **Reports & Dashboard**: Summaries, logs, benchmarks, TUI dashboard ke liye data prepare karta hai.

### Kyun Layered Architecture?

- **Separation of Concerns**: Har layer independent, testable.
- **Scalability**: Nayi platform add karni ho, sirf Platform Layer mein adapter likho.
- **Maintainability**: Ek layer change karne se doosri impact nahi.
- **Flexibility**: Future mein CLI ki jagah GUI ya Web API laga sakte ho, bas CLI Layer replace karo.

---

## Package Manager Strategy

Har OS ke liye package manager priority order defined hai, taake best available tool use ho aur fallback hamesha available rahe.

### Windows

1. **Winget** — Microsoft ka native package manager, modern, community-driven, fast. Orexeva ka primary choice kyunki ye pre-installed hota hai Windows 10/11 mein.
2. **Chocolatey** (fallback) — agar winget unavailable ho ya specific package winget mein na ho. Mature, large repository.
3. **Direct Installer** — last resort: official `.exe`/`.msi` download karke silent install.

### macOS

1. **Homebrew** — de facto standard. Orexeva ise primary maanta hai kyunki ye almost har developer tool provide karta hai.
2. **Direct Installer** — agar Homebrew mein package nahi, `.pkg` ya `.dmg` download.

### Linux

1. **Native Package Manager** — `apt` (Debian/Ubuntu), `dnf` (Fedora), `pacman` (Arch) automatically detect hoga.
2. **Manual Installation** — agar native repo mein latest version na ho, official script ya binary tarball.

### Fallback Kyun Zaroori Hai?

- **Reliability**: Primary package manager fail ho sakta hai (not installed, broken, corporate firewall). Fallback ensures installation kabhi ruke nahi.
- **Coverage**: Kuch tools sirf alternative sources mein available hote hain.
- **User Choice**: Agar user ne koi package manager specifically install nahi kiya, Orexeva automatic next best option use karega.

Har package manager ke liye adapter class hogi jo same interface implement karegi — `install(package)`, `update(package)`, `is_available()`. Core engine bus interface se baat karega, internal details se nahi.

---

## Project Workflow

Ek fresh machine se fully AI-ready workstation tak ka safar.

``` flow diagram
┌──────────────────────┐
│   Fresh Computer     │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ Install Orexeva      │  (pipx install orexeva, ya single binary)
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ orexeva setup        │
└─────────┬────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ System Detection (OS, Package Manager)       │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Hardware Detection (CPU, RAM, GPU, Storage)  │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Interactive Wizard: Developer Profile        │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Environment Setup                            │
│   - Install required tools via package mgr  │
│   - Configure shell, aliases, env vars      │
│   - IDE extensions, settings sync           │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Verification System                          │
│   - Check installations: versions, paths    │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Deterministic AI Recommendation              │
│   - Rule engine + scoring engine            │
│   - Generate Recommendation Report          │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Model Installation                           │
│   - Pull models from Ollama (or other)      │
│   - Verify they work                        │
└─────────┬───────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│ Development Ready!                           │
│   - Show summary, team, next steps           │
└─────────────────────────────────────────────┘
```

Har stage ki apni importance hai, jaise:

- **System Detection** — kaunsa OS, kaunsa package manager available hai, wahi se sahi tools select hote hain.
- **Hardware Detection** — RAM, VRAM, storage dekh kar hi decide hota hai kaunse AI models chalenge.
- **Developer Profile** — wizard user ki choice leta hai, jisse environment personal banta hai.
- **Environment Setup** — yahan real magic hota hai; saare tools parallel install hote hain, dotfiles configure hote hain.
- **Verification** — install ke baad check, taake kuch bhi adhura na rahe.
- **Deterministic Recommendation** — rule engine aur scoring engine sahi models chun kar recommendation report banata hai.
- **Model Installation** — report ke according models pull karke AI team ready ho jaati hai.

---

## Features

Orexeva ke commands hi features ka backbone hain. Har ek command ek specific responsibility handle karta hai.

### 1. `orexeva setup` – Complete Environment Bootstrap

Yeh wizard-based, step by step fresh machine se AI-ready workstation tak le jaata hai. Profile selection, tool install (Git, Python, Node, Docker, VS Code…), shell customization (Oh My Zsh, starship, aliases), AI team installation (deterministic recommendation se), aur verification report sab kuch ek hi command mein.

### 2. `orexeva doctor` – System Health Check

Verification engine ka frontend. Ye check karta hai:

- Installed tool versions
- PATH configuration
- Environment variables
- IDE extensions status
- Docker/WSL running
- Ollama service status
- Model integrity

Report generate hoti hai warnings ke saath. Future mein continuous monitoring bhi add ho sakta hai.

### 3. `orexeva repair` – Smart Fixer

Doctor ne problem report ki, ab repair fix karega. Capabilities:

- **Repair PATH**: Missing entries add karega.
- **Repair Python**: Virtual environment recreate karega, pip reinstall.
- **Repair Git**: Config validate karega, missing user details set karega.
- **Repair Ollama**: Service restart, corrupt models redownload.
- **Repair VS Code Integration**: Extension reinstall, settings sync restore.
- **Repair Broken Environment**: Package manager se reinstall attempt karega.

Workflow: `orexeva doctor` → issues list → `orexeva repair` specific target ya `orexeva repair --all`.

### 4. `orexeva recommend` – AI Model Advisor (Fully Deterministic)

Hardware + developer profile + rule engine + scoring engine ke hisaab se AI team suggest karta hai. Koi AI isme involved nahi. Output ek Recommendation Report hoti hai jisme har model ka reason, priority, alternatives, warnings diye hote hain.

### 5. `orexeva models` – Model Manager

Subcommands:

- `list` — installed models, versions, size
- `pull <name>` — download model with progress
- `remove <name>`
- `benchmark` — speed test
- `info <name>` — metadata from model database

### 6. `orexeva workspace` – Project Scaffolding

Templates se naye projects create karo. Jaise:

- `orexeva workspace new python-flask my-api`
- Cookiecutter templates, Orexeva built-in templates support.
- Optionally sets up AI assistant role for that project.

### 7. `orexeva update` – Keep Everything Updated

Update karega:

- Developer tools (winget/brew/apt ke through)
- Orexeva configuration templates (latest profiles, rules)
- AI model database (new models, scores)
- Orexeva itself (self-update)
- Future: plugin updates

Strategy: Check karega, diff dikhayega, confirm leke update karega. Safe rollback point banayega.

### 8. `orexeva backup` – Environment Snapshot

Backup hoga: installed tools list with versions, Orexeva profiles, custom configs, shell configs, dotfiles (optional), model list (not model files), IDE settings. Portable archive (JSON + files) kisi cloud/USB pe rakh sakte ho.

### 9. `orexeva restore` – Migrate to New Machine

Backup file do, Orexeva turant same environment recreate karega. New machine minutes mein ready.

### 10. `orexeva clean` – Housekeeping

Remove karega temporary installer files, old logs, unused model cache, broken partial downloads, Docker images, build artifacts. Disk space free, environment tidy.

### 11. `orexeva export` / `orexeva import` – Team Portability

Export profile, rules, model team composition as portable file. Team lead apna curated setup share kar sakta hai. New joiner `orexeva import team-profile.yaml` kare.

### 12. `orexeva dashboard` – Live TUI

Future Textual-based dashboard: system resources, model status, quick chat with AI team, logs. Abhi plan mein hai.

### 13. Failure Recovery

Orexeva ko reliable hona chahiye chahe installation ke dauran kuch bhi fail ho jaye. Isliye failure recovery built-in hogi.

- **Python installation fails**: Error log, retry option. Alternative method try. Complete rollback nahi.
- **Git installation fails**: Retry/fallback. Critical tools ke liye warning.
- **Internet disconnects**: Download resume support, retry with backoff.
- **System restarts/power failure**: State file se resume — dobara shuru nahi karna padega.
- **Partial installations**: Verification detect karega, repair se fix.

Rollback: user consent ke bina automatic destructive rollback nahi hoga.

---

## Configuration Engine

### Why Configuration-Driven?

Hard-coding tools, versions, rules directly in Python code is a maintenance disaster. Orexeva me sab kuch **declarative YAML/JSON** mein defined hoga.

### What Configuration Includes

- **Software Catalog**: Har tool ki definition (name, install commands per platform, verify command, dependencies).
- **Profiles**: Predefined developer profiles (`web-dev`, `data-science`) with selected tools, extensions, models.
- **Models Database**: Model metadata (RAM, VRAM, scores, tags, roles).
- **Rules**: Compatibility rules, recommendation scoring weights.
- **Extensions**: VS Code extensions, shell plugins mapping.
- **Templates**: Workspace templates with post-create hooks.
- **Package Managers**: Platform mapping, fallback chains.
- **Settings**: Global Orexeva behavior (logging level, parallelism, default providers).
- **Hooks**: Pre/post install scripts.

### Benefits over Code

- **Change without code**: Naya tool add karne ke liye sirf YAML file PR. CI test karega, merge, users ko next `orexeva update` mein mil jayega.
- **Community contributions**: Non-programmers bhi profiles, rules contribute kar sakte hain.
- **Versioning**: Configs ko Git mein track karo, rollback easy.
- **Override**: User apna custom config merge kare, bina original delete kiye.

Configuration engine load karte waqt multiple sources merge karega: built-in defaults → user config → environment overrides. Isse flexibility unlimited.

### Configuration Versioning

Jaise-jaise Orexeva evolve hoga, configuration files ka format badlega.

- **Configuration Version**: Har release ke saath config schema version badhega.
- **Migration**: Purane config ko naye format mein automatic migrate karega.
- **Backward Compatibility**: Naye Orexeva purane config padh sake, ya migrate kare.
- **Automatic Upgrade**: `orexeva update` user ke custom overrides preserve karega.
- **Configuration Backup**: Migration se pehle backup, revert safe.

Versioning isliye zaroori hai taake users ke setups kabhi break na ho.

---

## Model Database

Ye recommendation system ka dil hai. Har model jo Orexeva support karega, uska detailed metadata ek structured database (YAML/JSON) mein maintain hoga.

### Metadata per Model

|Field|Description|
|-------|-------------|
|`name`|e.g. `codellama:13b`|
|`role`|Lead, Architect, Quick Assistant, etc.|
|`category`|Code, Reasoning, Chat, Vision|
|`ram_required`|Minimum RAM in GB|
|`vram_required`|VRAM if GPU offload|
|`disk_size`|Download + extracted size|
|`context_length`|Max tokens|
|`coding_score`|0–100|
|`reasoning_score`|0–100|
|`writing_score`|0–100|
|`vision_support`|true/false|
|`license`|MIT, Llama2, etc.|
|`quantization`|q4_0, q5_K_M, etc.|
|`strengths`|["Python", "TypeScript", "SQL"]|
|`weaknesses`|["Rust", "COBOL"]|
|`best_use_cases`|["Code review", "Unit tests"]|
|`pull_command`|`ollama pull codellama:13b`|
|`tags`|["fast", "low-ram", "privacy"]|
|`architecture`|llama, mistral, gemma|

### Why Detailed?

- Compatibility check: RAM/VRAM mismatches reject.
- Scoring: Developer profile ke against har model ko score.
- Explainability: Report mein clear reason ki ye model kyun recommend hua.

Database community-maintained rahega, regular updates with new models.

---

## AI Team Concept

### Kyun Individual Model Recommend Nahin Karte?

Ek beginner ko “codellama:13b” vs “deepseek-coder:6.7b” mein farak nahi pata. Terms confusing hain. Use cases alag hote hain.

### Role-Based AI Team — Orexeva Builds It

Hum model ko ek **role** dete hain, jaise team members:

|Role|Purpose|Model Example (flexible)|
|------|---------|---------------------------|
|**Lead Software Engineer**|Project planning, system design, code review|codellama:13b / deepseek-coder:33b|
|**Technical Architect**|Architecture decisions, deep thinking|wizardlm-2:8x22b / mistral-large|
|**Reasoning Specialist**|Mathematical, logical puzzles|qwen2:72b / deepseek-r1|
|**Quick Assistant**|Small tasks, boilerplate, autocomplete|phi3:mini / stable-code:3b|

Yeh team **installation ke baad** user ko milti hai. Orexeva ka recommendation engine (deterministic) decide karta hai ki kaunse models kis role mein fit honge. AI team khud recommend nahi karti; recommendation engine team ko assemble karta hai.

### Psychology & Beginner Friendliness

- **Familiarity**: Team concept natural hai, lead, architect jaise roles familiar hain.
- **Decision Paralysis Kam**: “Mere team mein Architect chahiye” sochna easy hai.
- **Productivity**: Role ke hisaab se prompt, sahi model auto use.

### Role Interaction

User “Lead, review this code.” kahe, Orexeva Lead role ke assigned model ko call karega. Models swappable, roles consistent.

### Future Expansion

- **Security Engineer** — vulnerability scanning, secure coding.
- **DevOps Engineer** — CI/CD, Dockerfile optimization.
- **QA Engineer** — test generation, bug analysis.
- **Documentation Writer** — docstrings, README drafts.
- **Database Architect** — SQL optimization, schema design.
- **UI/UX Designer** — design feedback, accessibility checks.

Users custom AI teams bana sakte hain, roles define kar ke, models assign kar ke. Ye flexibility Orexeva ko AI-augmented development partner banati hai.

---

## Developer Profiles

Developer profile seedha affect karta hai kaunse tools install honge aur AI team kaise banegi.

- **Beginner**: Minimum tools, small fast AI models, focus on learning.
- **Student**: Python, Git, VS Code, Jupyter, basic models for assignments.
- **Professional**: Full toolchain (Docker, Kubernetes tools, multiple languages), powerful models for code review and architecture.
- **Researcher**: Data science stack, high-RAM models, embeddings.
- **AI Engineer**: Model development tools, Ollama advanced parameters.
- **Web Developer**: Node.js, npm, Git, front-end AI models.
- **Mobile Developer**: Android SDK, Xcode, Flutter, mobile-specific models.
- **Custom Workflow**: User khud define kare tools aur models, full control.

Profiles YAML files hoti hain jo community contribute kar sakti hai. Wizard ke through user modify kar sakta hai.

---

## Recommendation Engine (Fully Deterministic)

Recommendations kabhi AI par depend nahi karenge. Purely deterministic logic se aayengi.

### Recommendation Flow

``` flow
User
  ↓
System Scan
  ↓
Hardware Detection
  ↓
Developer Profile
  ↓
Rule Engine
  ↓
Compatibility Engine
  ↓
Scoring Engine
  ↓
Recommendation Engine
  ↓
Recommendation Report
  ↓
End
```

### Scoring Engine – Deterministic Scoring

Har compatible model ko numeric score based on weighted factors:

- **RAM Compatibility**: Available RAM mein kitna fit.
- **Storage Impact**: Disk size vs free space.
- **Programming Language Match**: Model ki strengths user ke languages se match.
- **Framework Match**: Matching models ko bonus.
- **Developer Profile Match**: Web dev ko fast, researcher ko deep reasoning.
- **Offline Suitability**: Smaller quantized models if offline preferred.
- **Speed**: Inference latency.
- **Role Suitability**: Role-specific heuristics.

Sab factors configurable weights. Top scoring models report mein dikhte hain. Deterministic => debug easy.

### Compatibility Engine

Hardware checks, architecture match, dependency rules filter karte hain. Fail hone wale models scoring mein participate nahi karte.

### Recommendation Report

Report mein har suggested model ke saath:

- **Model Name & Role**
- **Reason** (e.g. “Python coding score 92, RAM fit with 30% margin”)
- **RAM Usage**
- **Storage Usage**
- **Priority** (primary, secondary)
- **Alternative Options**
- **Warnings** (e.g. “large context window mein CPU pe slow”)

Report pure deterministic engine ka output hai. Intelligence Layer enable ho to natural language explanation milega, lekin content same.

---

## Rule Engine

### Deterministic Rules – Core of Trust

- **Memory Rule**: Model RAM + OS overhead <= available RAM - buffer.
- **Architecture Rule**: x86 model ARM machine pe reject.
- **GPU Rule**: GPU offload only if driver installed and VRAM sufficient.
- **Dependency Rule**: Model requires specific Ollama version.
- **License Rule**: Agar user ne “only permissive licenses” choose kiya to GPL models filter out.

Rules YAML mein defined, versioned, testable. Har PR ke saath rule validation tests run honge.

---

## Intelligence Layer (Optional Enhancement)

Intelligence Layer AI decisions nahi leti, sirf communication aur explanation ke liye hai.

### Ye Layer Kabhi Participate Nahi Karegi

- Model Selection
- Compatibility checks
- Hardware Analysis
- Rule Processing
- Scoring
- Recommendation generation

### Sirf Itna Karegi

- **Natural Language Understanding**: Wizard mein “Mujhe Python data science setup chahiye” ko structured options mein convert.
- **Explain Recommendation Reports**: Deterministic report ko beginner-friendly language mein samjhana.
- **Generate Readable Summaries**: Installation ke baad summary.
- **Format Outputs**: Better readability, tips.
- **Help Users Understand Technical Concepts**: “Ye quantization kya hai?” type queries.

Intelligence Layer pure optional hai. Bina kisi local AI model ke bhi Orexeva fully functional. Sirf ek lightweight instruction-following local model chahiye, koi heavy reasoning model nahi.

### Provider Lifecycle (for Intelligence Layer)

1. **Provider Initialization**: Config se API key/model path load.
2. **Health Check**: Verify reachable.
3. **Capability Detection**: Streaming, context length.
4. **Model Discovery**: Available models (cloud ke liye).
5. **Chat**: Synchronous/async chat completion.
6. **Streaming**: Token-by-token output.
7. **Shutdown**: Resources release.

Cloud providers optional; local Ollama sufficient.

---

## Repository Philosophy (Expanded)

### Single Responsibility Principle

Har module ka ek clear purpose. Detection sirf detect kare, install nahi.

### Modular Design

`core/`, `cli/`, `platform/`, `installer/`, `recommender/`, `models_db/`, `plugins/` – boundaries clear.

### Dependency Isolation

Modules interfaces ke through communicate, direct internal calls nahi. Testing easy.

### Loose Coupling

Platform layer badalne se Intelligence layer prabhavit nahi.

### High Cohesion

Related functionality ek module mein; model data aur recommendation logic alag.

### Configuration Driven Development

Code behavior data se control hota hai.

### Plugin Architecture

Dynamic discovery, hook points. Community plugins extend karein bina core change.

#### Plugin Security

- **Plugin Permissions**: Declared permissions, user approval.
- **Plugin Verification**: Signed plugins from trusted marketplace.
- **Plugin Isolation**: Separate process or virtual env.
- **Trusted Sources**: Curated marketplace, sideloading with warning.
- **Future Marketplace Review**: Automated scan + human review.

### Future Maintainability

Naye OS, naye package manager – bas adapter add karo. Provider change – nayi class. Long-term project healthy.

---

## Development Philosophy

### Feature Based Development

Har feature ek branch pe, main se sync. PR ke through merge.

### Issue Based Development

Pehle issue, discussion, requirement clear, fir implementation.

### Branch Based Development

- `main`: stable, release ready.
- `develop`: integration.
- `feature/xyz`: individual features.
- `fix/abc`: bug fixes.

### Review Process

PRs require review. Automated checks: linting, type checking, cross-platform tests.

### Versioning

Semantic versioning: `MAJOR.MINOR.PATCH`. Breaking changes? MAJOR bump.

### Documentation First

Design doc, user docs, automated doc generation.

### Architecture First, Implementation Later

Is report ka purpose yahi hai – sab aligned.

---

## Non Functional Requirements

### Performance

- Parallel installations.
- Resumable downloads.
- CLI response <500ms.

### Reliability

- Idempotent operations.
- Failure recovery built-in.
- Deterministic rule engine.

### Offline Support

- Core setup offline.
- Configs, profiles bundled.

### Maintainability

- Modular, typed code.
- Configuration-driven – zero code for new tool.
- Structured logging.

### Scalability

- Hundreds of tools without bloat.
- Plugin system scales ecosystem.
- Rule engine/database scale to thousands of models.

### Security

- No telemetry.
- API keys encrypted.
- Least privilege installs.
- Plugin isolation.

### Cross Platform Compatibility

- Windows 10+, macOS 12+, Ubuntu 20.04+.
- ARM/x86 transparent.

### Low Resource Usage

- Orexeva lightweight ~50MB, minimal RAM.

### Fast Startup

- Wizard instant, state detection <2 sec.

### Minimal Dependencies

- Only essential Python libraries; self-contained binary.

---

## Privacy & Telemetry

Orexeva developer ka personal assistant hai. Privacy sabse upar.

- **Completely Offline by Default**: Internet sirf model pull/update ke liye.
- **Telemetry Disabled**: Zero data collection.
- **No Personal Data Collection**: Sirf wahi data jo user explicitly de (encrypted).
- **No Mandatory Cloud Account**: Purely local.
- **Local Data Ownership**: Sab configs, logs, models user ke paas.
- **User Controls Everything**: Logs delete kar sakte hain, kuch bhi bahar nahi.

Ye Local AI First aur Developer First ke saath aligned hai.

---

## Minimum Viable Product (MVP)

Version 1 mein sirf core commands:

- **`orexeva setup`**: Basic wizard, predefined profiles, essential tools, deterministic recommendation, verification. No Intelligence Layer.
- **`orexeva doctor`**: Tools version, PATH, Ollama status.
- **`orexeva recommend`**: Deterministic report.
- **`orexeva models`**: List, pull, remove.
- **`orexeva update`**: Self-update, config updates.

Baaki features (`repair`, `backup/restore`, `workspace`, etc.) future versions mein. Complexity kam, jaldi ship, real user feedback, stable foundation.

---

## Future Scope

### 1. Orexeva Cloud Sync

Profiles, dotfiles sync encrypted; self-hosted option.

### 2. Remote Development Setup

Cloud VM pe remote `orexeva setup` via SSH.

### 3. Team Profiles as Code

`orexeva.yaml` commit, CI/CD reproduce environment.

### 4. Live Collaboration in Dashboard

Terminal-based pair programming.

### 5. Local AI Agent Platform

Agents jo test, lint, PR generate karein.

### 6. Plugin Marketplace

CLI se search, install; community curated.

### 7. IDE Deep Integration

VS Code extension Orexeva backend se connected.

### 8. Learning Paths

“I want to learn X” wizard, tools+models+project templates.

### 9. Containerized Development

Dev container generation, Docker Dev Environments.

### 10. Automatic Dependency Resolution

Tool dependencies auto install.

---

## Success Metrics

- **Fresh PC setup under 20 minutes**: Blank machine pe complete ≤20 min.
- **95% automated installation**: 95% steps bina manual intervention.
- **Zero manual configuration**: Wizard ke baad koi file edit nahi.
- **Cross-platform compatibility**: Windows/macOS/Linux flawless.
- **Single command onboarding**: `orexeva import` se instant ready.
- **Doctor success rate**: 90% issues `repair --all` se fix.
- **Offline capability**: `orexeva setup` bina internet (cached models) error-free.

---

## Final Vision – Evolution Stages

Orexeva sirf installer nahi, ek **Developer Infrastructure Platform** hai.

### Stage 1 – Setup Tool

Ek command se developer-ready. Basic AI setup, configuration driven.

### Stage 2 – Developer Infrastructure Platform

Backup/restore, team profiles, import/export, onboarding automation.

### Stage 3 – AI Development Platform

Local AI agents, project assistants, learning paths, dashboard.

### Stage 4 – Complete Developer Ecosystem

Plugin marketplace, community model database, cloud sync, enterprise management.

**Long-term Dream**: Pehla software jo fresh machine pe install ho — Orexeva. Kuch minutes mein sab ready, local AI saath, privacy intact, productivity skyrocket. Open source community aur aage le jaaye.

> **Orexeva trusts deterministic engineering for decisions and uses intelligence only for communication.**

---

*Yeh report Orexeva ke blueprint ke roop mein likhi gayi hai. Har decision, har philosophy, har feature ko detail mein samjhane ka prayaas kiya gaya hai. Ab jab hum code likhne baithenge, toh sabko clear hoga ki hum kya bana rahe hain, kyun bana rahe hain, aur kaise bana rahe hain.*

> “Pahle socho, fir samjho, fir banao.” – Orexeva Way.

---

## End of Document
