import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { ManimFrames } from "./components/ManimFrames";

const colors = {
  ink: "#030a13",
  line: "#24475b",
  white: "#f4f8fb",
  muted: "#91aabd",
  cyan: "#53dcff",
  orange: "#ff9b51",
};

const fontFamily =
  '"Noto Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif';

export const Demo: React.FC = () => {
  const frame = useCurrentFrame();
  const titleReveal = interpolate(frame, [8, 32], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const visualOpacity = interpolate(frame, [18, 45], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const captionOpacity = interpolate(frame, [40, 62], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.ink,
        color: colors.white,
        fontFamily,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(155deg, #030a13 0%, #051725 55%, #071a28 100%)",
        }}
      />
      <svg width="1080" height="1920" style={{ position: "absolute" }}>
        <defs>
          <pattern id="grid" width="90" height="90" patternUnits="userSpaceOnUse">
            <path
              d="M 90 0 L 0 0 0 90"
              fill="none"
              stroke={colors.line}
              strokeWidth="1"
              opacity="0.38"
            />
          </pattern>
        </defs>
        <rect width="1080" height="1920" fill="url(#grid)" />
      </svg>

      <div
        style={{
          position: "absolute",
          top: 118,
          left: 100,
          color: colors.cyan,
          fontSize: 24,
          fontWeight: 700,
          letterSpacing: 3,
        }}
      >
        MANIM + REMOTION / STARTER
      </div>
      <div
        style={{
          position: "absolute",
          top: 205,
          left: 100,
          width: 880,
          fontSize: 86,
          fontWeight: 900,
          lineHeight: 1.28,
          clipPath: `inset(0 ${(1 - titleReveal) * 100}% 0 0)`,
          translate: `0 ${(1 - titleReveal) * 24}px`,
        }}
      >
        看见公式，
        <br />
        <span style={{ color: colors.cyan }}>也看见声音。</span>
      </div>

      <div
        style={{
          position: "absolute",
          top: 520,
          left: 40,
          opacity: visualOpacity,
        }}
      >
        <ManimFrames
          scene="formula"
          frame={frame}
          from={20}
          duration={210}
          width={1000}
          height={760}
        />
      </div>

      <div
        style={{
          position: "absolute",
          top: 1370,
          left: 100,
          width: 880,
          padding: "26px 30px",
          borderTop: `1px solid ${colors.line}`,
          borderBottom: `1px solid ${colors.line}`,
          backgroundColor: "rgba(3,10,19,0.72)",
          opacity: captionOpacity,
        }}
      >
        <div style={{ color: colors.muted, fontSize: 22, letterSpacing: 2 }}>
          SAME SIGNAL, TWO VIEWS
        </div>
        <div style={{ marginTop: 12, fontSize: 40, fontWeight: 700 }}>
          时域看变化，<span style={{ color: colors.orange }}>频域看成分</span>
        </div>
      </div>

      <Audio src={staticFile("audio/bgm.wav")} volume={0.18} />
    </AbsoluteFill>
  );
};
