import { Composition } from "remotion";
import { Demo } from "./Demo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ManimStarter"
      component={Demo}
      durationInFrames={240}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
