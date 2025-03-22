from enum import Enum
from typing import NoReturn, cast

class OptionType(Enum):
    FLAGS = cast(int, ...)
    INT = cast(int, ...)
    INT64 = cast(int, ...)
    DOUBLE = cast(int, ...)
    FLOAT = cast(int, ...)
    STRING = cast(int, ...)
    RATIONAL = cast(int, ...)
    BINARY = cast(int, ...)
    DICT = cast(int, ...)
    CONST = cast(int, ...)
    IMAGE_SIZE = cast(int, ...)
    PIXEL_FMT = cast(int, ...)
    SAMPLE_FMT = cast(int, ...)
    VIDEO_RATE = cast(int, ...)
    DURATION = cast(int, ...)
    COLOR = cast(int, ...)
    CHANNEL_LAYOUT = cast(int, ...)
    BOOL = cast(int, ...)

class BaseOption:
    name: str
    help: str
    flags: int
    is_encoding_param: bool
    is_decoding_param: bool
    is_audio_param: bool
    is_video_param: bool
    is_subtitle_param: bool
    is_export: bool
    is_readonly: bool
    is_filtering_param: bool

class Option(BaseOption):
    type: OptionType
    offset: int
    default: int
    min: int
    max: int

class OptionChoice(BaseOption):
    value: int

class Descriptor:
    name: str
    options: tuple[Option, ...]
