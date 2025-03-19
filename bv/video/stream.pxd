from bv.packet cimport Packet
from bv.stream cimport Stream

from .frame cimport VideoFrame


cdef class VideoStream(Stream):
    cpdef encode(self, VideoFrame frame=?)
    cpdef decode(self, Packet packet=?)
