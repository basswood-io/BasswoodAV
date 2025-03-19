import errno
import logging
import threading

import bv.error
import bv.logging


def do_log(message: str) -> None:
    bv.logging.log(bv.logging.INFO, "test", message)


def test_adapt_level() -> None:
    assert bv.logging.adapt_level(bv.logging.ERROR) == logging.ERROR
    assert bv.logging.adapt_level(bv.logging.WARNING) == logging.WARNING
    assert (
        bv.logging.adapt_level((bv.logging.WARNING + bv.logging.ERROR) // 2)
        == logging.WARNING
    )


def test_threaded_captures() -> None:
    bv.logging.set_level(bv.logging.VERBOSE)

    with bv.logging.Capture(local=True) as logs:
        do_log("main")
        thread = threading.Thread(target=do_log, args=("thread",))
        thread.start()
        thread.join()

    assert (bv.logging.INFO, "test", "main") in logs
    bv.logging.set_level(None)


def test_global_captures() -> None:
    bv.logging.set_level(bv.logging.VERBOSE)

    with bv.logging.Capture(local=False) as logs:
        do_log("main")
        thread = threading.Thread(target=do_log, args=("thread",))
        thread.start()
        thread.join()

    assert (bv.logging.INFO, "test", "main") in logs
    assert (bv.logging.INFO, "test", "thread") in logs
    bv.logging.set_level(None)


def test_repeats() -> None:
    bv.logging.set_level(bv.logging.VERBOSE)

    with bv.logging.Capture() as logs:
        do_log("foo")
        do_log("foo")
        do_log("bar")
        do_log("bar")
        do_log("bar")
        do_log("baz")

    logs = [log for log in logs if log[1] == "test"]

    assert logs == [
        (bv.logging.INFO, "test", "foo"),
        (bv.logging.INFO, "test", "foo"),
        (bv.logging.INFO, "test", "bar"),
        (bv.logging.INFO, "test", "bar (repeated 2 more times)"),
        (bv.logging.INFO, "test", "baz"),
    ]

    bv.logging.set_level(None)


def test_error() -> None:
    bv.logging.set_level(bv.logging.VERBOSE)

    log = (bv.logging.ERROR, "test", "This is a test.")
    bv.logging.log(*log)
    try:
        bv.error.err_check(-errno.EPERM)
    except bv.error.PermissionError as e:
        assert e.log == log
    else:
        assert False

    bv.logging.set_level(None)
