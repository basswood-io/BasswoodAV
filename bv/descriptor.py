from enum import Enum

import cython
from cython.cimports import libav as lib
from cython.cimports.libc.stdint import uint64_t

_cinit_sentinel = object()


class OptionType(Enum):
    FLAGS = lib.AV_OPT_TYPE_FLAGS
    INT = lib.AV_OPT_TYPE_INT
    INT64 = lib.AV_OPT_TYPE_INT64
    DOUBLE = lib.AV_OPT_TYPE_DOUBLE
    FLOAT = lib.AV_OPT_TYPE_FLOAT
    STRING = lib.AV_OPT_TYPE_STRING
    RATIONAL = lib.AV_OPT_TYPE_RATIONAL
    BINARY = lib.AV_OPT_TYPE_BINARY
    DICT = lib.AV_OPT_TYPE_DICT
    UINT64 = lib.AV_OPT_TYPE_UINT64
    CONST = lib.AV_OPT_TYPE_CONST
    IMAGE_SIZE = lib.AV_OPT_TYPE_IMAGE_SIZE
    PIXEL_FMT = lib.AV_OPT_TYPE_PIXEL_FMT
    SAMPLE_FMT = lib.AV_OPT_TYPE_SAMPLE_FMT
    VIDEO_RATE = lib.AV_OPT_TYPE_VIDEO_RATE
    DURATION = lib.AV_OPT_TYPE_DURATION
    COLOR = lib.AV_OPT_TYPE_COLOR
    CHANNEL_LAYOUT = lib.AV_OPT_TYPE_CHLAYOUT
    BOOL = lib.AV_OPT_TYPE_BOOL


_INT_TYPES: tuple = (
    lib.AV_OPT_TYPE_FLAGS,
    lib.AV_OPT_TYPE_INT,
    lib.AV_OPT_TYPE_INT64,
    lib.AV_OPT_TYPE_PIXEL_FMT,
    lib.AV_OPT_TYPE_SAMPLE_FMT,
    lib.AV_OPT_TYPE_DURATION,
    lib.AV_OPT_TYPE_CHLAYOUT,
    lib.AV_OPT_TYPE_BOOL,
)


@cython.cfunc
def flag_in_bitfield(bitfield: uint64_t, flag: uint64_t):
    # Not every flag exists in every version of ffmpeg, so we define them to 0.
    if not flag:
        return None
    return bool(bitfield & flag)


@cython.cclass
class BaseOption:
    def __cinit__(self, sentinel):
        if sentinel is not _cinit_sentinel:
            raise RuntimeError(f"Cannot construct bv.{self.__class__.__name__}")

    @property
    def name(self):
        return self.ptr.name

    @property
    def help(self):
        return self.ptr.help if self.ptr.help != cython.NULL else ""

    @property
    def flags(self):
        return self.ptr.flags

    @property
    def is_encoding_param(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_ENCODING_PARAM)

    @property
    def is_decoding_param(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_DECODING_PARAM)

    @property
    def is_audio_param(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_AUDIO_PARAM)

    @property
    def is_video_param(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_VIDEO_PARAM)

    @property
    def is_subtitle_param(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_SUBTITLE_PARAM)

    @property
    def is_export(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_EXPORT)

    @property
    def is_readonly(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_READONLY)

    @property
    def is_filtering_param(self):
        return flag_in_bitfield(self.ptr.flags, lib.AV_OPT_FLAG_FILTERING_PARAM)


@cython.cclass
class Option(BaseOption):
    @property
    def type(self):
        return OptionType(self.ptr.type)

    @property
    def offset(self):
        """
        This can be used to find aliases of an option.
        Options in a particular descriptor with the same offset are aliases.
        """
        return self.ptr.offset

    @property
    def default(self):
        if self.ptr.type in _INT_TYPES:
            return self.ptr.default_val.i64

        if self.ptr.type in (
            lib.AV_OPT_TYPE_DOUBLE,
            lib.AV_OPT_TYPE_FLOAT,
            lib.AV_OPT_TYPE_RATIONAL,
        ):
            return self.ptr.default_val.dbl

        if self.ptr.type in (
            lib.AV_OPT_TYPE_STRING,
            lib.AV_OPT_TYPE_BINARY,
            lib.AV_OPT_TYPE_IMAGE_SIZE,
            lib.AV_OPT_TYPE_VIDEO_RATE,
            lib.AV_OPT_TYPE_COLOR,
        ):
            return (
                self.ptr.default_val.str
                if self.ptr.default_val.str != cython.NULL
                else ""
            )

    def _norm_range(self, value):
        if self.ptr.type in _INT_TYPES:
            return int(value)
        return value

    @property
    def min(self):
        return self._norm_range(self.ptr.min)

    @property
    def max(self):
        return self._norm_range(self.ptr.max)

    def __repr__(self):
        return (
            f"<bv.{self.__class__.__name__} {self.name}"
            f" ({self.type} at *0x{self.offset:x}) at 0x{id(self):x}>"
        )


@cython.cclass
class OptionChoice(BaseOption):
    """
    Represents AV_OPT_TYPE_CONST options which are essentially
    choices of non-const option with same unit.
    """

    @property
    def value(self):
        return self.ptr.default_val.i64

    def __repr__(self):
        return f"<bv.{self.__class__.__name__} {self.name} at 0x{id(self):x}>"


@cython.cfunc
def wrap_option(
    choices: tuple, ptr: cython.pointer[cython.const[lib.AVOption]]
) -> Option | None:
    if ptr == cython.NULL:
        return None

    obj: Option = Option(_cinit_sentinel)
    obj.ptr = ptr
    obj.choices = choices
    return obj


@cython.cfunc
def wrap_avclass(ptr: cython.pointer[cython.const[lib.AVClass]]) -> Descriptor:
    if ptr == cython.NULL:
        return None

    obj = Descriptor(_cinit_sentinel)
    obj.ptr = ptr
    return obj


@cython.cclass
class Descriptor:
    def __cinit__(self, sentinel):
        if sentinel is not _cinit_sentinel:
            raise RuntimeError("Cannot construct bv.Descriptor")

    @property
    def name(self):
        return self.ptr.class_name if self.ptr.class_name else None

    @property
    def options(self):
        ptr: cython.pointer[cython.const[lib.AVOption]] = self.ptr.option
        choice_ptr: cython.pointer[cython.const[lib.AVOption]]
        option: Option
        option_choice: OptionChoice

        if self._options is None:
            options: list = []
            ptr = self.ptr.option
            while ptr != cython.NULL and ptr.name != cython.NULL:
                if ptr.type == lib.AV_OPT_TYPE_CONST:
                    ptr += 1
                    continue
                choices = []

                if ptr.unit != cython.NULL:
                    choice_ptr = self.ptr.option
                    while choice_ptr != cython.NULL and choice_ptr.name != cython.NULL:
                        if (
                            choice_ptr.type != lib.AV_OPT_TYPE_CONST
                            or choice_ptr.unit != ptr.unit
                        ):
                            choice_ptr += 1
                            continue

                        option_choice = OptionChoice(_cinit_sentinel)
                        option_choice.ptr = choice_ptr
                        option_choice.is_default = (
                            choice_ptr.default_val.i64 == ptr.default_val.i64
                            or ptr.type == lib.AV_OPT_TYPE_FLAGS
                            and choice_ptr.default_val.i64 & ptr.default_val.i64
                        )
                        choices.append(option_choice)
                        choice_ptr += 1

                option = wrap_option(tuple(choices), ptr)
                options.append(option)
                ptr += 1
            self._options = tuple(options)
        return self._options

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} at 0x{id(self):x}>"
