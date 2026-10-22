---
name: manim-remotion-explainer
description: "Build and render code-generated mathematics and science explainer videos with Remotion, React/SVG, and transparent Manim sequences. Use for formula-driven educational animations, waveform or spectrum explainers, and synchronized caption timelines that must produce a verified MP4."
metadata:
  short-description: "Manim + Remotion science video production"
---

# Manim + Remotion Explainer

Create the working project and render the video, not just a storyboard. Use Remotion for timeline control, typography, SVG diagrams, audio, subtitles, and scene composition. Use Manim for formulas and mathematical plots that benefit from TeX-quality typography and coordinate geometry.

Do not use this skill for live-action editing, talking-head footage, or image-only slide decks.

## Start

1. Inspect the brief, existing assets, target dimensions, duration, frame rate, audio policy, and Manim entrypoint.
2. Check the environment:

```powershell
pwsh -File scripts/check_environment.ps1 -ManimExe "D:\Manim\manim.cmd"
```

3. For a new video, create a project from the bundled working starter:

```powershell
pwsh -File scripts/create_project.ps1 -Destination "C:\path\to\new-video" -ManimExe "D:\Manim\manim.cmd" -Install -GenerateAssets
```

If a project already exists, reuse it and preserve unrelated changes.

## Production Rules

- Convert the timeline to exact frame numbers before implementing scenes.
- Use `useCurrentFrame()`, `interpolate()`, `spring()`, and `Sequence` for Remotion motion. Do not use CSS transitions.
- Render Manim with transparent PNG sequences, collect them under `public/manim/<scene>/`, and select the current frame in React. This avoids unreliable alpha-video paths.
- Keep scientific data in one shared source. A spectrum must be computed from the same signal shown in the time domain.
- Keep Chinese labels and captions in Remotion. Do not build a second subtitle system inside Manim.
- Generate or use only licensed audio. Never claim that missing audio is present.
- Verify representative frames visually and inspect the encoded MP4 with ffprobe and audio RMS before delivery.

## Supporting Resources

- Read [references/workflow.md](references/workflow.md) for end-to-end architecture, rendering, frame-sequence integration, and QA.
- Read [references/scientific-animation.md](references/scientific-animation.md) before making Fourier, signal-processing, or active-noise-control claims.
- Use `scripts/create_project.ps1` to copy the working starter.
- Use `scripts/verify_media.py` to verify stream metadata, audio, and representative frames.
- Starter project: `assets/project-template/`. Adapt it rather than treating its demo text as the requested content.

## Definition of Done

Deliver the MP4 path, source project, optional contact sheet, and a truthful verification summary with dimensions, duration, FPS, codecs, and unresolved limitations. An unrendered project is not a finished video.
