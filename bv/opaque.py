from uuid import uuid4

import cython
from cython.cimports import libav as lib
from cython.cimports.libc.stdint import uint8_t


@cython.cfunc
@cython.nogil
@cython.exceptval(check=False)
def key_free(opaque: cython.p_void, data: cython.p[uint8_t]) -> cython.void:
    name: cython.p_char = cython.cast(cython.p_char, data)
    with cython.gil:
        opaque_container.pop(name)


@cython.cclass
class OpaqueContainer:
    """A container that holds references to Python objects, indexed by uuid"""

    def __cinit__(self):
        self._by_name = {}

    @cython.cfunc
    def add(self, v: object) -> cython.pointer[lib.AVBufferRef]:
        uuid: bytes = uuid4().bytes
        ref: cython.p[lib.AVBufferRef] = lib.av_buffer_create(
            uuid, len(uuid), cython.address(key_free), cython.NULL, 0
        )
        self._by_name[uuid] = v
        return ref

    @cython.cfunc
    def get(self, name: bytes) -> object:
        return self._by_name.get(name)

    @cython.cfunc
    def pop(self, name: bytes) -> object:
        return self._by_name.pop(name)


opaque_container = cython.declare(OpaqueContainer, OpaqueContainer())
