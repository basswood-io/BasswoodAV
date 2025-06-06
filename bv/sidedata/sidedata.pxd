cimport libav as lib

from bv.buffer cimport Buffer
from bv.dictionary cimport _Dictionary, wrap_dictionary
from bv.frame cimport Frame


cdef class SideData(Buffer):
    cdef Frame frame
    cdef lib.AVFrameSideData *ptr
    cdef _Dictionary metadata

cdef SideData wrap_side_data(Frame frame, int index)

cdef int get_display_rotation(Frame frame)

cdef class _SideDataContainer:
    cdef Frame frame
    cdef list _by_index
    cdef dict _by_type
