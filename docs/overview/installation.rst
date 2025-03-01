Installation
============

Binary wheels
-------------

Binary wheels are provided on PyPI for Linux, MacOS, and Windows linked against FFmpeg. The most straight-forward way to install PyAV is to run:

.. code-block:: bash

    pip install basswood-av


Building from the latest source
-------------------------------

::

    # Get PyAV from GitHub.
    git clone https://github.com/PyAV-Org/PyAV.git
    cd PyAV

    # Prep a virtualenv.
    source scripts/activate.sh

    # Optionally build FFmpeg.
    ./scripts/build-deps

    # Build PyAV.
    make


.. _build_on_windows:

On **Windows** you must indicate the location of your FFmpeg, e.g.::

    python setup.py build --ffmpeg-dir=C:\ffmpeg
