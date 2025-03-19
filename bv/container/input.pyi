from typing import Any, Iterator, overload

from bv.audio.frame import AudioFrame
from bv.audio.stream import AudioStream
from bv.packet import Packet
from bv.stream import Stream
from bv.subtitles.stream import SubtitleStream
from bv.subtitles.subtitle import AssSubtitle, BitmapSubtitle
from bv.video.frame import VideoFrame
from bv.video.stream import VideoStream

from .core import Container

class InputContainer(Container):
    start_time: int
    duration: int | None
    bit_rate: int
    size: int

    def __enter__(self) -> InputContainer: ...
    def close(self) -> None: ...
    def demux(self, *args: Any, **kwargs: Any) -> Iterator[Packet]: ...
    @overload
    def decode(self, video: int) -> Iterator[VideoFrame]: ...
    @overload
    def decode(self, audio: int) -> Iterator[AudioFrame]: ...
    @overload
    def decode(
        self, subtitles: int
    ) -> Iterator[AssSubtitle] | Iterator[BitmapSubtitle]: ...
    @overload
    def decode(self, *args: VideoStream) -> Iterator[VideoFrame]: ...
    @overload
    def decode(self, *args: AudioStream) -> Iterator[AudioFrame]: ...
    @overload
    def decode(
        self, *args: SubtitleStream
    ) -> Iterator[AssSubtitle] | Iterator[BitmapSubtitle]: ...
    @overload
    def decode(
        self, *args: Any, **kwargs: Any
    ) -> (
        Iterator[VideoFrame]
        | Iterator[AudioFrame]
        | Iterator[AssSubtitle]
        | Iterator[BitmapSubtitle]
    ): ...
    def seek(
        self,
        offset: int,
        *,
        backward: bool = True,
        any_frame: bool = False,
        stream: Stream | VideoStream | AudioStream | None = None,
        unsupported_frame_offset: bool = False,
        unsupported_byte_offset: bool = False,
    ) -> None: ...
    def flush_buffers(self) -> None: ...
