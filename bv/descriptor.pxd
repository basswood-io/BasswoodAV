cimport libav as lib


cdef class BaseOption:
    cdef const lib.AVOption *ptr

cdef class Option(BaseOption):
    cdef readonly tuple choices

cdef class OptionChoice(BaseOption):
    cdef readonly bint is_default


cdef class Descriptor:
    # These are present as:
    # - AVCodecContext.av_class (same as avcodec_get_class())
    # - AVFormatContext.av_class (same as avformat_get_class())
    # - AVFilterContext.av_class (same as avfilter_get_class())
    # - AVCodec.priv_class
    # - AVOutputFormat.priv_class
    # - AVInputFormat.priv_class
    # - AVFilter.priv_class

    cdef const lib.AVClass *ptr
    cdef tuple _options  # Option list cache.


cdef Descriptor wrap_avclass(const lib.AVClass*)
