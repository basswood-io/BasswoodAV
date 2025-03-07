Changelog
=========

We are operating with `semantic versioning <https://semver.org>`_.

..
    Please try to update this file in the commits that make the changes.

    To make merging/rebasing easier, we don't manually break lines in here
    when they are too long, so any particular change is just one line.

    To make tracking easier, please add either ``closes #123`` or ``fixes #123``
    to the first line of the commit message. There are more syntaxes at:
    <https://blog.github.com/2013-01-22-closing-issues-via-commit-messages/>.

    Note that they these tags will not actually close the issue/PR until they
    are merged into the "default" branch.


v15.0.0 (Unreleased)
--------------------

Major:

- Turn ``av.ValueError`` into ``av.ArgumentError``. The latter is now not a subclass of ``ValueError``. This change better reflects how PyAV users should think about this exception.

Features:

- Add support for Python free-threading builds.


v14.2.0
-------

Features:

- Add support for external flags in hwacccel by :gh-user:`materight` in (:pr:`1751`).
- Add Bayer pixel formats by :gh-user:`z-khan` in (:pr:`1755`).
- Add support for yuv422p10le pix_fmt by :gh-user:`WyattBlue` in (:pr:`1767`).
- Add ``supported_np_pix_fmts`` by :gh-user:`WyattBlue` in (:pr:`1766`).
- Add ``Codec.canonical_name`` by :gh-user:`WyattBlue`.

Misc:

- Drop support for MacOS 11 by :gh-user:`WyattBlue` in (:pr:`1764`).


v14.1.0
-------

Features:

- Add hardware decoding by :gh-user:`matthewlai` and :gh-user:`WyattBlue` in (:pr:`1685`).
- Add ``Stream.disposition`` and ``Disposition`` enum by :gh-user:`WyattBlue` in (:pr:`1720`).
- Add ``VideoFrame.rotation`` by :gh-user:`lgeiger` in (:pr:`1675`).
- Support grayf32le and gbrapf32le in numpy convertion by :gh-user:`robinechuca` in (:pr:`1712`).
- Support yuv[a]p16 formats in numpy convertion by :gh-user:`robinechuca` in (:pr:`1722`).

v14.0.1
-------

Fixes:

- Include header files in source distribution by :gh-user:`hmaarrfk` in (:pr:`1662`).
- Cleanup ``AVStream.side_data`` leftovers by :gh-user:`lgeiger` in (:pr:`1674`).
- Address :issue:`1663` by :gh-user:`WyattBlue`.
- Make ``mp3`` work with ``OutputContainer.add_stream_from_template()``.

v14.0.0
-------

Major:

- Drop FFmpeg 6.
- Drop support for MacOS <11 in our binary wheels.
- Deleted PyAV's custom Enum class in favor of Python's standard Enums.
- Remove ``CodecContext.close()``  and ``Stream.side_data`` because it's deprecated in ffmpeg.
- Remove ``AVError`` alias (use ``FFmpegError`` directly instead).
- Remove the `template` arg from ``OutputContainer.add_stream()``.

Features:

- Add ``OutputContainer.add_stream_from_template()`` by :gh-user:`WyattBlue` and :gh-user:`cdce8p`.
- Add ``OutputContainer.add_data_stream()`` by :gh-user:`WyattBlue`.
- Add ``filter.loudnorm.stats()`` function that returns the stats of loudnorm for 2-pass filtering by :gh-user:`WyattBlue`.
- Add ``qmin`` and ``qmax`` parameters to the ``VideoCodecContext`` by :gh-user:`davidplowman` in (:pr:`1618`).
- Allow the profile of a codec to be set as well as queried by :gh-user:`davidplowman` in (:pr:`1625`).

Fixes:

- Make ``VideoFrame.from_numpy_buffer()`` support buffers with padding by :gh-user:`davidplowman` in (:pr:`1635`).
- Correct ``Colorspace``'s lowercase enums.
- Updated ``sidedata.Type`` enum.
- Ensure streams in StreamContainer are released. Fixes :issue:`1599`.

