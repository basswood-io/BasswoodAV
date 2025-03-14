from cpython.buffer cimport Py_buffer


cdef class Buffer:
    cdef size_t _buffer_size(self)
    cdef void* _buffer_ptr(self)
    cdef bint _buffer_writable(self)

cdef class ByteSource:
    cdef object owner
    cdef bint has_view
    cdef Py_buffer view
    cdef unsigned char *ptr
    cdef size_t length

cdef ByteSource bytesource(object, bint allow_none=*)
