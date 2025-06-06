cimport libav as lib


cdef class Codec:
    cdef const lib.AVCodec *ptr
    cdef const lib.AVCodecDescriptor *desc
    cdef readonly bint is_encoder
    cdef tuple _hardware_configs

    cdef _init(self, name=?)


cdef Codec wrap_codec(const lib.AVCodec *ptr)
