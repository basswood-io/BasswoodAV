cimport libav as lib


cdef class AudioFormat:
    cdef lib.AVSampleFormat sample_fmt

cdef AudioFormat get_audio_format(lib.AVSampleFormat format)
