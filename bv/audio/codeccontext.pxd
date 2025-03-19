from bv.audio.frame cimport AudioFrame
from bv.audio.resampler cimport AudioResampler
from bv.codec.context cimport CodecContext


cdef class AudioCodecContext(CodecContext):
    # Hold onto the frames that we will decode until we have a full one.
    cdef AudioFrame next_frame
    # For encoding.
    cdef AudioResampler resampler
