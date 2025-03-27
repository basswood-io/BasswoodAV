import cython
from cython.cimports import libav as lib


def _flatten(input_):
    for x in input_:
        if isinstance(x, (tuple, list)):
            for y in _flatten(x):
                yield y
        else:
            yield x


@cython.cfunc
def _get_media_type_enum(type: str) -> lib.AVMediaType:
    if type == "video":
        return lib.AVMEDIA_TYPE_VIDEO
    elif type == "audio":
        return lib.AVMEDIA_TYPE_AUDIO
    elif type == "subtitle":
        return lib.AVMEDIA_TYPE_SUBTITLE
    elif type == "attachment":
        return lib.AVMEDIA_TYPE_ATTACHMENT
    elif type == "data":
        return lib.AVMEDIA_TYPE_DATA
    else:
        raise ValueError(f"Invalid stream type: {type}")


@cython.cclass
class StreamContainer:
    """

    A tuple-like container of :class:`Stream`.

    ::

        # There are a few ways to pulling out streams.
        first = container.streams[0]
        video = container.streams.video[0]
        audio = container.streams.get(audio=(0, 1))


    """

    def __cinit__(self):
        self._streams = []
        self.video = ()
        self.audio = ()
        self.subtitles = ()
        self.data = ()
        self.attachments = ()
        self.other = ()

    @cython.cfunc
    def add_stream(self, stream: Stream) -> cython.void:
        assert stream.ptr.index == len(self._streams)
        self._streams.append(stream)

        if stream.ptr.codecpar.codec_type == lib.AVMEDIA_TYPE_VIDEO:
            self.video = self.video + (stream,)
        elif stream.ptr.codecpar.codec_type == lib.AVMEDIA_TYPE_AUDIO:
            self.audio = self.audio + (stream,)
        elif stream.ptr.codecpar.codec_type == lib.AVMEDIA_TYPE_SUBTITLE:
            self.subtitles = self.subtitles + (stream,)
        elif stream.ptr.codecpar.codec_type == lib.AVMEDIA_TYPE_ATTACHMENT:
            self.attachments = self.attachments + (stream,)
        elif stream.ptr.codecpar.codec_type == lib.AVMEDIA_TYPE_DATA:
            self.data = self.data + (stream,)
        else:
            self.other = self.other + (stream,)

    # Basic tuple interface.
    def __len__(self):
        return len(self._streams)

    def __iter__(self):
        return iter(self._streams)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get(index)[0]
        return self.get(index)

    def get(self, *args, **kwargs):
        """get(streams=None, video=None, audio=None, subtitles=None, data=None)

        Get a selection of :class:`.Stream` as a ``list``.

        Positional arguments may be ``int`` (which is an index into the streams),
        or ``list`` or ``tuple`` of those::

            # Get the first channel.
            streams.get(0)

            # Get the first two audio channels.
            streams.get(audio=(0, 1))

        Keyword arguments (or dicts as positional arguments) as interpreted
        as ``(stream_type, index_value_or_set)`` pairs::

            # Get the first video channel.
            streams.get(video=0)
            # or
            streams.get({'video': 0})

        :class:`.Stream` objects are passed through untouched.

        If nothing is selected, then all streams are returned.
        """
        selection: list = []

        for x in _flatten((args, kwargs)):
            if x is None:
                pass
            elif isinstance(x, Stream):
                selection.append(x)
            elif isinstance(x, int):
                selection.append(self._streams[x])
            elif isinstance(x, dict):
                for type_, indices in x.items():
                    if (
                        type_ == "streams"
                    ):  # For compatibility with the pseudo signature
                        streams = self._streams
                    else:
                        streams = getattr(self, type_)
                    if not isinstance(indices, (tuple, list)):
                        indices = [indices]
                    for i in indices:
                        selection.append(streams[i])
            else:
                raise TypeError("Argument must be Stream or int.", type(x))

        return selection or self._streams[:]

    @cython.cfunc
    @cython.exceptval(check=False)
    def _get_best_stream_index(
        self, container: Container, type_enum: lib.AVMediaType, related: Stream
    ) -> cython.int:
        stream_index: cython.int

        if related is None:
            stream_index = lib.av_find_best_stream(
                container.ptr, type_enum, -1, -1, cython.NULL, 0
            )
        else:
            stream_index = lib.av_find_best_stream(
                container.ptr, type_enum, -1, related.ptr.index, cython.NULL, 0
            )

        return stream_index

    def best(self, type: str, /, related: Stream | None = None):
        """best(type: Literal["video", "audio", "subtitle", "attachment", "data"], /, related: Stream | None)
        Finds the "best" stream in the file. Wraps :ffmpeg:`av_find_best_stream`. Example::

            stream = container.streams.best("video")

        :param type: The type of stream to find
        :param related: A related stream to use as a reference (optional)
        :return: The best stream of the specified type
        :rtype: Stream | None
        """
        if len(self._streams) == 0:
            return None

        stream_index: cython.int = self._get_best_stream_index(
            self._streams[0].container, _get_media_type_enum(type), related
        )
        if stream_index < 0:
            return None

        return self._streams[stream_index]
