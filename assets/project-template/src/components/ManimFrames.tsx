import { Img, staticFile } from "remotion";
import { MANIM_FRAME_COUNTS } from "../manimManifest";

export const ManimFrames: React.FC<{
  scene: keyof typeof MANIM_FRAME_COUNTS;
  frame: number;
  from: number;
  duration: number;
  width: number;
  height: number;
}> = ({ scene, frame, from, duration, width, height }) => {
  const count = MANIM_FRAME_COUNTS[scene];
  const localFrame = frame - from;
  const index = Math.min(
    count - 1,
    Math.max(0, Math.floor((localFrame / duration) * count)),
  );
  const source = staticFile(
    `manim/${scene}/${String(index).padStart(5, "0")}.png`,
  );

  return <Img src={source} width={width} height={height} />;
};
