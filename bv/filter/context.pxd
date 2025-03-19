cimport libav as lib

from bv.filter.filter cimport Filter
from bv.filter.graph cimport Graph


cdef class FilterContext:
    cdef lib.AVFilterContext *ptr
    cdef readonly object _graph
    cdef readonly Filter filter

    cdef object _inputs
    cdef object _outputs
    cdef bint inited


cdef FilterContext wrap_filter_context(Graph graph, Filter filter, lib.AVFilterContext *ptr)
