# Scientific Animation Guardrails

## Signals and Fourier Transforms

- State the synthetic signal explicitly, including frequency, amplitude, and phase.
- Use one shared signal definition for the time-domain plot and spectrum.
- For a one-second signal with integer frequencies, integer DFT bins align exactly with the components.
- Do not use random or hand-animated bar heights as a spectrum.
- Label synthetic examples. A Fourier transform analyzes frequency content; it does not by itself remove noise.

## Active Noise Control

The ideal cancellation model is:

```text
sin(ωt) + sin(ωt + π) = 0
```

Describe it as same-frequency, equal-amplitude, opposite-phase cancellation. Real ANC also involves microphones, delay, control algorithms, loudspeakers, position, and frequency-dependent performance. Do not claim a Fourier transform is the whole system.

## Visual Honesty

- Do not present a static equation image as an animated Manim result.
- Do not claim transparent video if the actual integration uses PNG sequences.
- Keep frequencies, labels, peaks, and formulas synchronized.
- Verify audio, subtitles, and rendered output independently.
