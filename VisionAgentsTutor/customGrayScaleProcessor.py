import aiortc
import av
import cv2
from typing import Optional
from vision_agents.core.processors import VideoProcessorPublisher
from vision_agents.core.utils.video_track import QueuedVideoTrack
from vision_agents.core.utils.video_forwarder import VideoForwarder

class GrayscaleProcessor(VideoProcessorPublisher):
    name = "grayscale"

    def __init__(self, fps: int = 30):
        self.fps = fps
        self._forwarder: Optional[VideoForwarder] = None
        self._video_track = QueuedVideoTrack()

    async def process_video(
        self,
        track: aiortc.VideoStreamTrack,
        participant_id: Optional[str],
        shared_forwarder: Optional[VideoForwarder] = None,
    ) -> None:
        # Remove existing handler if switching tracks
        if self._forwarder:
            await self._forwarder.remove_frame_handler(self._process_frame)

        self._forwarder = shared_forwarder
        self._forwarder.add_frame_handler(
            self._process_frame,
            fps=float(self.fps),
            name="grayscale",
        )

    async def _process_frame(self, frame: av.VideoFrame):
        img = frame.to_ndarray(format="rgb24")
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        new_frame = av.VideoFrame.from_ndarray(rgb, format="rgb24")
        await self._video_track.add_frame(new_frame)

    def publish_video_track(self) -> aiortc.VideoStreamTrack:
        return self._video_track

    async def stop_processing(self) -> None:
        if self._forwarder:
            await self._forwarder.remove_frame_handler(self._process_frame)
            self._forwarder = None

    async def close(self) -> None:
        await self.stop_processing()
        self._video_track.stop()