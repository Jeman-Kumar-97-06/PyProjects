from dataclasses import dataclass
from vision_agents.core.processors import VideoProcessorPublisher
from vision_agents.core.events import Event

@dataclass
class ObjectDetectedEvent(Event):
    objects: list[str]
    frame_number: int

class DetectionProcessor(VideoProcessorPublisher):
    name = 'detection'

    def attach_agent(self, agent):
        self._events= agent.events
        self._events.register(ObjectDetectedEvent)

    async def _process_frame(self, frame):
        objects = self._detect(frame)
        await self._events.emit(ObjectDetectedEvent(
            objects = objects,
            frame_number = self.frame_count
        ))

