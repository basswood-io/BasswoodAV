LDFLAGS ?= ""
CFLAGS ?= "-O0"

PYAV_PYTHON ?= python
PYTHON := $(PYAV_PYTHON)


.PHONY: default build cythonize clean clean-all info lint test fate-suite test-assets docs

default: build


build:
	CFLAGS=$(CFLAGS) LDFLAGS=$(LDFLAGS) $(PYTHON) setup.py build_ext --inplace --debug

cythonize:
	$(PYTHON) setup.py cythonize


wheel: build-mingw32
	$(PYTHON) setup.py bdist_wheel

build-mingw32:
	# before running, set PKG_CONFIG_PATH to the pkgconfig dir of the ffmpeg build.
	# set PKG_CONFIG_PATH=D:\dev\3rd\media-autobuild_suite\local32\bin-video\ffmpegSHARED\lib\pkgconfig
	CFLAGS=$(CFLAGS) LDFLAGS=$(LDFLAGS) $(PYTHON) setup.py build_ext --inplace -c mingw32
	mv *.pyd av


fate-suite:
	# Grab ALL of the samples from the ffmpeg site.
	rsync -vrltLW rsync://fate-suite.ffmpeg.org/fate-suite/ tests/assets/fate-suite/

lint:
	TESTSUITE=flake8 scripts/test
	TESTSUITE=isort scripts/test

test:
	$(PYTHON) setup.py test

tmp/ffmpeg-git:
	@ mkdir -p tmp/ffmpeg-git
	git clone --depth=1 git://source.ffmpeg.org/ffmpeg.git tmp/ffmpeg-git

clean-build:
	- rm -rf build
	- find av -name '*.so' -delete

clean-sandbox:
	- rm -rf sandbox/201*
	- rm -f sandbox/last

clean-src:
	- rm -rf src

clean: clean-build clean-sandbox clean-src
clean-all: clean-build clean-sandbox clean-src
