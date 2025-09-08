# ----------------------------
# Noxfile
# ----------------------------
from pathlib import Path
from typing import Any

import nox

# ----------------------------
# Constants / Configuration
# ----------------------------
PYPROJECT: dict[str, Any] = nox.project.load_toml()
PYTHON_VERSIONS: list[str] = nox.project.python_versions(PYPROJECT)
DEFAULT_PYTHON: str = PYTHON_VERSIONS[-1]

# ----------------------------
# Settings
# ----------------------------
nox.options.sessions = ["tests", "check", "docs_build"]
nox.options.reuse_existing_virtualenvs = True


# ----------------------------
# Helper Functions
# ----------------------------
def get_opt_deps(
    group: str,
    pyproject: dict[str, Any] = PYPROJECT,
) -> list[str]:
    """Fetch dependencies for a given group from pyproject.toml."""
    if "optional-dependencies" not in pyproject["project"]:
        raise KeyError("Missing 'optional-dependencies' in pyproject.toml")
    opt_deps = pyproject["project"]["optional-dependencies"]
    if group not in opt_deps:
        raise KeyError(f"Missing group '{group}' in 'optional-dependencies' in pyproject.toml")
    return opt_deps[group]


def load_dotenv(path: Path = Path(".env")) -> dict[str, str]:
    """Load simple .env file (KEY=VALUE) into a dict"""
    if not str(path).endswith(".env"):
        raise ValueError(f"Provided path must end with '.env': {path}")

    env: dict[str, str] = {}
    if not path.exists():
        return env

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def _draft_changelog(session: nox.Session) -> Path:
    """Generate a draft changelog from Towncrier"""
    draft_path = Path("docs/_draft_changelog.md")
    content = session.run("towncrier", "build", "--version", "Upcoming", "--draft", silent=True)
    if not content or "No significant changes" in content:
        return draft_path
    lines = content.splitlines()
    idx = next((i for i, line in enumerate(lines) if line.startswith("##")), None)
    if idx is not None:
        lines[idx] = "## Upcoming changes"
        content = "\n".join(lines[idx:])
    draft_path.write_text(content)
    return draft_path


# ----------------------------
# Dependency constants
# ----------------------------
TEST_DEPS = get_opt_deps("tests")
TYPES_DEPS = get_opt_deps("types")
DOC_DEPS = get_opt_deps("docs")


# ----------------------------
# Dependency constants
# ----------------------------
@nox.session(python=PYTHON_VERSIONS)
def develop(session):
    session.env.update(load_dotenv())
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("-e", ".", *TEST_DEPS, *TYPES_DEPS, *DOC_DEPS, "nox")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    session.install("-e", ".", *TEST_DEPS)
    session.run("pytest", *session.posargs, external=True)
    session.notify("coverage")


@nox.session
def coverage(session: nox.Session) -> None:
    session.install("coverage[toml]")
    session.run("coverage", "report", external=True)
    session.run("coverage", "erase", external=True)


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", external=True)


@nox.session
def typecheck(session: nox.Session) -> None:
    session.install("-e", ".", "mypy", *TEST_DEPS, *TYPES_DEPS)
    session.run("mypy", "--install-types", "--non-interactive", *session.posargs, external=True)


@nox.session(python=DEFAULT_PYTHON)
def check(session: nox.Session) -> None:
    session.notify("lint")
    session.notify("typecheck")


@nox.session(python=DEFAULT_PYTHON)
def build(session: nox.Session) -> None:
    session.install("hatch")
    session.run("python", "-m", "hatch", "build", external=True)
    session.log("Build complete")


@nox.session(python=DEFAULT_PYTHON)
def changelog(session: nox.Session) -> None:
    session.install("towncrier")
    session.run("towncrier", "build", "--version", session.posargs[0], "--yes")


@nox.session(python=DEFAULT_PYTHON)
def docs_serve(session: nox.Session) -> None:
    session.install(*DOC_DEPS, ".")
    draft_changelog = _draft_changelog(session)
    session.run("mkdocs", "serve", "--strict")
    draft_changelog.unlink(missing_ok=True)


@nox.session(python=DEFAULT_PYTHON)
def docs_build(session: nox.Session) -> None:
    session.install(*DOC_DEPS, ".")
    version = session.posargs[0] if session.posargs else "dev"
    alias = session.posargs[1] if len(session.posargs) > 1 else "latest"
    session.run("mike", "deploy", version, alias)
    session.run("mike", "set-default", alias)
