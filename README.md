<p align="center"><img src="https://av.basswood-io.com/docs/stable/_static/logo.avif" title="BasswoodAV" width="700"></p>

# BasswoodAV

BasswoodAV provides Pythonic binding for the [FFmpeg][ffmpeg] libraries. We aim to provide all of the power and control of the underlying library, but manage the gritty details as much as possible.

---

[![GitHub Test Status][github-tests-badge]][github-tests] [![Documentation][docs-badge]][docs] [![Python Package Index][pypi-badge]][pypi]

BasswoodAV provides direct and precise access to your media via containers, streams, packets, codecs, and frames. It exposes a few transformations of that data, and helps you get your data to/from other packages, such as Numpy.

This power does come with some responsibility as working with media is complicated and BasswoodAV can't abstract it away or make all the best decisions for you. But where you can't work without it, BasswoodAV is a critical tool.


## Installation
Binary wheels are provided on [PyPI][pypi] for Linux, MacOS and Windows linked against the latest stable version of ffmpeg. You can install these wheels by running:

```bash
pip install basswood-av
```

## Installing From Source
Here's how to build BasswoodAV from source source. You must use [MSYS2](https://www.msys2.org/) when using Windows.

```bash
git clone https://github.com/basswood-io/BasswoodAV.git
cd BasswoodAV
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

[docs-badge]: https://img.shields.io/badge/docs-on%20av.basswood--io.com-blue.svg
[docs]: https://av.basswood-io.com
[pypi-badge]: https://img.shields.io/pypi/v/basswood-av.svg?colorB=CCB39A
[pypi]: https://pypi.org/project/basswood-av
[github-tests-badge]: https://github.com/basswood-io/BasswoodAV/workflows/tests/badge.svg
[github-tests]: https://github.com/basswood-io/BasswoodAV/actions?workflow=tests
[github]: https://github.com/basswood-io/BasswoodAV
[ffmpeg]: https://ffmpeg.org/
