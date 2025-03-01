PyAV
====

PyAV is a Pythonic binding for the [FFmpeg][ffmpeg] libraries. We aim to provide all of the power and control of the underlying library, but manage the gritty details as much as possible.

---

[![GitHub Test Status][github-tests-badge]][github-tests] [![Documentation][docs-badge]][docs] [![Python Package Index][pypi-badge]][pypi]

PyAV is for direct and precise access to your media via containers, streams, packets, codecs, and frames. It exposes a few transformations of that data, and helps you get your data to/from other packages (e.g. Numpy and Pillow).

This power does come with some responsibility as working with media is horrendously complicated and PyAV can't abstract it away or make all the best decisions for you. If the `ffmpeg` command does the job without you bending over backwards, PyAV is likely going to be more of a hindrance than a help.

But where you can't work without it, PyAV is a critical tool.


Installation
------------

Binary wheels are provided on [PyPI](https://pypi.org/project/pyav) for Linux, MacOS and Windows linked against the latest stable version of ffmpeg. You can install these wheels by running:

```bash
pip install pyav
```


Installing From Source
----------------------

Here's how to build PyAV from source source. You must use [MSYS2](https://www.msys2.org/) when using Windows.

```bash
git clone https://github.com/basswood-io/PyAV.git
cd PyAV
source scripts/activate.sh

# Build ffmpeg from source. You can skip this step
# if ffmpeg is already installed.
./scripts/build-deps

# Build
make

# Testing
make test

# Install globally
deactivate
pip install .
```

---


[docs-badge]: https://img.shields.io/badge/docs-on%20pyav.basswood--io.com-blue.svg
[docs]: https://pyav.basswood-io.com
[pypi-badge]: https://img.shields.io/pypi/v/pyav.svg?colorB=CCB39A

[github-tests-badge]: https://github.com/basswood-io/PyAV/workflows/tests/badge.svg
[github-tests]: https://github.com/basswood-io/PyAV/actions?workflow=tests
[github]: https://github.com/basswood-io/PyAV

[ffmpeg]: https://ffmpeg.org/
