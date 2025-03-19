from bv.packet cimport Packet
from bv.stream cimport Stream

from .frame cimport AudioFrame


cdef class AudioStream(Stream):
    cpdef encode(self, AudioFrame frame=?)
    cpdef decode(self, Packet packet=?)
