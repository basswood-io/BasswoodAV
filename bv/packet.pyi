from fractions import Fraction

from bv.audio.frame import AudioFrame
from bv.subtitles.subtitle import AssSubtitle, BitmapSubtitle
from bv.video.frame import VideoFrame

from .buffer import Buffer
from .stream import Stream

class Packet(Buffer):
    stream: Stream
    stream_index: int
    time_base: Fraction
    pts: int | None
    dts: int | None
    pos: int | None
    size: int
    duration: int | None
    opaque: object
    is_keyframe: bool
    is_corrupt: bool
    is_discard: bool
    is_trusted: bool
    is_disposable: bool

    def __init__(self, input: int | bytes | None = None) -> None: ...
    def decode(
        self,
    ) -> (
        list[VideoFrame] | list[AudioFrame] | list[AssSubtitle] | list[BitmapSubtitle]
    ): ...
