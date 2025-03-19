# MUST import the core before anything else in order to initialize the underlying
# library that is being wrapped.
# Capture logging (by importing it).
from bv import logging
from bv._core import ffmpeg_version_info, library_versions, time_base

# For convenience, import all common attributes.
from bv.about import __version__
from bv.audio.codeccontext import AudioCodecContext
from bv.audio.fifo import AudioFifo
from bv.audio.format import AudioFormat
from bv.audio.frame import AudioFrame
from bv.audio.layout import AudioLayout
from bv.audio.resampler import AudioResampler
from bv.audio.stream import AudioStream
from bv.bitstream import BitStreamFilterContext, bitstream_filters_available
from bv.codec.codec import Codec, codecs_available
from bv.codec.context import CodecContext
from bv.codec.hwaccel import HWConfig
from bv.container import open
from bv.error import *  # noqa: F403; This is limited to exception types.
from bv.format import ContainerFormat, formats_available
from bv.packet import Packet
from bv.video.codeccontext import VideoCodecContext
from bv.video.format import VideoFormat
from bv.video.frame import VideoFrame
from bv.video.stream import VideoStream

__all__ = (
    "__version__",
    "time_base",
    "ffmpeg_version_info",
    "library_versions",
    "AudioCodecContext",
    "AudioFifo",
    "AudioFormat",
    "AudioFrame",
    "AudioLayout",
    "AudioResampler",
    "AudioStream",
    "BitStreamFilterContext",
    "bitstream_filters_available",
    "Codec",
    "codecs_available",
    "CodecContext",
    "open",
    "ContainerFormat",
    "formats_available",
    "Packet",
    "VideoCodecContext",
    "VideoFormat",
    "VideoFrame",
    "VideoStream",
)


def get_include() -> str:
    """
    Returns the path to the `include` folder to be used when building extensions to bv.
    """
    import os

    # Installed package
    include_path = os.path.join(os.path.dirname(__file__), "include")
    if os.path.exists(include_path):
        return include_path
    # Running from source directory
    return os.path.join(os.path.dirname(__file__), os.pardir, "include")
