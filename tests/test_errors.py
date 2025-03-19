import errno
from traceback import format_exception_only

import pytest

import bv

from .common import is_windows


def test_stringify() -> None:
    for cls in (bv.FileNotFoundError, bv.DecoderNotFoundError):
        e = cls(1, "foo")
        assert f"{e}" == "[Errno 1] foo"
        assert f"{e!r}" == f"{cls.__name__}(1, 'foo')"
        assert (
            format_exception_only(cls, e)[-1]
            == f"bv.error.{cls.__name__}: [Errno 1] foo\n"
        )

    for cls in (bv.FileNotFoundError, bv.DecoderNotFoundError):
        e = cls(1, "foo", "bar.txt")
        assert f"{e}" == "[Errno 1] foo: 'bar.txt'"
        assert f"{e!r}" == f"{cls.__name__}(1, 'foo', 'bar.txt')"
        assert (
            format_exception_only(cls, e)[-1]
            == f"bv.error.{cls.__name__}: [Errno 1] foo: 'bar.txt'\n"
        )


def test_bases() -> None:
    assert issubclass(bv.FileNotFoundError, FileNotFoundError)
    assert issubclass(bv.FileNotFoundError, OSError)
    assert issubclass(bv.FileNotFoundError, bv.FFmpegError)


def test_filenotfound():
    """Catch using builtin class on Python 3.3"""
    try:
        bv.open("does not exist")
    except FileNotFoundError as e:
        assert e.errno == errno.ENOENT
        if is_windows:
            assert e.strerror in (
                "Error number -2 occurred",
                "No such file or directory",
            )
        else:
            assert e.strerror == "No such file or directory"
        assert e.filename == "does not exist"
    else:
        assert False, "No exception raised!"


def test_buffertoosmall() -> None:
    """Throw an exception from an enum."""

    BUFFER_TOO_SMALL = 1397118274
    try:
        bv.error.err_check(-BUFFER_TOO_SMALL)
    except bv.error.BufferTooSmallError as e:
        assert e.errno == BUFFER_TOO_SMALL
    else:
        assert False, "No exception raised!"


def test_argument_error() -> None:
    with pytest.raises(bv.ArgumentError) as e:
        with bv.open("out.gif", "w") as container:
            output_stream = container.add_stream("gif")

            frame = bv.VideoFrame(640, 640, "yuv420p")
            container.mux(output_stream.encode(frame))
        assert f"{e}" == """Invalid argument: 'avcodec_open2("gif", {})' returned 22"""
