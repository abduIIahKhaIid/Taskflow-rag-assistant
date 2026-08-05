#!/usr/bin/env python3
"""Validate the TaskFlow Phase 1 planning artifacts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PHASE_1_FILES = (
    "docs/phase-1/product-overview.md",
    "docs/phase-1/project-brief.md",
    "docs/phase-1/project-scope.md",
    "docs/phase-1/target-users.md",
    "docs/phase-1/user-stories.md",
    "docs/phase-1/rag-behavior-spec.md",
    "docs/phase-1/ui-wireframes.md",
    "docs/phase-1/acceptance-criteria.md",
    "sample-data/evaluation/test-questions.json",
    "sample-data/evaluation/test-questions.md",
)

KNOWLEDGE_BASE_FILES = (
    "sample-data/knowledge-base/01-getting-started.md",
    "sample-data/knowledge-base/02-plans-and-billing.md",
    "sample-data/knowledge-base/03-account-and-security.md",
    "sample-data/knowledge-base/04-integrations-and-troubleshooting.md",
    "sample-data/knowledge-base/05-cancellation-and-refund-policy.md",
)

REQUIRED_KB_METADATA = (
    "Document ID",
    "Title",
    "Version",
    "Status",
    "Last Updated",
)

REQUIRED_TEST_FIELDS = frozenset(
    {
        "id",
        "category",
        "question",
        "conversation_context",
        "expected_behavior",
        "expected_answer_summary",
        "expected_source_document_ids",
        "required_facts",
        "forbidden_claims",
        "notes",
    }
)

EVALUATION_JSON = ROOT / "sample-data/evaluation/test-questions.json"
EVALUATION_MARKDOWN = ROOT / "sample-data/evaluation/test-questions.md"
TEST_ID_PATTERN = re.compile(r"\bTQ-\d{3}\b")
FICTIONAL_PHRASE = "fictional demonstration saas product"


def relative(path: Path) -> str:
    """Return a repository-relative path for output."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> tuple[str | None, str | None]:
    """Read UTF-8 text and return content or an actionable error."""
    try:
        return path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return None, f"Create the missing file: {relative(path)}"
    except UnicodeDecodeError as exc:
        return None, f"Save {relative(path)} as UTF-8 ({exc})."
    except OSError as exc:
        return None, f"Unable to read {relative(path)}: {exc}"


def parse_front_matter(path: Path) -> tuple[dict[str, str], list[str]]:
    """Parse the simple key/value front matter used by knowledge documents."""
    content, error = read_text(path)
    if error:
        return {}, [error]

    assert content is not None
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [f"Add opening front matter (`---`) to {relative(path)}."]

    metadata: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return metadata, []
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip().strip('"').strip("'")

    return {}, [f"Close the front matter in {relative(path)} with `---`."]


def load_evaluation_json() -> tuple[Any | None, list[str]]:
    """Load the evaluation JSON and report precise parse errors."""
    content, error = read_text(EVALUATION_JSON)
    if error:
        return None, [error]

    assert content is not None
    try:
        return json.loads(content), []
    except json.JSONDecodeError as exc:
        return None, [
            f"Fix invalid JSON in {relative(EVALUATION_JSON)} at "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ]


def test_items(data: Any) -> tuple[list[dict[str, Any]], list[str]]:
    """Return object-shaped test items or errors describing invalid entries."""
    if not isinstance(data, list):
        return [], [
            f"Make {relative(EVALUATION_JSON)} a top-level JSON array of test cases."
        ]

    errors: list[str] = []
    items: list[dict[str, Any]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f"Test item {index} must be a JSON object.")
            continue
        items.append(item)
    return items, errors


def find_obvious_secret_files() -> tuple[list[str], list[str]]:
    """Return tracked files whose names strongly suggest committed secrets."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return [], [f"Install or make Git available so tracked files can be checked: {exc}"]

    if result.returncode != 0:
        detail = result.stderr.strip() or "unknown Git error"
        return [], [f"Run this validator inside the Git repository ({detail})."]

    suspicious: list[str] = []
    exact_names = {
        ".env",
        "credentials.json",
        "service-account.json",
        "id_rsa",
        "id_ed25519",
    }
    secret_suffixes = {".key", ".pem", ".p12", ".pfx"}

    for tracked in filter(None, result.stdout.split("\0")):
        name = Path(tracked).name.lower()
        is_env_variant = name.startswith(".env.") and name != ".env.example"
        if name in exact_names or is_env_variant or Path(name).suffix in secret_suffixes:
            suspicious.append(tracked)

    return suspicious, []


def report(index: int, name: str, errors: list[str]) -> bool:
    """Print one validation result and return whether it passed."""
    status = "PASS" if not errors else "FAIL"
    print(f"{status} {index:02d}. {name}")
    for error in errors:
        print(f"  - {error}")
    return not errors


def main() -> int:
    results: list[bool] = []

    missing_phase_files = [
        path for path in REQUIRED_PHASE_1_FILES if not (ROOT / path).is_file()
    ]
    results.append(
        report(
            1,
            "Required Phase 1 files exist",
            [f"Create the missing required file: {path}" for path in missing_phase_files],
        )
    )

    missing_kb_files = [
        path for path in KNOWLEDGE_BASE_FILES if not (ROOT / path).is_file()
    ]
    results.append(
        report(
            2,
            "All five knowledge-base files exist",
            [f"Create the missing knowledge-base file: {path}" for path in missing_kb_files],
        )
    )

    metadata_by_path: dict[Path, dict[str, str]] = {}
    metadata_errors: list[str] = []
    for file_name in KNOWLEDGE_BASE_FILES:
        path = ROOT / file_name
        if not path.is_file():
            metadata_errors.append(
                f"Cannot validate metadata until {file_name} exists."
            )
            continue
        metadata, parse_errors = parse_front_matter(path)
        metadata_by_path[path] = metadata
        metadata_errors.extend(parse_errors)
        if parse_errors:
            continue
        for field in REQUIRED_KB_METADATA:
            if not metadata.get(field):
                metadata_errors.append(
                    f"Add a non-empty `{field}` value to {file_name} front matter."
                )
    results.append(report(3, "Knowledge-base metadata is complete", metadata_errors))

    document_ids: list[str] = []
    id_errors: list[str] = []
    for path, metadata in metadata_by_path.items():
        document_id = metadata.get("Document ID")
        if document_id:
            document_ids.append(document_id)
        else:
            id_errors.append(
                f"Add `Document ID` to {relative(path)} before uniqueness can be verified."
            )
    duplicate_document_ids = sorted(
        value for value, count in Counter(document_ids).items() if count > 1
    )
    for document_id in duplicate_document_ids:
        id_errors.append(
            f"Assign a unique value to duplicate knowledge-base ID `{document_id}`."
        )
    results.append(report(4, "Knowledge-base document IDs are unique", id_errors))

    evaluation_data, json_errors = load_evaluation_json()
    results.append(report(5, "Evaluation JSON is valid", json_errors))
    items, item_shape_errors = test_items(evaluation_data) if not json_errors else ([], [])

    count_errors = list(item_shape_errors)
    if json_errors:
        count_errors.append("Fix the evaluation JSON before checking the test-case count.")
    elif len(items) != 30:
        count_errors.append(
            f"Add or remove test cases so {relative(EVALUATION_JSON)} contains exactly 30; "
            f"found {len(items)}."
        )
    results.append(report(6, "Exactly 30 evaluation cases exist", count_errors))

    test_id_errors: list[str] = []
    test_ids: list[str] = []
    if json_errors:
        test_id_errors.append("Fix the evaluation JSON before checking test IDs.")
    else:
        test_id_errors.extend(item_shape_errors)
        for index, item in enumerate(items, start=1):
            value = item.get("id")
            if not isinstance(value, str) or not value:
                test_id_errors.append(
                    f"Give test item {index} a non-empty string `id`."
                )
            else:
                test_ids.append(value)
        for test_id, count in sorted(Counter(test_ids).items()):
            if count > 1:
                test_id_errors.append(
                    f"Rename duplicate test ID `{test_id}` so every test ID is unique."
                )
    results.append(report(7, "Evaluation test IDs are unique", test_id_errors))

    field_errors: list[str] = []
    if json_errors:
        field_errors.append("Fix the evaluation JSON before checking required fields.")
    else:
        field_errors.extend(item_shape_errors)
        for index, item in enumerate(items, start=1):
            missing = sorted(REQUIRED_TEST_FIELDS - item.keys())
            if missing:
                label = item.get("id", f"item {index}")
                field_errors.append(
                    f"Add missing field(s) to {label}: {', '.join(missing)}."
                )
    results.append(report(8, "Evaluation cases contain required fields", field_errors))

    source_errors: list[str] = []
    known_document_ids = set(document_ids)
    if json_errors:
        source_errors.append("Fix the evaluation JSON before checking source IDs.")
    elif id_errors:
        source_errors.append(
            "Fix knowledge-base document IDs before checking evaluation source references."
        )
    else:
        for index, item in enumerate(items, start=1):
            label = item.get("id", f"item {index}")
            sources = item.get("expected_source_document_ids")
            if not isinstance(sources, list):
                source_errors.append(
                    f"Make `expected_source_document_ids` an array in {label}."
                )
                continue
            for source_id in sources:
                if not isinstance(source_id, str):
                    source_errors.append(
                        f"Use string source IDs in {label}; found {source_id!r}."
                    )
                elif source_id not in known_document_ids:
                    source_errors.append(
                        f"Replace unknown source ID `{source_id}` in {label} with an "
                        "existing knowledge-base Document ID."
                    )
    results.append(report(9, "Expected source document IDs exist", source_errors))

    no_answer_errors: list[str] = []
    if json_errors:
        no_answer_errors.append("Fix the evaluation JSON before checking no-answer cases.")
    else:
        for index, item in enumerate(items, start=1):
            if item.get("expected_behavior") != "no_answer":
                continue
            label = item.get("id", f"item {index}")
            sources = item.get("expected_source_document_ids")
            if sources != []:
                no_answer_errors.append(
                    f"Set `expected_source_document_ids` to [] for no-answer case {label}."
                )
    results.append(
        report(10, "No-answer cases have no expected sources", no_answer_errors)
    )

    parity_errors: list[str] = []
    markdown_content, markdown_error = read_text(EVALUATION_MARKDOWN)
    if json_errors:
        parity_errors.append("Fix the evaluation JSON before comparing test IDs.")
    elif test_id_errors:
        parity_errors.append("Fix JSON test IDs before comparing evaluation files.")
    if markdown_error:
        parity_errors.append(markdown_error)
    if not parity_errors and markdown_content is not None:
        json_id_set = set(test_ids)
        markdown_id_set = set(TEST_ID_PATTERN.findall(markdown_content))
        missing_in_markdown = sorted(json_id_set - markdown_id_set)
        extra_in_markdown = sorted(markdown_id_set - json_id_set)
        if missing_in_markdown:
            parity_errors.append(
                "Add these JSON test IDs to the Markdown evaluation file: "
                + ", ".join(missing_in_markdown)
                + "."
            )
        if extra_in_markdown:
            parity_errors.append(
                "Remove or add matching JSON cases for these Markdown-only IDs: "
                + ", ".join(extra_in_markdown)
                + "."
            )
    results.append(
        report(11, "JSON and Markdown contain all test IDs", parity_errors)
    )

    suspicious_files, secret_check_errors = find_obvious_secret_files()
    for path in suspicious_files:
        secret_check_errors.append(
            f"Remove `{path}` from Git tracking, rotate its secrets, and use an example file."
        )
    results.append(report(12, "No obvious secret files are tracked", secret_check_errors))

    readme_errors: list[str] = []
    readme_content, readme_error = read_text(ROOT / "README.md")
    if readme_error:
        readme_errors.append(readme_error)
    elif readme_content is not None and FICTIONAL_PHRASE not in readme_content.lower():
        readme_errors.append(
            "Add the phrase `fictional demonstration SaaS product` to README.md."
        )
    results.append(
        report(13, "README labels TaskFlow as fictional", readme_errors)
    )

    passed = sum(results)
    total = len(results)
    print()
    if passed == total:
        print(f"RESULT: PASS ({passed}/{total} validation groups passed)")
        return 0

    print(f"RESULT: FAIL ({passed}/{total} validation groups passed)")
    print("Resolve the FAIL messages above, then rerun: python scripts/validate_phase_1.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
