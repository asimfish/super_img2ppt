"""Build a self-contained skill ZIP and checksum without changing host directories."""

import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    skill = ROOT / "skills/super-img2ppt"
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / "super-img2ppt.skill"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(skill.rglob("*")):
            if (
                source.is_file()
                and not any(p in {"__pycache__", ".venv", ".DS_Store"} for p in source.parts)
                and source.suffix != ".pyc"
            ):
                info = zipfile.ZipInfo(
                    f"super-img2ppt/{source.relative_to(skill).as_posix()}",
                    date_time=(2026, 9, 5, 0, 0, 0),
                )
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, source.read_bytes())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (dist / "SHA256SUMS").write_text(f"{digest}  {target.name}\n")
    print(f"{target}\nSHA256 {digest}")


if __name__ == "__main__":
    main()
