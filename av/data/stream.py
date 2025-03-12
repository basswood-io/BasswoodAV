import cython

from av.stream import Stream


class DataStream(Stream):
    def __repr__(self):
        return (
            f"<av.{self.__class__.__name__} #{self.index} data/"
            f"{self.name or '<nocodec>'} at 0x{id(self):x}>"
        )

    @property
    def name(self):
        desc: cython.pointer[cython.const[lib.AVCodecDescriptor]] = (
            lib.avcodec_descriptor_get(self.ptr.codecpar.codec_id)
        )
        if desc == cython.NULL:
            return None
        return desc.name
