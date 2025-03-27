import cython
from cython.cimports import libav as lib
from cython.cimports.bv.filter.graph import Graph

_cinit_sentinel = cython.declare(object, object())


@cython.cclass
class FilterLink:
    def __cinit__(self, sentinel):
        if sentinel is not _cinit_sentinel:
            raise RuntimeError("cannot instantiate FilterLink")

    @property
    def input(self):
        if self._input:
            return self._input

        cctx: cython.pointer[lib.AVFilterContext] = self.ptr.src
        i: cython.uint
        for i in range(cctx.nb_outputs):
            if self.ptr == cctx.outputs[i]:
                break
        else:
            raise RuntimeError("could not find link in context")
        ctx = self.graph._context_by_ptr[cython.cast(cython.long, cctx)]
        self._input = ctx.outputs[i]
        return self._input

    @property
    def output(self):
        if self._output:
            return self._output
        cctx: cython.pointer[lib.AVFilterContext] = self.ptr.dst
        i: cython.uint
        for i in range(cctx.nb_inputs):
            if self.ptr == cctx.inputs[i]:
                break
        else:
            raise RuntimeError("could not find link in context")
        try:
            ctx = self.graph._context_by_ptr[cython.cast(cython.long, cctx)]
        except KeyError:
            raise RuntimeError(
                "could not find context in graph", (cctx.name, cctx.filter.name)
            )
        self._output = ctx.inputs[i]
        return self._output


@cython.cfunc
def wrap_filter_link(graph: Graph, ptr: cython.pointer[lib.AVFilterLink]) -> FilterLink:
    link: FilterLink = FilterLink(_cinit_sentinel)
    link.graph = graph
    link.ptr = ptr
    return link
