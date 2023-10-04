# PyAV

[![GitHub Test Status][https://github.com/WyattBlue/PyAV/workflows/tests/badge.svg]][https://github.com/WyattBlue/PyAV/actions?workflow=tests]

PyAV is a Pythonic binding for the [FFmpeg][https://ffmpeg.org] libraries. We aim to provide all of the power and control of the underlying library, but manage the gritty details as much as possible.

PyAV is for direct and precise access to your media via containers, streams, packets, codecs, and frames. It exposes a few transformations of that data, and helps you get your data to/from other packages (e.g. Numpy and Pillow).

This power does come with some responsibility as working with media is horrendously complicated and PyAV can't abstract it away or make all the best decisions for you. If the `ffmpeg` command does the job without you bending over backwards, PyAV is likely going to be more of a hindrance than a help.

But where you can't work without it, PyAV is a critical tool.


## Installation
Due to the complexity of the dependencies, PyAV is not always the easiest Python package to install from source. Binary wheels are provided on [PyPI][https://pypi.org/project/pyav] for  MacOS, Windows, and Linux linked against a modern FFmpeg. You can install these wheels by running:

```bash
pip install pyav
```

If you want to use your existing FFmpeg, the source version is available too:

```bash
pip install pyav --no-binary pyav
```

## Alternative installation methods

Another way of installing PyAV is via [conda-forge][https://conda-forge.github.io/]:

```bash
conda install av -c conda-forge
```

And if you want to build from the absolute source (for development or testing):

```bash
git clone https://github.com/WyattBlue/PyAV.git
cd PyAV
source scripts/activate.sh

pip install -U -r tests/requirements.txt
./scripts/build-deps

make
```

---

Have fun, and good luck!
