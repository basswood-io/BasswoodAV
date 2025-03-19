from typing import Literal

from bv.codec.context import CodecContext
from bv.packet import Packet
from bv.subtitles.subtitle import SubtitleSet

class SubtitleCodecContext(CodecContext):
    type: Literal["subtitle"]
    def decode2(self, packet: Packet) -> SubtitleSet | None: ...
