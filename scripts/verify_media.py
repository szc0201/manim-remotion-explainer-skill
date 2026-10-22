from __future__ import annotations

import argparse
import array
import json
import math
import subprocess
import tempfile
import wave
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def parse_rate(value: str) -> float:
    if "/" not in value:
        return float(value)
    numerator, denominator = value.split("/", 1)
    return float(numerator) / float(denominator)


def probe(ffprobe: Path, video: Path) -> dict:
    result = run(
        [
            str(ffprobe),
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate",
            "-show_entries",
            "stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels",
            "-of",
            "json",
            str(video),
        ]
    )
    return json.loads(result.stdout)


def audio_metrics(ffmpeg: Path, video: Path) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        wav_path = Path(temp_dir) / "audio.wav"
        run(
            [
                str(ffmpeg),
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(video),
                "-map",
                "0:a:0",
                "-c:a",
                "pcm_s16le",
                str(wav_path),
            ]
        )
        with wave.open(str(wav_path), "rb") as source:
            frames = source.getnframes()
            sample_rate = source.getframerate()
            channels = source.getnchannels()
            samples = source.readframes(frames)

    values = array.array("h")
    values.frombytes(samples)
    rms = math.sqrt(sum(value * value for value in values) / len(values)) if values else 0
    return {
        "duration": frames / sample_rate,
        "sample_rate": sample_rate,
        "channels": channels,
        "rms": round(rms, 2),
        "peak": max((abs(value) for value in values), default=0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--ffprobe", required=True)
    parser.add_argument("--ffmpeg", required=True)
    parser.add_argument("--output-dir")
    parser.add_argument("--times", default="1,5,10")
    parser.add_argument("--expected-width", type=int)
    parser.add_argument("--expected-height", type=int)
    parser.add_argument("--expected-fps", type=float)
    parser.add_argument("--expected-duration", type=float)
    args = parser.parse_args()

    video = Path(args.video).resolve()
    ffprobe = Path(args.ffprobe).resolve()
    ffmpeg = Path(args.ffmpeg).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else video.parent
    frame_dir = output_dir / "verification-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)

    metadata = probe(ffprobe, video)
    streams = metadata.get("streams", [])
    video_stream = next((item for item in streams if item.get("codec_type") == "video"), None)
    audio_stream = next((item for item in streams if item.get("codec_type") == "audio"), None)
    if video_stream is None:
        raise SystemExit("No video stream")

    width = int(video_stream["width"])
    height = int(video_stream["height"])
    fps = parse_rate(video_stream["r_frame_rate"])
    duration = float(metadata["format"]["duration"])
    issues = []
    if args.expected_width and width != args.expected_width:
        issues.append(f"expected width {args.expected_width}, got {width}")
    if args.expected_height and height != args.expected_height:
        issues.append(f"expected height {args.expected_height}, got {height}")
    if args.expected_fps and abs(fps - args.expected_fps) > 0.01:
        issues.append(f"expected fps {args.expected_fps}, got {fps}")
    if args.expected_duration and abs(duration - args.expected_duration) > 0.5:
        issues.append(f"expected duration {args.expected_duration}, got {duration}")
    if audio_stream is None:
        issues.append("audio stream missing")

    frames = []
    for index, value in enumerate(args.times.split(","), start=1):
        target = frame_dir / f"{index:02d}_{float(value):05.2f}s.png"
        run(
            [
                str(ffmpeg),
                "-loglevel",
                "error",
                "-y",
                "-ss",
                value,
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-update",
                "1",
                str(target),
            ]
        )
        frames.append(str(target))

    audio = audio_metrics(ffmpeg, video) if audio_stream else None
    if audio and audio["rms"] <= 5:
        issues.append("audio appears silent")

    print(
        json.dumps(
            {
                "video": str(video),
                "width": width,
                "height": height,
                "fps": fps,
                "duration": duration,
                "video_codec": video_stream.get("codec_name"),
                "audio": audio,
                "frames": frames,
                "issues": issues,
                "ok": not issues,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
