# CLAUDE.md — AI Assistant Guide for CS-5260

This file provides context, conventions, and workflows for AI assistants (like Claude) working in this repository.

---

## Project Overview

**Course:** Vanderbilt CS-5260 — Artificial Intelligence
**Author:** johnford2002
**Purpose:** Implement and experiment with AI search strategies applied to a multi-agent world trading simulation.

The primary deliverable is **WorldTraderSim** — a Python application where an AI agent generates optimal trade/transform schedules to maximize a country's resource quality using graph search algorithms.

A secondary package, **ReferenceCode**, contains canonical search algorithm implementations used as a reference library.

---

## Repository Layout

```
CS-5260/
├── WorldTraderSim/                  # Primary project
│   ├── src/WorldTraderSim/          # Application source
│   │   ├── main.py                  # Entry point (CLI)
│   │   ├── graph_schedule.py        # Visualization script
│   │   ├── Constants.py             # Required resource names & transform keywords
│   │   ├── DataTypes/               # Domain model entities
│   │   │   ├── Country.py           # Country state (resources map)
│   │   │   ├── Node.py              # Search tree node (hashed state, cached depth)
│   │   │   ├── Action.py            # Abstract base action
│   │   │   ├── TransferAction.py    # Inter-country resource transfer
│   │   │   ├── TransformAction.py   # Intra-country resource transformation
│   │   │   ├── Schedule.py          # Action sequence; CSV/JSON output
│   │   │   ├── Solution.py          # Search result with path and cost
│   │   │   ├── Heuristic.py         # Callable heuristic wrapper
│   │   │   ├── PriorityQueue.py     # Frontier priority queue
│   │   │   ├── ResourceQuantity.py  # Resource name + amount pair
│   │   │   └── ResourceTemplate.py  # Resource metadata (weights, transferability)
│   │   ├── Evaluators/
│   │   │   ├── StateEvaluator.py    # Weighted resource quality score for a country
│   │   │   └── ScheduleEvaluator.py # Expected utility via discounted reward + logistic acceptance
│   │   ├── Parsers/
│   │   │   ├── StateParser.py       # CSV → initial state / resource list
│   │   │   └── TransformTemplateParser.py  # .tmpl → TransformTemplate objects
│   │   ├── SearchStrategies/
│   │   │   ├── SearchStrategy.py             # Abstract base (depth bound, frontier size)
│   │   │   ├── HeuristicDepthFirstSearch.py  # Primary strategy with reached-state tracking
│   │   │   └── BestFirstSearch.py            # Greedy best-first variant
│   │   ├── ProblemFormulations/
│   │   │   ├── Problem.py           # Abstract base problem
│   │   │   ├── ImplicitGraph.py     # On-demand node expansion (main formulation)
│   │   │   └── ExplicitGraph.py     # Pre-computed graph structure
│   │   └── data/
│   │       ├── states/              # CSV files for initial states and resources
│   │       ├── templates/base/      # .tmpl files defining transform actions
│   │       └── schedules/           # Generated schedule outputs
│   ├── requirements.txt             # matplotlib, numpy, pandas, seaborn (pinned)
│   ├── setup.cfg                    # Package metadata, Python 3.8-3.11
│   └── pyproject.toml               # Build backend (setuptools + wheel)
├── ReferenceCode/                   # Reference search library
│   ├── src/cs5260/
│   │   ├── DataTypes/               # Canonical State, Action, Node, Solution, Heuristic
│   │   ├── SearchStrategies/        # DFS, BFS, UCS, Greedy BFS, HDFS
│   │   ├── ProblemFormulations/     # Explicit/implicit graph
│   │   └── Examples/HW2_1.py        # Homework example usage
│   └── setup.py / requirements.txt
├── docs/
│   ├── STATE_QUALITY.md             # State quality function design
│   ├── SCHEDULE_EVALUATION.md       # EU mathematics (logistic, discounted reward)
│   └── ProgrammingProjectPart1.pdf  # Original project spec
├── README.md                        # Setup and CLI reference
├── CHANGELOG.md                     # Part 1 → Part 2 improvements
├── FINDINGS.md                      # Search performance research notes
├── test_cases_summary.md            # Documented test scenarios (manual)
└── test_cases_summary2.md           # Additional test summaries
```

---

## Development Setup

```bash
cd CS-5260/WorldTraderSim
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Python version:** 3.8–3.11
**Dependencies (pinned):** matplotlib 3.6.3, numpy 1.24.1, pandas 1.5.3, seaborn 0.12.2

> Run all `main.py` commands from inside `WorldTraderSim/` because the script resolves paths relative to its own location (`SCRIPT_PATH`).

---

## Running the Simulation

### Generate a schedule

```bash
python src/WorldTraderSim/main.py
```

With arguments:

```bash
python src/WorldTraderSim/main.py \
  -c Atlantis \
  -i initial-balanced.csv \
  -r resources-balanced.csv \
  -n 3 \
  -d 100 \
  -f 20000 \
  -l 20
```

### Visualize the best schedule

```bash
python src/WorldTraderSim/graph_schedule.py
```

### CLI Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `-c, --country-name` | `Atlantis` | Self country for the AI agent |
| `-s, --state-dir` | `SCRIPT_PATH/data/states/` | Directory with state CSVs |
| `-r, --resources-file` | `resources.csv` | CSV defining resource metadata |
| `-i, --initial-state-file` | `initial.csv` | CSV defining initial world state |
| `-o, --output-file` | `schedules.txt` | Output file for generated schedules |
| `-n, --num-schedules` | `1` | Number of schedules to generate |
| `-d, --depth-bound` | `100` | Maximum search depth |
| `-f, --frontier-size` | `20000` | Maximum frontier size |
| `--config` | `SCRIPT_PATH/config.ini` | INI config file path |
| `-l, --logging-level` | `20` (INFO) | Logging verbosity (10/20/30/40/50) |

---

## Configuration File (`config.ini`)

The config file is **not committed** to the repo; defaults are applied via `fallback=` in `configparser`. To override, create `WorldTraderSim/src/WorldTraderSim/config.ini`:

```ini
[Actions]
Shuffle = True
TransferQuantityMax = 5
TransformQuantityMax = 1

[Search]
Strategy = HeuristicDepthFirstSearch
EnableReached = True

[ScheduleEvaluation]
FailedImpact = -0.35
LengthImpact = 0.999
LogisticFunctionMidpoint = -1
LogisticFunctionGrowth = 1
ForceSelfAccept = False
```

**Key tuning notes:**
- `TransferQuantityMax = 5` creates 5 transfer actions per resource (quantities 1-5), yielding ~40 base transfer branches.
- When increasing `depth-bound`, watch logs for "Max Frontier Length" — if it approaches `frontier-size`, results degrade.
- `HeuristicDepthFirstSearch` with `EnableReached = True` is the best-performing configuration.

---

## Core Domain Concepts

### Resources

Nine **required** resources are defined in `Constants.py`:

```
Population, MetallicElements, Timber, MetallicAlloys, MetallicAlloysWaste,
Electronics, ElectronicsWaste, Housing, HousingWaste
```

Extended resources (Part 2 additions): `Housing2`, `Housing3`, `Electronics2`, `Electronics3`.

### Actions

| Type | Class | Description |
|------|-------|-------------|
| Transfer | `TransferAction` | Move a single resource between two countries (SEND or RECEIVE) |
| Transform | `TransformAction` | Convert inputs → outputs within a single country via a `.tmpl` template |

### Transform Templates (`.tmpl` files)

Located in `data/templates/base/`. Format:

```
(TRANSFORM <name>
  (INPUTS  (<resource> <qty>) ...)
  (OUTPUTS (<resource> <qty>) ...))
```

### State Quality

`StateEvaluator.state_quality(country)` returns a weighted sum of a country's normalized resource holdings. Weights and normalizations come from the `ResourceTemplate` objects loaded from the resources CSV. See `docs/STATE_QUALITY.md` for the full formula.

### Expected Utility (Schedule Evaluation)

`ScheduleEvaluator.expected_utility(country, schedule)` computes:

```
EU = Σ (γ^n * ΔQ_n) * P_accept - C * P_fail
```

Where:
- `γ` (LengthImpact) = discount factor per step
- `P_accept` = logistic function of discounted reward delta relative to other countries
- `C` (FailedImpact) = failure penalty coefficient

See `docs/SCHEDULE_EVALUATION.md` for full mathematics.

---

## Search Strategies

The active strategy is selected via `config.ini` `[Search] Strategy` and instantiated through `search_strategy_factory()` in `SearchStrategies/__init__.py`.

| Strategy | Class | Notes |
|----------|-------|-------|
| `HeuristicDepthFirstSearch` | `HeuristicDepthFirstSearch` | **Default / best-performing.** DFS guided by heuristic with optional reached-state pruning. |
| `BestFirstSearch` | `BestFirstSearch` | Greedy best-first; explores best heuristic node first. |
| BFS/DFS/UCS | (ReferenceCode) | Available in reference library for comparison. |

**Reached-state pruning** (`EnableReached = True`): tracks visited state hashes in a set to skip revisiting equivalent world states, significantly reducing redundant computation.

---

## Code Conventions

### Python Style

- **`from __future__ import annotations`** — used for forward type references; include this at the top of all new modules.
- **Type hints** — all function signatures must have complete type annotations using `typing` (Dict, List, Callable, Optional, Union).
- **Dataclasses** — domain types use `@dataclass` with `field(default_factory=...)` for mutable defaults.
- **Naming:**
  - Class-level constants: `UPPER_SNAKE_CASE` (e.g., `STATE_HASH`, `DEPTH`)
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
- **Deep copies** — always `copy.deepcopy()` when passing state between search iterations to avoid mutation bugs.

### File Organization

- New DataTypes go in `DataTypes/` with a corresponding export added to `DataTypes/__init__.py`.
- New search strategies go in `SearchStrategies/` and must be registered in `search_strategy_factory()`.
- New evaluators go in `Evaluators/`.
- Data files (CSVs, templates) belong in `data/states/` or `data/templates/base/` respectively.

### Logging

Use the `logging` module (never `print`) at the appropriate level:

| Level | Use |
|-------|-----|
| `DEBUG` | Detailed state values, intermediate computations |
| `INFO` | High-level progress, counts, key metric values |
| `WARNING` | Unexpected-but-recoverable situations |
| `ERROR` / `CRITICAL` | Fatal errors before raising an exception |

### Error Handling

- Validate at system boundaries (CSV parsing, CLI input) and raise descriptive `Exception` messages.
- Internal functions can trust that inputs have already been validated upstream.
- Use `configparser` `.getint()` / `.getfloat()` / `.getboolean()` with a `fallback=` default — never assume a config key exists.

### Performance Patterns

- **State hash caching** — `Node.STATE_HASH` is computed once (MD5) and cached; do not recompute it.
- **Depth caching** — `Node.DEPTH` is cached; do not recount ancestor links.
- **Reached set** — uses string hashes, not full node objects, to minimize memory usage.
- **Frontier bounding** — the frontier is capped at `frontier-size`; stay within this constraint when modifying search logic.

---

## Testing

There is **no automated test suite** (no pytest, unittest, or CI pipeline). Testing is documented manually:

- `test_cases_summary.md` — 5 detailed scenario descriptions with parameters and expected outcomes.
- `test_cases_summary2.md` — additional concise test summaries.

**When making changes, manually verify against these scenarios:**
1. Run with default settings: `python src/WorldTraderSim/main.py`
2. Confirm schedule output appears in `schedules.txt` and `best_solution.csv`.
3. Confirm state quality improves (log line: `Final Agent Country State Quality > Start Agent Country State Quality`).
4. Run `graph_schedule.py` to visually confirm EU trajectory is non-decreasing.

---

## Git Workflow

**Active branch convention:** Feature branches follow `claude/<description>-<id>` naming.

```bash
# Switch to or create the feature branch
git checkout -b claude/<description>-<id>

# Stage and commit
git add <specific-files>
git commit -m "Descriptive message"

# Push
git push -u origin claude/<description>-<id>
```

**Never push directly to `master` or `main`.** The CODEOWNERS file assigns `@johnford2002` as the required reviewer.

---

## Key Files Quick Reference

| File | What it does |
|------|-------------|
| `main.py` | Orchestrates the full pipeline: load → build actions → search → output |
| `Constants.py` | Defines `REQUIRED_RESOURCES` list used for validation |
| `StateEvaluator.py` | `state_quality(country)` → float |
| `ScheduleEvaluator.py` | `expected_utility(country, schedule)` → float |
| `HeuristicDepthFirstSearch.py` | Core search algorithm |
| `ImplicitGraph.py` | Defines successor/action application logic |
| `Node.py` | Search tree node; holds `STATE`, `ACTION`, `PARENT`, `STATE_HASH`, `DEPTH` |
| `Schedule.py` | Wraps a terminal node into an action sequence; writes outputs |
| `StateParser.py` | `read_csv()` + `validate_initial_state()` / `validate_resources()` |
| `TransformTemplateParser.py` | `parse(path)` → `TransformTemplate` |

---

## Common Pitfalls

1. **Running from the wrong directory** — `main.py` uses `SCRIPT_PATH` for default data paths. Always `cd WorldTraderSim` before running.
2. **Mutating shared state** — always deep-copy `country_states` before passing into a new search iteration.
3. **Missing config fallbacks** — if you add a new `config.ini` option, always supply a `fallback=` value so the code runs without a config file.
4. **Frontier overflow** — increasing `depth-bound` without increasing `frontier-size` proportionally causes the frontier to cap and degrade search quality.
5. **Adding a resource without updating `Constants.py`** — `StateParser.validate_resources()` checks against `REQUIRED_RESOURCES`; new required resources must be added there.
6. **Forgetting to register a new search strategy** — `search_strategy_factory()` must be updated to map string names to new strategy classes.
