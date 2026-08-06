#!/usr/bin/env python3
"""Validate the TaskFlow Phase 2 project foundation without editing repository files."""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"

Status = Literal["PASS", "FAIL", "SKIP"]

REQUIRED_FILES = (
    ".gitignore",
    "package.json",
    "package-lock.json",
    "compose.yaml",
    "frontend/.env.example",
    "frontend/Dockerfile",
    "frontend/package.json",
    "frontend/package-lock.json",
    "frontend/next.config.ts",
    "frontend/tsconfig.json",
    "frontend/vitest.config.mts",
    "frontend/vitest.setup.ts",
    "frontend/src/app/globals.css",
    "frontend/src/app/layout.tsx",
    "frontend/src/app/page.tsx",
    "frontend/src/components/system-status.tsx",
    "frontend/src/lib/api.ts",
    "frontend/src/lib/env.ts",
    "frontend/src/tests/system-status.test.tsx",
    "backend/.env.example",
    "backend/.python-version",
    "backend/Dockerfile",
    "backend/pyproject.toml",
    "backend/uv.lock",
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/api/router.py",
    "backend/app/api/routes/health.py",
    "backend/app/core/config.py",
    "backend/app/schemas/health.py",
    "backend/tests/__init__.py",
    "backend/tests/test_config.py",
    "backend/tests/test_health.py",
    "docs/phase-2/architecture-foundation.md",
    "docs/phase-2/local-development.md",
    "docs/phase-2/acceptance-criteria.md",
    "scripts/validate_phase_2.py",
)

BACKEND_STRUCTURE_FILES = (
    "backend/app/main.py",
    "backend/app/api/router.py",
    "backend/app/api/routes/health.py",
    "backend/app/core/config.py",
    "backend/tests/test_config.py",
    "backend/tests/test_health.py",
    "backend/pyproject.toml",
    "backend/uv.lock",
)

FRONTEND_STRUCTURE_FILES = (
    "frontend/src/app/page.tsx",
    "frontend/src/components/system-status.tsx",
    "frontend/src/lib/api.ts",
    "frontend/vitest.config.mts",
    "frontend/src/tests/system-status.test.tsx",
    "frontend/package-lock.json",
)

EXTERNAL_EXAMPLE_KEYS = frozenset(
    {
        "GROQ_API_KEY",
        "GROQ_MODEL",
        "SUPABASE_URL",
        "SUPABASE_PUBLISHABLE_KEY",
        "SUPABASE_SECRET_KEY",
        "DATABASE_URL",
        "NEXT_PUBLIC_SUPABASE_URL",
        "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY",
    }
)

LIKELY_SECRET_PATTERNS = (
    ("Groq-style API key", re.compile(r"\bgsk_[A-Za-z0-9_-]{16,}\b")),
    ("provider secret key", re.compile(r"\b(?:sk-|sb_secret_)[A-Za-z0-9_-]{16,}\b")),
    ("JWT-like token", re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}")),
    (
        "database URL containing credentials",
        re.compile(r"\bpostgres(?:ql)?://[^\s:/]+:[^\s@]+@", re.IGNORECASE),
    ),
    ("private key material", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)

PROHIBITED_BACKEND_IMPORTS = frozenset(
    {
        "docling",
        "groq",
        "langchain",
        "langchain_groq",
        "langchain_postgres",
        "langgraph",
        "sentence_transformers",
        "supabase",
        "torch",
    }
)

PROHIBITED_BACKEND_DEPENDENCIES = frozenset(
    {
        "docling",
        "groq",
        "langchain",
        "langchain-groq",
        "langchain-postgres",
        "langgraph",
        "sentence-transformers",
        "supabase",
        "torch",
    }
)

PROHIBITED_CALL_NAMES = frozenset(
    {
        "ChatGroq",
        "Groq",
        "HuggingFaceEmbeddings",
        "PGVector",
        "SentenceTransformer",
        "SupabaseVectorStore",
        "create_client",
        "embed_documents",
        "embed_query",
    }
)

PROHIBITED_IMPLEMENTATION_PATH_TERMS = frozenset(
    {
        "auth",
        "authentication",
        "chat",
        "database",
        "db",
        "document_ingestion",
        "embedding",
        "embeddings",
        "ingest",
        "ingestion",
        "login",
        "migrations",
        "rag",
        "signin",
        "sign-in",
        "signup",
        "sign-up",
        "vector_store",
    }
)


@dataclass(frozen=True)
class GroupResult:
    """Outcome for one validator group."""

    status: Status
    name: str
    messages: tuple[str, ...] = ()


@dataclass(frozen=True)
class CommandCheck:
    """One external quality command executed without a shell."""

    label: str
    arguments: tuple[str, ...]
    working_directory: Path


def relative(path: Path) -> str:
    """Return a stable repository-relative display path."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def missing_file_errors(paths: tuple[str, ...]) -> list[str]:
    """Return actionable errors for missing files."""
    errors: list[str] = []
    for path in paths:
        if not (ROOT / path).is_file():
            errors.append(f"Create the missing required file: {path}")
    return errors


def validate_required_files() -> GroupResult:
    """Verify the complete Phase 2 foundation file set."""
    errors = missing_file_errors(REQUIRED_FILES)
    return GroupResult("FAIL" if errors else "PASS", "Required files", tuple(errors))


def validate_phase_1_preservation() -> GroupResult:
    """Verify the Phase 1 directory and its validator remain present."""
    errors: list[str] = []
    phase_one_directory = ROOT / "docs/phase-1"
    if not phase_one_directory.is_dir():
        errors.append("Restore the preserved Phase 1 directory: docs/phase-1/")
    elif not any(phase_one_directory.iterdir()):
        errors.append("Restore the Phase 1 artifacts; docs/phase-1/ is empty.")

    phase_one_validator = ROOT / "scripts/validate_phase_1.py"
    if not phase_one_validator.is_file():
        errors.append("Restore the Phase 1 validator: scripts/validate_phase_1.py")

    return GroupResult("FAIL" if errors else "PASS", "Phase 1 preservation", tuple(errors))


def read_utf8(path: Path) -> tuple[str | None, str | None]:
    """Read UTF-8 content or return a useful validation error."""
    try:
        return path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return None, f"Create the missing file: {relative(path)}"
    except UnicodeDecodeError as exc:
        return None, f"Save {relative(path)} as UTF-8 ({exc})."
    except OSError as exc:
        return None, f"Unable to read {relative(path)}: {exc}"


def tracked_environment_errors() -> list[str]:
    """Find tracked environment files while allowing committed examples."""
    if shutil.which("git") is None:
        return ["Install Git so tracked environment files can be verified."]

    try:
        result = subprocess.run(
            ("git", "ls-files", "-z"),
            cwd=ROOT,
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"Unable to inspect tracked files with Git: {exc}"]

    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip() or "unknown Git error"
        return [f"Run the validator inside a Git worktree so env safety can be checked ({detail})."]

    errors: list[str] = []
    for raw_path in filter(None, result.stdout.split(b"\0")):
        tracked_path = raw_path.decode("utf-8", errors="replace")
        name = Path(tracked_path).name.lower()
        is_environment_file = name == ".env" or (
            name.startswith(".env.") and name != ".env.example"
        )
        if is_environment_file:
            errors.append(
                f"Remove {tracked_path} from Git tracking, rotate any contained secrets, and keep "
                "only an .env.example file."
            )
    return errors


def frontend_secret_reference_errors() -> list[str]:
    """Reject server-only secret names from executable frontend source."""
    errors: list[str] = []
    source_directory = FRONTEND / "src"
    if not source_directory.is_dir():
        return ["Create frontend/src/ before frontend secret boundaries can be checked."]

    source_suffixes = {".js", ".jsx", ".mjs", ".ts", ".tsx", ".mts"}
    for path in sorted(source_directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in source_suffixes:
            continue
        content, error = read_utf8(path)
        if error:
            errors.append(error)
            continue
        assert content is not None
        for forbidden_name in ("GROQ_API_KEY", "SUPABASE_SECRET_KEY"):
            if forbidden_name in content:
                errors.append(
                    f"Remove server-only {forbidden_name} from frontend source: {relative(path)}"
                )
    return errors


def placeholder_safety_errors() -> list[str]:
    """Detect populated future-service values and common real-secret shapes in examples."""
    errors: list[str] = []
    for path in (FRONTEND / ".env.example", BACKEND / ".env.example"):
        content, error = read_utf8(path)
        if error:
            errors.append(error)
            continue
        assert content is not None

        for line_number, raw_line in enumerate(content.splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", maxsplit=1)
            if key.strip() in EXTERNAL_EXAMPLE_KEYS and value.strip():
                errors.append(
                    f"Clear future-service value {key.strip()} in {relative(path)}:{line_number}; "
                    "Phase 2 examples must use an empty placeholder."
                )

        for description, pattern in LIKELY_SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(
                    f"Replace likely {description} in {relative(path)} with an empty placeholder."
                )
    return errors


def validate_environment_safety() -> GroupResult:
    """Verify tracked env files, frontend boundaries, and placeholder safety."""
    errors = missing_file_errors(("frontend/.env.example", "backend/.env.example"))
    errors.extend(tracked_environment_errors())
    errors.extend(frontend_secret_reference_errors())
    errors.extend(placeholder_safety_errors())
    return GroupResult("FAIL" if errors else "PASS", "Environment safety", tuple(errors))


def validate_backend_structure() -> GroupResult:
    """Verify the backend application, routes, configuration, tests, and locks."""
    errors = missing_file_errors(BACKEND_STRUCTURE_FILES)
    return GroupResult("FAIL" if errors else "PASS", "Backend structure", tuple(errors))


def validate_frontend_structure() -> GroupResult:
    """Verify the App Router, health client, test setup, and lockfile."""
    errors = missing_file_errors(FRONTEND_STRUCTURE_FILES)
    return GroupResult("FAIL" if errors else "PASS", "Frontend structure", tuple(errors))


def command_output_excerpt(result: subprocess.CompletedProcess[str]) -> str:
    """Return a bounded, readable failure excerpt."""
    combined = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    if not combined:
        return "The command produced no output."
    lines = combined.splitlines()
    return "\n".join(lines[-40:])


def run_command_checks(name: str, checks: tuple[CommandCheck, ...]) -> GroupResult:
    """Run every command in a group and collect all genuine failures."""
    errors: list[str] = []
    command_environment = os.environ.copy()
    command_environment.update(
        {
            "CI": "1",
            "FORCE_COLOR": "0",
            "NEXT_TELEMETRY_DISABLED": "1",
            "NO_COLOR": "1",
        }
    )

    for check in checks:
        executable = check.arguments[0]
        if shutil.which(executable) is None:
            errors.append(
                f"Install {executable} and rerun {check.label}: {' '.join(check.arguments)}"
            )
            continue
        try:
            result = subprocess.run(
                check.arguments,
                cwd=check.working_directory,
                env=command_environment,
                check=False,
                capture_output=True,
                text=True,
                timeout=900,
            )
        except subprocess.TimeoutExpired:
            command = " ".join(check.arguments)
            location = relative(check.working_directory) or "."
            errors.append(
                f"{check.label} timed out after 900 seconds. Diagnose the hanging command and "
                f"rerun `{command}` from {location}."
            )
            continue
        except OSError as exc:
            errors.append(f"Unable to run {check.label}: {exc}")
            continue

        if result.returncode != 0:
            command = " ".join(check.arguments)
            location = relative(check.working_directory) or "."
            errors.append(
                f"{check.label} failed with exit code {result.returncode}. Fix the output and "
                f"rerun `{command}` from {location}:\n{command_output_excerpt(result)}"
            )

    return GroupResult("FAIL" if errors else "PASS", name, tuple(errors))


def validate_api_behavior() -> GroupResult:
    """Run backend tests through the uv-managed environment."""
    return run_command_checks(
        "API behavior",
        (CommandCheck("backend pytest", ("uv", "run", "pytest"), BACKEND),),
    )


def validate_backend_quality() -> GroupResult:
    """Run Ruff lint, Ruff format check, and mypy."""
    return run_command_checks(
        "Backend quality",
        (
            CommandCheck("Ruff lint", ("uv", "run", "ruff", "check", "."), BACKEND),
            CommandCheck(
                "Ruff format check",
                ("uv", "run", "ruff", "format", "--check", "."),
                BACKEND,
            ),
            CommandCheck("mypy", ("uv", "run", "mypy", "app"), BACKEND),
        ),
    )


def validate_frontend_quality() -> GroupResult:
    """Run frontend linting, type checking, tests, and production build."""
    return run_command_checks(
        "Frontend quality",
        (
            CommandCheck("frontend lint", ("npm", "run", "lint"), FRONTEND),
            CommandCheck("frontend typecheck", ("npm", "run", "typecheck"), FRONTEND),
            CommandCheck("frontend tests", ("npm", "run", "test"), FRONTEND),
            CommandCheck("frontend build", ("npm", "run", "build"), FRONTEND),
        ),
    )


def imported_module_names(tree: ast.AST) -> set[str]:
    """Collect top-level Python import names from an AST."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", maxsplit=1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", maxsplit=1)[0])
    return names


def called_name(node: ast.Call) -> str | None:
    """Return the final identifier for a Python call."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def implementation_path_errors() -> list[str]:
    """Detect source modules and routes reserved for later phases."""
    errors: list[str] = []
    implementation_roots = (BACKEND / "app", FRONTEND / "src")
    source_suffixes = {".js", ".jsx", ".mjs", ".py", ".ts", ".tsx", ".mts"}

    for source_root in implementation_roots:
        if not source_root.is_dir():
            continue
        for path in sorted(source_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in source_suffixes:
                continue
            relative_parts = [part.lower() for part in path.relative_to(source_root).parts]
            normalized_stem = path.stem.lower().replace("-", "_")
            path_terms = set(relative_parts[:-1]) | {normalized_stem}
            matches = sorted(PROHIBITED_IMPLEMENTATION_PATH_TERMS & path_terms)
            if matches:
                errors.append(
                    f"Remove later-phase implementation file {relative(path)} (matched: "
                    f"{', '.join(matches)})."
                )
    return errors


def backend_implementation_errors() -> list[str]:
    """Use Python syntax to detect active external-service and RAG implementations."""
    errors: list[str] = []
    app_directory = BACKEND / "app"
    if not app_directory.is_dir():
        return errors

    for path in sorted(app_directory.rglob("*.py")):
        content, error = read_utf8(path)
        if error:
            errors.append(error)
            continue
        assert content is not None
        try:
            tree = ast.parse(content, filename=str(path))
        except SyntaxError as exc:
            errors.append(
                f"Fix Python syntax in {relative(path)} before scope safety can inspect it: {exc}"
            )
            continue

        prohibited_imports = sorted(PROHIBITED_BACKEND_IMPORTS & imported_module_names(tree))
        if prohibited_imports:
            errors.append(
                f"Remove active later-phase import(s) from {relative(path)}: "
                f"{', '.join(prohibited_imports)}. Runtime integrations are not allowed in Phase 2."
            )

        calls = {
            name
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and (name := called_name(node)) is not None
        }
        prohibited_calls = sorted(PROHIBITED_CALL_NAMES & calls)
        if prohibited_calls:
            errors.append(
                f"Remove active later-phase call(s) from {relative(path)}: "
                f"{', '.join(prohibited_calls)}."
            )
    return errors


def backend_dependency_errors() -> list[str]:
    """Reject direct dependency declarations reserved for later phases."""
    pyproject_path = BACKEND / "pyproject.toml"
    try:
        with pyproject_path.open("rb") as pyproject_file:
            pyproject = tomllib.load(pyproject_file)
    except FileNotFoundError:
        return ["Create backend/pyproject.toml before dependency scope can be checked."]
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"Fix backend/pyproject.toml before dependency scope can be checked: {exc}"]

    declared_dependencies = pyproject.get("project", {}).get("dependencies", [])
    if not isinstance(declared_dependencies, list):
        return ["Make project.dependencies an array in backend/pyproject.toml."]

    prohibited: list[str] = []
    for declaration in declared_dependencies:
        if not isinstance(declaration, str):
            continue
        match = re.match(r"[A-Za-z0-9_.-]+", declaration)
        if match is None:
            continue
        dependency_name = match.group(0).lower().replace("_", "-")
        if dependency_name in PROHIBITED_BACKEND_DEPENDENCIES:
            prohibited.append(dependency_name)

    if not prohibited:
        return []
    return [
        "Remove later-phase backend dependency declaration(s) from backend/pyproject.toml: "
        + ", ".join(sorted(set(prohibited)))
    ]


def frontend_implementation_errors() -> list[str]:
    """Detect active Supabase/authentication client code without scanning documentation."""
    errors: list[str] = []
    source_directory = FRONTEND / "src"
    if not source_directory.is_dir():
        return errors

    active_patterns = (
        ("Supabase client import", re.compile(r"from\s+['\"]@supabase/")),
        ("Supabase client creation", re.compile(r"\bcreateClient\s*\(")),
        ("authentication invocation", re.compile(r"\.auth\.(?:signIn|signUp|signOut)\w*\s*\(")),
    )
    for path in sorted(source_directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".js", ".jsx", ".ts", ".tsx"}:
            continue
        content, error = read_utf8(path)
        if error:
            errors.append(error)
            continue
        assert content is not None
        for description, pattern in active_patterns:
            if pattern.search(content):
                errors.append(
                    f"Remove active later-phase {description} from frontend source: "
                    f"{relative(path)}"
                )
    return errors


def sql_migration_errors() -> list[str]:
    """Find SQL implementation files while pruning generated and documentation trees."""
    errors: list[str] = []
    excluded_directories = {
        ".git",
        ".mypy_cache",
        ".next",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "docs",
        "node_modules",
        "sample-data",
    }
    for current_directory, directory_names, file_names in os.walk(ROOT):
        directory_names[:] = [name for name in directory_names if name not in excluded_directories]
        current_path = Path(current_directory)
        for file_name in file_names:
            if file_name.lower().endswith(".sql"):
                path = current_path / file_name
                errors.append(f"Remove Phase 3 SQL or migration implementation: {relative(path)}")
    return errors


def validate_scope_safety() -> GroupResult:
    """Reject real later-phase code while ignoring docs, examples, and dependency locks."""
    errors = implementation_path_errors()
    errors.extend(backend_dependency_errors())
    errors.extend(backend_implementation_errors())
    errors.extend(frontend_implementation_errors())
    errors.extend(sql_migration_errors())
    return GroupResult("FAIL" if errors else "PASS", "Scope safety", tuple(errors))


def validate_docker() -> GroupResult:
    """Validate Compose when Docker and its Compose plugin are available."""
    if shutil.which("docker") is None:
        return GroupResult(
            "SKIP",
            "Docker",
            ("Docker CLI is unavailable; install Docker to run `docker compose config`.",),
        )

    try:
        compose_version = subprocess.run(
            ("docker", "compose", "version"),
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return GroupResult(
            "SKIP",
            "Docker",
            (f"Docker Compose is unavailable ({exc}); skipping optional Compose validation.",),
        )

    if compose_version.returncode != 0:
        detail = command_output_excerpt(compose_version)
        return GroupResult(
            "SKIP",
            "Docker",
            (f"Docker Compose plugin is unavailable; skipping optional validation: {detail}",),
        )

    try:
        compose_config = subprocess.run(
            ("docker", "compose", "config"),
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return GroupResult(
            "FAIL",
            "Docker",
            (
                "`docker compose config` timed out. Check the Compose installation and "
                "configuration.",
            ),
        )
    except OSError as exc:
        return GroupResult("FAIL", "Docker", (f"Unable to run Docker Compose config: {exc}",))

    if compose_config.returncode != 0:
        return GroupResult(
            "FAIL",
            "Docker",
            (
                "Fix compose.yaml, then rerun `docker compose config`:\n"
                + command_output_excerpt(compose_config),
            ),
        )
    return GroupResult("PASS", "Docker")


def print_result(index: int, result: GroupResult) -> None:
    """Print one group outcome and its supporting messages."""
    print(f"{result.status} {index:02d}. {result.name}")
    for message in result.messages:
        for line in message.splitlines():
            print(f"  - {line}")


def main() -> int:
    """Run every Phase 2 validation group and return a process status."""
    results = (
        validate_required_files(),
        validate_phase_1_preservation(),
        validate_environment_safety(),
        validate_backend_structure(),
        validate_frontend_structure(),
        validate_api_behavior(),
        validate_backend_quality(),
        validate_frontend_quality(),
        validate_scope_safety(),
        validate_docker(),
    )

    for index, result in enumerate(results, start=1):
        print_result(index, result)

    failed = sum(result.status == "FAIL" for result in results)
    passed = sum(result.status == "PASS" for result in results)
    skipped = sum(result.status == "SKIP" for result in results)
    print()
    if failed:
        print(f"RESULT: FAIL ({passed} passed, {failed} failed, {skipped} skipped)")
        return 1

    print(f"RESULT: PASS ({passed} passed, {skipped} skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
