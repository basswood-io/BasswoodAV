from bv.packet cimport Packet
from bv.stream cimport Stream


cdef class SubtitleStream(Stream):
    cpdef decode(self, Packet packet=?)
