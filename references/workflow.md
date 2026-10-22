# Production Workflow

## Timeline

Extract exact frame counts from the requested duration and FPS before building scenes. Keep a single timeline manifest for scene boundaries. When a transition overlaps two scenes, account for that overlap in the final composition duration.

Use frame-driven animation only. Captions need explicit entrance, hold, and exit intervals; adjacent full sentences should not remain legible at the same time.

## Architecture

Keep these responsibilities separate:

- Remotion: global timeline, typography, captions, SVG objects, background, audio, and transitions.
- Manim: equations, axes, sine waves, spectra with mathematical geometry, and derivation animations.
- Shared data: signal frequencies, amplitudes, phases, and derived spectrum values.

The starter layout is:

```text
src/
  Demo.tsx
  Root.tsx
  components/ManimFrames.tsx
manim/formula_demo.py
scripts/generate_audio.py
scripts/render_manim.py
public/manim/formula/
public/audio/
output/
```

## Manim PNG Sequences

Set `MANIM_EXE` if the launcher is not `D:\Manim\manim.cmd`. Render with:

```powershell
npm run manim
```

The starter script uses transparent PNG output, collects numbered frames, and writes `src/manimManifest.ts` with the actual frame count. Re-render only one scene when patching:

```powershell
python scripts/render_manim.py formula
```

Select frames from Remotion with a single manifest constant. Never assume a fixed Manim frame count after editing animation timing.

## Scientific Data

Define the signal once in TypeScript and use that function for both plots and DFT calculations. Keep frequency, amplitude, and phase explicit. Normalize bars for display only if peak locations remain exact.

Label synthetic examples as synthetic. Do not describe a demonstration DFT as a real hardware measurement.

## Audio

When no licensed music is available, generate a deterministic low-volume track with `scripts/generate_audio.py`. Verify the final container has a non-silent audio stream. Do not add voiceover unless requested.

## Rendering and QA

Run:

```powershell
npm run lint
npm run render
python path\to\skill\scripts\verify_media.py --video output\demo.mp4 --ffprobe node_modules\@remotion\compositor-win32-x64-msvc\ffprobe.exe --ffmpeg node_modules\@remotion\compositor-win32-x64-msvc\ffmpeg.exe
```

Inspect the contact sheet at the opening, formula reveal, transition, and ending. Re-render after correcting clipping, overlaps, missing frames, or transition black frames.

On Windows paths that confuse the Remotion parent-directory scan, use `Config.setRspack(false)` in `remotion.config.ts`. If Chromium or the config compiler is blocked by the sandbox, retry the render with approval outside the sandbox.

## Cleanup

Preserve source, configs, lockfile, Manim sources, final frame sequences, audio, README, and final deliverables.

Safe to delete after verification:

- `node_modules/`
- Manim raw intermediate output
- `__pycache__/`
- temporary review stills and extracted audio
