"""Portable package/activation/schema gate; semantic acceptance is recorded separately."""

import ast
import json
import re
from pathlib import Path

import yaml
from super_img2ppt.scene import SCHEMA

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/super-img2ppt"


def main():
    problems = []
    required = [
        "SKILL.md",
        "agents/openai.yaml",
        "skill-card.md",
        "evals/activation.json",
        "UPSTREAM.md",
        "requirements.lock",
        "LICENSE",
    ]
    for name in required:
        if not (SKILL / name).is_file():
            problems.append(f"Missing {name}")
    skill = (SKILL / "SKILL.md").read_text()
    metadata = yaml.safe_load(skill.split("---", 2)[1])
    if metadata["name"] != "super-img2ppt":
        problems.append("Skill ID mismatch")
    if not all(s in metadata["description"] for s in ["Use when", "Do not use"]):
        problems.append("Activation boundary missing")
    for target in re.findall(r"\]\(([^)]+)\)", skill):
        if not target.startswith("https://") and not (SKILL / target).is_file():
            problems.append(f"Broken skill reference: {target}")
    ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())
    if "$super-img2ppt" not in ui["interface"]["default_prompt"]:
        problems.append("Invocation prompt missing")
    if not 25 <= len(ui["interface"]["short_description"]) <= 64:
        problems.append("UI short description length outside 25–64")
    cases = json.loads((SKILL / "evals/activation.json").read_text())["activation_cases"]
    if (
        sum(c["should_activate"] for c in cases) < 2
        or sum(not c["should_activate"] for c in cases) < 2
    ):
        problems.append("Insufficient activation cases")
    if json.loads((SKILL / "references/scene.schema.json").read_text()) != SCHEMA:
        problems.append("Scene schema drift; regenerate with super-img2ppt schema")
    upstream = (SKILL / "UPSTREAM.md").read_text()
    if not re.search(r"\b[0-9a-f]{40}\b", upstream):
        problems.append("Upstream revision not pinned")
    for path in SKILL.rglob("*"):
        if path.is_symlink():
            problems.append(f"Skill bundle must be self contained: {path.relative_to(SKILL)}")
        if path.suffix in {".py", ".md", ".json", ".yaml", ".swift", ".toml"}:
            content = path.read_text()
            if any(
                c in content
                for c in [
                    "\u202a",
                    "\u202b",
                    "\u202d",
                    "\u202e",
                    "\u2066",
                    "\u2067",
                    "\u2068",
                    "\ufeff",
                ]
            ):
                problems.append(f"Hidden direction/format control: {path.relative_to(SKILL)}")
            if path.suffix == ".py":
                for node in ast.walk(ast.parse(content)):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id in {
                            "eval",
                            "exec",
                            "compile",
                        }:
                            problems.append(f"Dynamic execution: {path.name}:{node.lineno}")
                        if any(
                            k.arg == "shell"
                            and isinstance(k.value, ast.Constant)
                            and k.value.value is True
                            for k in node.keywords
                        ):
                            problems.append(f"Shell execution: {path.name}:{node.lineno}")
    print(
        json.dumps(
            {
                "status": "fail" if problems else "pass",
                "activation_cases": len(cases),
                "problems": problems,
                "scope": "Static package checks; semantic review and forward tests are separate evidence",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
