"""Package the explicitly indexed public gallery; retain earlier release archives unchanged."""

import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "examples/gallery"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    index = json.loads((GALLERY / "index.json").read_text())
    files = [GALLERY / "index.json", GALLERY / "NOTICE.md"]
    seen = set()
    for case in index["cases"]:
        name = case["id"]
        if not re.fullmatch(r"[a-z][a-z0-9_]*", name) or name in seen:
            raise ValueError(f"Invalid or duplicate gallery ID: {name}")
        seen.add(name)
        folder = GALLERY / name
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError(f"Missing or linked gallery directory: {name}")
        for required in ["source.png", "actual.png", "editable.pptx", "scene.resolved.json"]:
            if not (folder / required).is_file():
                raise ValueError(f"Incomplete gallery case: {name}/{required}")
        for path in sorted(folder.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Linked gallery artifact: {path}")
            if path.is_file():
                files.append(path)
    files.sort()
    sums = "".join(f"{digest(p)}  {p.relative_to(GALLERY).as_posix()}\n" for p in files)
    target = GALLERY / "paper_gallery.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(
                path.relative_to(GALLERY).as_posix(), date_time=(2026, 9, 12, 0, 0, 0)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
        info = zipfile.ZipInfo("SHA256SUMS", date_time=(2026, 9, 12, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info, sums)
    # Keep the frozen v0.3.3 three-case ZIP; the current checksum list covers both archives.
    archives = [target]
    legacy = GALLERY / "complex_figures.zip"
    if legacy.is_file():
        archives.append(legacy)
    (GALLERY / "SHA256SUMS").write_text(
        sums + "".join(f"{digest(p)}  {p.name}\n" for p in archives)
    )
    print(f"{len(seen)} complete cases; {len(files)} files; SHA256 {digest(target)}")


if __name__ == "__main__":
    main()
