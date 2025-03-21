Video
=====

Video Streams
-------------

.. automodule:: bv.video.stream

    .. autoclass:: VideoStream
        :members:

Video Codecs
-------------

.. automodule:: bv.video.codeccontext

    .. autoclass:: VideoCodecContext
        :members:

Video Formats
-------------

.. automodule:: bv.video.format

    .. autoclass:: VideoFormat
        :members:

    .. autoclass:: VideoFormatComponent
        :members:

Video Frames
------------

.. automodule:: bv.video.frame

.. autoclass:: VideoFrame

    A single video frame.

    :param int width: The width of the frame.
    :param int height: The height of the frame.
    :param format: The format of the frame.
    :type  format: :class:`VideoFormat` or ``str``.

    >>> frame = VideoFrame(1920, 1080, 'rgb24')

Structural
~~~~~~~~~~

.. autoattribute:: VideoFrame.width
.. autoattribute:: VideoFrame.height
.. attribute:: VideoFrame.format

    The :class:`.VideoFormat` of the frame.

.. autoattribute:: VideoFrame.planes

Types
~~~~~

.. autoattribute:: VideoFrame.key_frame
.. autoattribute:: VideoFrame.interlaced_frame
.. autoattribute:: VideoFrame.pict_type

.. autoclass:: bv.video.frame.PictureType

    Wraps ``AVPictureType`` (``AV_PICTURE_TYPE_*``).

    .. enumtable:: bv.video.frame.PictureType


Conversions
~~~~~~~~~~~

.. automethod:: VideoFrame.reformat

.. automethod:: VideoFrame.to_rgb
.. automethod:: VideoFrame.save
.. automethod:: VideoFrame.to_image
.. automethod:: VideoFrame.to_ndarray

.. automethod:: VideoFrame.from_image
.. automethod:: VideoFrame.from_ndarray



Video Planes
-------------

.. automodule:: bv.video.plane

    .. autoclass:: VideoPlane
        :members:


Video Reformatters
------------------

.. automodule:: bv.video.reformatter

    .. autoclass:: VideoReformatter

        .. automethod:: reformat

Enums
~~~~~

.. autoclass:: bv.video.reformatter.Interpolation

    Wraps the ``SWS_*`` flags.

    .. enumtable:: bv.video.reformatter.Interpolation

.. autoclass:: bv.video.reformatter.Colorspace

    Wraps the ``SWS_CS_*`` flags. There is a bit of overlap in
    these names which comes from FFmpeg and backards compatibility.

    .. enumtable:: bv.video.reformatter.Colorspace

.. autoclass:: bv.video.reformatter.ColorRange

    Wraps the ``AVCOL*`` flags.

    .. enumtable:: bv.video.reformatter.ColorRange

