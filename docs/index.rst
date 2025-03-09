**BasswoodAV** Documentation
======================

**BasswoodAV** provides Pythonic bindings for FFmpeg_. We aim to provide all of the power and control of the underlying library, but manage the gritty details as much as possible.

BasswoodAV provides direct and precise access to your media via containers, streams, packets, codecs, and frames. It exposes a few transformations of that data, and helps you get your data to/from other packages, such as Numpy.

This power does come with some responsibility as working with media is complicated and BasswoodAV can't abstract it away or make all the best decisions for you. But where you can't work without it, BasswoodAV is a critical tool.

Currently we provide:

- ``libavformat``:
  :class:`containers <.Container>`,
  audio/video/subtitle :class:`streams <.Stream>`,
  :class:`packets <.Packet>`;

- ``libavdevice`` (by specifying a format to containers);

- ``libavcodec``:
  :class:`.Codec`,
  :class:`.CodecContext`,
  :class:`.BitStreamFilterContext`,
  audio/video :class:`frames <.Frame>`,
  :class:`data planes <.Plane>`,
  :class:`subtitles <.Subtitle>`;

- ``libavfilter``:
  :class:`.Filter`,
  :class:`.Graph`;

- ``libswscale``:
  :class:`.VideoReformatter`;

- ``libswresample``:
  :class:`.AudioResampler`;

- and a few more utilities.

.. _FFmpeg: https://ffmpeg.org/


Basic Demo
----------

.. testsetup::

    path_to_video = common.fate_png() # We don't need a full QT here.


.. testcode::

    import av

    av.logging.set_level(av.logging.VERBOSE)
    container = av.open(path_to_video)

    for index, frame in enumerate(container.decode(video=0)):
        frame.save(f"frame-{index:04d}.jpg")


Overview
--------

.. toctree::
    :glob:
    :maxdepth: 2

    overview/*


Cookbook
--------

.. toctree::
    :glob:
    :maxdepth: 2

    cookbook/*


Reference
---------

.. toctree::
    :glob:
    :maxdepth: 2

    api/*


Development
-----------

.. toctree::
    :glob:
    :maxdepth: 1

    development/*


Indices and Tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
