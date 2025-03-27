from collections.abc import Sequence

import cython

_cinit_bypass_sentinel = cython.declare(object, object())


# Cython doesn't let us inherit from the abstract Sequence, so we will subclass it later.
@cython.cclass
class _MotionVectors(SideData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vectors = {}
        self._len = self.ptr.size // cython.sizeof(lib.AVMotionVector)

    def __repr__(self):
        return f"<bv.sidedata.MotionVectors {self.ptr.size} bytes of {len(self)} vectors at 0x{cython.cast(cython.uint, self.ptr.data):0x}"

    def __getitem__(self, index: cython.int):
        try:
            return self._vectors[index]
        except KeyError:
            pass

        if index >= self._len:
            raise IndexError(index)

        vector = self._vectors[index] = MotionVector(
            _cinit_bypass_sentinel, self, index
        )
        return vector

    def __len__(self):
        return self._len

    def to_ndarray(self):
        import numpy as np

        return np.frombuffer(
            self,
            dtype=np.dtype(
                [
                    ("source", "int32"),
                    ("w", "uint8"),
                    ("h", "uint8"),
                    ("src_x", "int16"),
                    ("src_y", "int16"),
                    ("dst_x", "int16"),
                    ("dst_y", "int16"),
                    ("flags", "uint64"),
                    ("motion_x", "int32"),
                    ("motion_y", "int32"),
                    ("motion_scale", "uint16"),
                ],
                align=True,
            ),
        )


class MotionVectors(_MotionVectors, Sequence):
    pass


@cython.cclass
class MotionVector:
    def __init__(self, sentinel, parent: _MotionVectors, index: cython.int):
        if sentinel is not _cinit_bypass_sentinel:
            raise RuntimeError("cannot manually instatiate MotionVector")
        self.parent = parent
        base: cython.pointer[lib.AVMotionVector] = cython.cast(
            cython.pointer[lib.AVMotionVector], parent.ptr.data
        )
        self.ptr = base + index

    def __repr__(self):
        return f"<bv.sidedata.MotionVector {self.w}x{self.h} from {self.src_x},{self.src_y} to {self.dst_x},{self.dst_y}>"

    @property
    def source(self):
        return self.ptr.source

    @property
    def w(self):
        return self.ptr.w

    @property
    def h(self):
        return self.ptr.h

    @property
    def src_x(self):
        return self.ptr.src_x

    @property
    def src_y(self):
        return self.ptr.src_y

    @property
    def dst_x(self):
        return self.ptr.dst_x

    @property
    def dst_y(self):
        return self.ptr.dst_y

    @property
    def motion_x(self):
        return self.ptr.motion_x

    @property
    def motion_y(self):
        return self.ptr.motion_y

    @property
    def motion_scale(self):
        return self.ptr.motion_scale
