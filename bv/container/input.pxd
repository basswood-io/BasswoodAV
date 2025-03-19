cimport libav as lib

from bv.container.core cimport Container
from bv.stream cimport Stream


cdef class InputContainer(Container):
    cdef flush_buffers(self)
