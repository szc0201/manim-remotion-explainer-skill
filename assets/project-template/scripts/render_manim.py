from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIM = Path(os.environ.get("MANIM_EXE", r"D:\Manim\manim.cmd"))
RAW_DIR = ROOT / "public" / "manim" / "raw"
OUTPUT_DIR = ROOT / "public" / "manim"
MANIFEST = ROOT / "src" / "manimManifest.ts"

SCENES = [
    ("formula_demo.py", "FormulaDemo", "formula"),
]


def main() -> None:
    if not MANIM.exists():
        raise SystemExit(f"Manim entrypoint not found: {MANIM}")

    requested = set(sys.argv[1:])
    selected = [scene for scene in SCENES if not requested or scene[2] in requested]
    if not selected:
        raise SystemExit(f"Unknown scene selector: {', '.join(requested)}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for script, scene_name, folder_name in selected:
        destination = OUTPUT_DIR / folder_name
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                str(MANIM),
                str(ROOT / "manim" / script),
                scene_name,
                "--format=png-sequence",
                "--transparent",
                "--fps=30",
                "--resolution=900,700",
                f"--media_dir={RAW_DIR}",
                "-v",
                "warning",
            ],
            cwd=ROOT,
            check=True,
        )

        candidates = sorted(RAW_DIR.glob(f"images/**/{scene_name}/*.png"))
        if not candidates:
            raise SystemExit(f"No PNG sequence found for {scene_name}")
        for index, source in enumerate(candidates):
            shutil.copy2(source, destination / f"{index:05d}.png")
        counts[folder_name] = len(candidates)
        print(f"{scene_name}: {len(candidates)} frames")

    previous = {
        "formula": 128,
    }
    previous.update(counts)
    manifest_lines = [
        "export const MANIM_FRAME_COUNTS = {",
        *[f"  {name}: {count}," for name, count in sorted(previous.items())],
        "} as const;",
        "",
    ]
    MANIFEST.write_text("\n".join(manifest_lines), encoding="utf-8")
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)


if __name__ == "__main__":
    main()
