cimport libav as lib

from av.error cimport err_check
from av.packet cimport Packet
from av.subtitles.subtitle cimport SubtitleProxy, SubtitleSet


cdef class SubtitleCodecContext(CodecContext):
    cdef _send_packet_and_recv(self, Packet packet):
        if packet is None:
            raise RuntimeError("packet cannot be None")

        cdef SubtitleProxy proxy = SubtitleProxy()
        cdef int got_frame = 0

        err_check(
            lib.avcodec_decode_subtitle2(self.ptr, &proxy.struct, &got_frame, packet.ptr)
        )

        if got_frame:
            return SubtitleSet(proxy)
        return []

    cpdef decode2(self, Packet packet):
        """
        Returns SubtitleSet if you really need it.
        """
        if not self.codec.ptr:
            raise ValueError("cannot decode unknown codec")

        self.open(strict=False)

        cdef SubtitleProxy proxy = SubtitleProxy()
        cdef int got_frame = 0

        err_check(
            lib.avcodec_decode_subtitle2(self.ptr, &proxy.struct, &got_frame, packet.ptr)
        )

        if got_frame:
            return SubtitleSet(proxy)
        return None
