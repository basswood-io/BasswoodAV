import cython
import cython as cy
from cython.cimports import libav as lib

_cinit_sentinel = cython.declare(object, object())


def wrap_avclass(ptr):
    if ptr == cython.NULL:
        return None

    obj = cython.declare(Descriptor, Descriptor(_cinit_sentinel))
    obj.ptr = ptr
    return obj


@cython.cclass
class Descriptor:
    def __cinit__(self, sentinel):
        if sentinel is not _cinit_sentinel:
            raise RuntimeError("Cannot construct bv.Descriptor")

    @property
    def name(self):
        return self.ptr.class_name if self.ptr.class_name else None

    @property
    def options(self):
        ptr = cython.declare(cy.pointer[cy.const[lib.AVOption]], self.ptr.option)
        choice_ptr = cython.declare(cy.pointer[cy.const[lib.AVOption]])
        option = cython.declare(Option)
        option_choice = cython.declare(OptionChoice)
        choice_is_default = cython.declare(cython.bint)

        if self._options is None:
            options = []
            ptr = self.ptr.option
            while ptr != cython.NULL and ptr.name != cython.NULL:
                if ptr.type == lib.AV_OPT_TYPE_CONST:
                    ptr += 1
                    continue
                choices = []

                if ptr.unit != cython.NULL:
                    choice_ptr = self.ptr.option
                    while choice_ptr != cython.NULL and choice_ptr.name != cython.NULL:
                        if (
                            choice_ptr.type != lib.AV_OPT_TYPE_CONST
                            or choice_ptr.unit != ptr.unit
                        ):
                            choice_ptr += 1
                            continue
                        choice_is_default = (
                            choice_ptr.default_val.i64 == ptr.default_val.i64
                            or ptr.type == lib.AV_OPT_TYPE_FLAGS
                            and choice_ptr.default_val.i64 & ptr.default_val.i64
                        )
                        option_choice = wrap_option_choice(
                            choice_ptr, choice_is_default
                        )
                        choices.append(option_choice)
                        choice_ptr += 1

                option = wrap_option(tuple(choices), ptr)
                options.append(option)
                ptr += 1
            self._options = tuple(options)
        return self._options

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} at 0x{id(self):x}>"
