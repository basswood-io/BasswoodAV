cdef int stash_exception(exc_info=*)
cpdef int err_check(int res, filename=*) except -1

cdef class EnumItem:
    cdef readonly str name
    cdef readonly int value