import aiortc
import av
from typing import Optional
from vision_agents.core.processors import VideoProcessor
from vision_agents.core.utils.video_forwarder import VideoForwarder

class FrameLogger(VideoProcessor):
    name = 'frame_logger'
    def __init__(self,fps:int=5):
        self.fps = fps
        self.frame_count = 0
        self._forwarder: Optional[VideoForwarder] = None

    async def process_video(
            self,
            track: aiortc.VideoStreamTrack,
            participant_id:Optional[str],
            shared_forwarder: Optional[VideoForwarder] = None,
    ) -> None:
        self._forwarder = shared_forwarder
        self._forwarder.add_frame_handler(
            self._log_frame,
            fps=float(self.fps),
            name="frame_logger",
        )
    
    async def _log_frame(self, frame:av.VideoFrame):
        self.frame_count += 1
        print(f"Frame {self.frame_count} ({frame.width}x{frame.height})")

    async def stop_processing(self) -> None:
        if self._forwarder:
            await self._forwarder.remove_frame_handler(self._log_frame)
            self._forwarder = None
    
    async def close(self) -> None:
        await self.stop_processing()