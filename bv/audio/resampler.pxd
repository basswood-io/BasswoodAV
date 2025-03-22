from bv.audio.format cimport AudioFormat
from bv.audio.frame cimport AudioFrame
from bv.audio.layout cimport AudioLayout
from bv.filter.graph cimport Graph


cdef class AudioResampler:
    cdef readonly bint is_passthrough
    cdef AudioFrame template

    # Destination descriptors
    cdef readonly AudioFormat format
    cdef readonly AudioLayout layout
    cdef readonly int rate
    cdef readonly unsigned int frame_size

    cdef Graph graph
    cpdef list resample(self, AudioFrame)
