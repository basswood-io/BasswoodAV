from bv.codec.context cimport CodecContext
from bv.packet cimport Packet


cdef class SubtitleCodecContext(CodecContext):
    cpdef decode2(self, Packet packet)
