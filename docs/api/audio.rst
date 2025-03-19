
Audio
=====

Audio Streams
-------------

.. automodule:: bv.audio.stream

    .. autoclass:: AudioStream
        :members:

Audio Context
-------------

.. automodule:: bv.audio.codeccontext

    .. autoclass:: AudioCodecContext
        :members:
        :exclude-members: channel_layout, channels

Audio Formats
-------------

.. automodule:: bv.audio.format

    .. autoclass:: AudioFormat
        :members:

Audio Layouts
-------------

.. automodule:: bv.audio.layout

    .. autoclass:: AudioLayout
        :members:

    .. autoclass:: AudioChannel
        :members:

Audio Frames
------------

.. automodule:: bv.audio.frame

    .. autoclass:: AudioFrame
        :members:
        :exclude-members: to_nd_array

Audio FIFOs
-----------

.. automodule:: bv.audio.fifo

    .. autoclass:: AudioFifo
        :members:
        :exclude-members: write, read, read_many

        .. automethod:: write
        .. automethod:: read
        .. automethod:: read_many

Audio Resamplers
----------------

.. automodule:: bv.audio.resampler

    .. autoclass:: AudioResampler
        :members:
        :exclude-members: resample

        .. automethod:: resample
