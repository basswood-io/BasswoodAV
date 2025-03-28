import cython
from cython.cimports.bv.filter.link import wrap_filter_link

_cinit_sentinel = cython.declare(object, object())


@cython.cclass
class FilterPad:
    def __cinit__(self, sentinel):
        if sentinel is not _cinit_sentinel:
            raise RuntimeError("cannot construct FilterPad")

    def __repr__(self):
        _filter = self.filter.name
        _io = "inputs" if self.is_input else "outputs"

        return (
            f"<bv.FilterPad {_filter}.{_io}[{self.index}]: {self.name} ({self.type})>"
        )

    @property
    def is_output(self):
        return not self.is_input

    @property
    def name(self):
        return lib.avfilter_pad_get_name(self.base_ptr, self.index)

    @property
    def type(self):
        """
        The media type of this filter pad.

        Examples: `'audio'`, `'video'`, `'subtitle'`.

        :type: str
        """
        return lib.av_get_media_type_string(
            lib.avfilter_pad_get_type(self.base_ptr, self.index)
        )


@cython.cclass
class FilterContextPad(FilterPad):
    def __repr__(self):
        _filter = self.filter.name
        _io = "inputs" if self.is_input else "outputs"
        context = self.context.name

        return f"<bv.FilterContextPad {_filter}.{_io}[{self.index}] of {context}: {self.name} ({self.type})>"

    @property
    def link(self):
        if self._link:
            return self._link

        links: cython.pointer[cython.pointer[lib.AVFilterLink]] = (
            self.context.ptr.inputs if self.is_input else self.context.ptr.outputs
        )
        link: cython.pointer[lib.AVFilterLink] = links[self.index]
        if not link:
            return
        self._link = wrap_filter_link(self.context.graph, link)
        return self._link

    @property
    def linked(self):
        link: FilterLink = self.link
        if link:
            return link.input if self.is_input else link.output


@cython.cfunc
def alloc_filter_pads(
    filter: Filter,
    ptr: cython.pointer[cython.const[lib.AVFilterPad]],
    is_input: cython.bint,
    context: FilterContext | None = None,
) -> tuple:
    if not ptr:
        return ()

    pads: list = []

    # We need to be careful and check our bounds if we know what they are,
    # since the arrays on a AVFilterContext are not NULL terminated.
    i: cython.int = 0
    count: cython.int
    if context is None:
        count = lib.avfilter_filter_pad_count(filter.ptr, not is_input)
    else:
        count = context.ptr.nb_inputs if is_input else context.ptr.nb_outputs

    pad: FilterPad
    while i < count:
        pad = (
            FilterPad(_cinit_sentinel)
            if context is None
            else FilterContextPad(_cinit_sentinel)
        )
        pads.append(pad)
        pad.filter = filter
        pad.context = context
        pad.is_input = is_input
        pad.base_ptr = ptr
        pad.index = i
        i += 1

    return tuple(pads)
