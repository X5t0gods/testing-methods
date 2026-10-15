"""Validate portfolio links, version metadata and curated evidence consistency."""

import ast
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def error(message):
    ERRORS.append(message)


def files_under_root():
    excluded = {".git", ".venv", "node_modules", "__pycache__", ".local", "artifacts"}
    return sorted(p for p in ROOT.rglob("*")
                  if p.is_file() and not excluded.intersection(p.relative_to(ROOT).parts))


def validate_text_files(files):
    signatures = [
        ("credential-like token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
        ("fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
        ("private user directory", re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+", re.I)),
        ("database URL with credentials", re.compile(r"(?:mysql|postgresql)(?:\+\w+)?://[^\s:@]+:[^\s@]+@", re.I)),
        ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ]
    forbidden_suffixes = {".log", ".sql", ".dump", ".db", ".pem", ".key"}
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix in forbidden_suffixes or path.name == ".env" or path.name.startswith(".env."):
            error(f"File outside public scope: {relative}")
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            error(f"Unexpected binary or non-UTF8 file: {relative}")
            continue
        for label, pattern in signatures:
            if pattern.search(source):
                error(f"Review {label}: {relative}")
        if path.suffix == ".py":
            try:
                ast.parse(source, filename=relative)
            except SyntaxError as exc:
                error(f"Python syntax error: {relative}:{exc.lineno}")
        if path.suffix == ".json":
            try:
                json.loads(source)
            except json.JSONDecodeError as exc:
                error(f"Invalid JSON: {relative}:{exc.lineno}")
        if path.suffix != ".md":
            continue
        if len(re.findall(r"^```", source, re.M)) % 2:
            error(f"Unbalanced code fence: {relative}")
        outside_code = re.sub(r"```.*?```", "", source, flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", outside_code):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            local = (path.parent / unquote(parsed.path)).resolve()
            if not local.is_relative_to(ROOT):
                error(f"Link leaves repository: {relative} -> {target}")
            elif not local.exists():
                error(f"Broken link: {relative} -> {target}")


def validate_metadata():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    publication = json.loads((ROOT / "publication.json").read_text(encoding="utf-8"))
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        error("VERSION must use major.minor.patch")
    if publication["version"] != version or publication["tag"] != f"v{version}":
        error("VERSION and publication.json disagree")
    if publication["repository"] != "X5t0gods/testing-methods":
        error("Canonical repository changed; confirm owner intent")
    if publication["visibility"] != "public":
        error("Publication visibility disagrees with current owner instruction")
    if not (ROOT / f"releases/v{version}.md").exists():
        error("Current release notes are missing")
    for name in ("README.md", "CHANGELOG.md"):
        if version not in (ROOT / name).read_text(encoding="utf-8"):
            error(f"Current version missing from {name}")


def validate_evidence_and_cards():
    evidence = json.loads((ROOT / "evidence/report-bi-audit.json").read_text(encoding="utf-8"))
    if evidence["private_project_rerun_during_publication"]:
        error("Historical project results must not be labeled as a publication rerun")
    coverage = evidence["coverage_files"]
    if set(coverage) != {"app/services/report_service.py", "app/repositories/report_repository.py"}:
        error("Unexpected coverage scope")
    for name, info in coverage.items():
        for covered, total in (("covered_statements", "statements"), ("covered_branches", "branches")):
            if not 0 <= info[covered] <= info[total]:
                error(f"Invalid coverage counts for {name}")
    provenance = json.loads((ROOT / "evidence/provenance.json").read_text(encoding="utf-8"))
    if len({source["id"] for source in provenance["sources"]}) != len(provenance["sources"]):
        error("Duplicate evidence source ids")
    for source in provenance["sources"]:
        if not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            error(f"Invalid evidence fingerprint: {source['id']}")
        if source["original_published"]:
            error("Raw private evidence is outside publication scope")
    cards = json.loads((ROOT / "checklists/index.json").read_text(encoding="utf-8"))
    expected = {f"B{i:02d}" for i in range(1, 16)} | {f"F{i:02d}" for i in range(1, 13)}
    if len(cards) != 27 or {card["id"] for card in cards} != expected:
        error("Expected 15 backend and 12 frontend module cards")
    for card in cards:
        if not (ROOT / card["path"]).is_file():
            error(f"Module card missing: {card['id']}")


def validate_regression_reports():
    for path in (ROOT / "evidence").glob("final-regression-*.json"):
        report = json.loads(path.read_text(encoding="utf-8"))
        checks = report["checks"]
        full = checks["backend_full"]
        if full["status"] == "initialization_aborted":
            if full["exit_code"] == 0 or full["coverage_total_generated"]:
                error(f"Aborted run has conflicting success metadata: {path.name}")
            for name in ("passed", "failed", "errors", "skipped", "coverage_total_percent"):
                if full[name] is not None:
                    error(f"Unavailable statistic must remain null: {path.name}:{name}")
        lint = checks["backend_lint"]
        if sum(lint["rules"].values()) != lint["diagnostics"]:
            error(f"Ruff diagnostic breakdown does not add up: {path.name}")
        mapping = checks["frontend_api_mock_mapping"]
        if mapping["missing"] != len(mapping["missing_mappings"]) or not 0 <= mapping["missing"] <= mapping["scanned"]:
            error(f"Mock gap counts disagree: {path.name}")
        if mapping["missing"] and mapping["status"] == "passed":
            error(f"Mock gaps cannot be described as passed: {path.name}")
        if report["business_tests_rerun_during_publication"]:
            error(f"Retained business results mislabeled as a publication rerun: {path.name}")


def main():
    files = files_under_root()
    validate_text_files(files)
    validate_metadata()
    validate_evidence_and_cards()
    validate_regression_reports()
    if ERRORS:
        print("\n".join(ERRORS))
        return 1
    print(f"PASS: {len(files)} files; links, metadata, evidence and 27 module cards checked.")
    print("This check does not rerun or independently audit the private business project.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
