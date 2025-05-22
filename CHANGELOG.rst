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


v15.2.0
-------

Features:

- Enable x265.
- Package source builds.

Fixes:

- Make format_dtypes public again.
- Copy template flags if creating a new Codec object. Fixes muxing error.

v15.1.2
-------

Fixes:

- Expose the duration field for frames.
- Add GBRP, GBRAP, RGBA formats by :gh-user:`z-khan` in (:pr:`29`).
- Build binary wheels against libvpx 1.14.1 to fix CVE-2024-5197.
- Build binary wheels against libxml2 2.13.7 to fix CVE-2022-40303 CVE-2022-40304 CVE-2023-29469.

v15.1.1
-------

Fixes:

- Support using using AudioFormat and AudioLayout python classes, in ``AudioFrame.__init__()`` and ``AudioFrame.from_ndarray()``.

Misc:

- Linux: Build binary wheels for musl linux.
- MacOS: Binary wheels require MacOS 13 or greater.

v15.1.0
-------

Misc:

- Remove the ``opaque`` property and avoid using the ``uuid`` module.
- Remove ``stream_options`` parameter in ``InputContainer()``. ``options`` already passes to all streams.

v15.0.1
-------

Major:

- Use ``bv`` instead of ``av`` for imports so both projects can play nice.

v15.0.0
-------

Major:

- Turn ``av.ValueError`` into ``av.ArgumentError``. The latter is now not a subclass of ``ValueError``. This change better reflects how users should think about this exception.
- Make ``SubtitleStream.decode()`` return the list of subtitles directly, without the intermediate ``SubtitleSet``.
- Drop Support for Python 3.9.

Features:

- Add support for Python 3.13t.
- Add ``SubtitleCodecContext.decode2()`` which returns ``SubtitleSet | None``.