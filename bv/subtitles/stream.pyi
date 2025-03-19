from bv.packet import Packet
from bv.stream import Stream
from bv.subtitles.subtitle import AssSubtitle, BitmapSubtitle, SubtitleSet

class SubtitleStream(Stream):
    def decode(
        self, packet: Packet | None = None
    ) -> list[AssSubtitle] | list[BitmapSubtitle]: ...
    def decode2(self, packet: Packet) -> SubtitleSet | None: ...
