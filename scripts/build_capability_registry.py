"""Generate the repository-local skill registry; never install it into an agent host."""

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    skills = ROOT / "skills"
    policy = json.loads((skills / "CAPABILITY_POLICY.json").read_text())
    entries = []
    for path in sorted(skills.glob("*/SKILL.md")):
        metadata = yaml.safe_load(path.read_text().split("---", 2)[1])
        skill_id = metadata["name"]
        relative = path.parent.relative_to(skills).as_posix()
        entries.append(
            {
                "id": skill_id,
                "path": relative,
                "description": metadata["description"],
                "canonical": policy["canonical_owners"].get(skill_id) == relative,
                "risk": policy["risk_classifications"][skill_id],
            }
        )
    content = (
        json.dumps({"schema_version": 1, "capabilities": entries}, ensure_ascii=False, indent=2)
        + "\n"
    )
    target = skills / "CAPABILITY_REGISTRY.json"
    if args.check:
        if not target.is_file() or target.read_text() != content:
            print(
                "Capability registry has drift; regenerate with scripts/build_capability_registry.py"
            )
            return 1
        print("Capability registry is current")
    else:
        target.write_text(content)
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
