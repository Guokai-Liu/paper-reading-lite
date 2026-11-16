"""Build a source distribution from an explicit project file list; no upload."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "README.md", "SKILL.md", "PROMPT.md", "VERSION", "PUBLICATION.md", "LICENSE",
    "THIRD_PARTY_NOTICES.md", "requirements.txt", ".gitignore",
    "technical-checklist.md", "agents/openai.yaml",
    "references/writing-standard.md", "templates/report.md", "templates/evidence.md",
    "scripts/render_report.py", "scripts/render_math.cjs", "scripts/build_release.py",
    "assets/report.css", "vendor/katex/LICENSE",
    "vendor/katex/dist/katex.js", "vendor/katex/dist/katex.min.css",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text().strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.]+)?", version):
        parser.error("Unexpected version syntax.")
    paths = [ROOT / p for p in FILES]
    paths.extend(sorted((ROOT / "vendor/katex/dist/fonts").glob("*")))
    paths = sorted(p for p in paths if p.is_file())
    missing = [p for p in FILES if not (ROOT / p).is_file()]
    if missing:
        parser.error("Missing release inputs: " + ", ".join(missing))
    for path in paths:
        if path.is_symlink() or ROOT not in path.resolve().parents:
            parser.error("Release inputs must be ordinary files inside this project.")
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    archive = out / ("paper-reading-lite-" + version + ".zip")
    manifest = archive.with_suffix(".manifest.json")
    if archive.exists() or manifest.exists():
        parser.error("Release output already exists; choose a new directory or version.")
    entries = {}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in paths:
            relative = str(path.relative_to(ROOT)).replace("\\", "/")
            data = path.read_bytes()
            info = zipfile.ZipInfo("paper-reading-lite/" + relative,
                                   date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, data)
            entries[relative] = hashlib.sha256(data).hexdigest()
    result = {"project": "paper-reading-lite", "version": version,
              "artifact_type": "source-distribution",
              "project_license": "MIT",
              "archive": archive.name,
              "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "files": entries}
    manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"archive": str(archive), "manifest": str(manifest),
                      "files": len(entries), "bytes": archive.stat().st_size}))


if __name__ == "__main__":
    main()
