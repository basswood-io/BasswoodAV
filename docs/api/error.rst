Errors
======

.. currentmodule:: bv.error

.. _error_behaviour:

General Behavior
-----------------

When BasswoodAV encounters an FFmpeg error, it raises an appropriate exception.

FFmpeg has a couple dozen of its own error types which we represent via
:ref:`error_classes`.

FFmpeg will also return more typical errors such as ``ENOENT`` or ``EAGAIN``,
which we do our best to translate to extensions of the builtin exceptions
as defined by
`PEP 3151 <https://www.python.org/dev/peps/pep-3151/#new-exception-classes>`_.


.. _error_classes:

Error Exception Classes
-----------------------

BasswoodAV raises the typical builtin exceptions within its own codebase, but things
get a little more complex when it comes to translating FFmpeg errors.

There are two competing ideas that have influenced the final design:

1. We want every exception that originates within FFmpeg to inherit from a common
   :class:`.FFmpegError` exception;

2. We want to use the builtin exceptions whenever possible.

As such, BasswoodAV effectively shadows as much of the builtin exception hierarchy as
it requires, extending from both the builtins and from :class:`FFmpegError`.

Therefore, an argument error within FFmpeg will raise a ``bv.error.ValueError``, which
can be caught via either :class:`FFmpegError` or ``ValueError``. All of these
exceptions expose the typical ``errno`` and ``strerror`` attributes, as well as some 
BasswoodAV extensions such as :attr:`FFmpegError.log`.

All of these exceptions are available on the top-level ``av`` package, e.g.::

    try:
        do_something()
    except bv.FilterNotFoundError:
        handle_error()


.. autoclass:: bv.FFmpegError

