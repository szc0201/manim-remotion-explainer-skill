from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "public" / "audio" / "bgm.wav"
SAMPLE_RATE = 22050
DURATION = 8.0


def sample(t: float) -> float:
    fade = min(1.0, t / 1.0, max(0.0, DURATION - t) / 1.2)
    chord = (
        math.sin(2 * math.pi * 110 * t) * 0.022
        + math.sin(2 * math.pi * 164.81 * t + 0.7) * 0.016
        + math.sin(2 * math.pi * 220 * t + 1.4) * 0.012
    )
    pulse = 0.8 + 0.2 * math.sin(2 * math.pi * 0.125 * t)
    return chord * fade * pulse


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUTPUT), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)
        data = bytearray()
        for index in range(int(DURATION * SAMPLE_RATE)):
            value = max(-1.0, min(1.0, sample(index / SAMPLE_RATE)))
            data.extend(struct.pack("<h", int(value * 32767)))
        output.writeframes(data)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
