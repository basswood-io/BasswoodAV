#!/bin/bash

# Make sure this is sourced.
if [[ "$0" == "${BASH_SOURCE[0]}" ]]; then
    echo This must be sourced.
    exit 1
fi

export PYAV_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)"

if [[ ! "$PYAV_LIBRARY" ]]; then
    if [[ "$1" ]]; then
        if [[ "$1" == ffmpeg-* ]]; then
            PYAV_LIBRARY="$1"
        else
            echo "Error: PYAV_LIBRARY must start with 'ffmpeg-'" >&2
            return 1
        fi
    else
        PYAV_LIBRARY=ffmpeg-7.1.1
        echo "No \$PYAV_LIBRARY set; defaulting to $PYAV_LIBRARY"
    fi
fi
export PYAV_LIBRARY

if [[ ! "$PYAV_PYTHON" ]]; then
    PYAV_PYTHON="${PYAV_PYTHON-python3}"
    echo 'No $PYAV_PYTHON set; defaulting to python3.'
fi

export PYAV_PYTHON
export PYAV_PIP="${PYAV_PIP-$PYAV_PYTHON -m pip}"

if [[ "$GITHUB_ACTION" ]]; then
    # GitHub has a very self-contained environment. Lets just work in that.
    echo "We're on CI, so not setting up another virtualenv."
else
    export PYAV_VENV_NAME="$(uname -s).$(uname -r).$("$PYAV_PYTHON" -c '
import sys
import platform
print("{}{}.{}".format(platform.python_implementation().lower(), *sys.version_info[:2]))
    ')"
    export PYAV_VENV="$PYAV_ROOT/venvs/$PYAV_VENV_NAME"

    if [[ ! -e "$PYAV_VENV/bin/python" ]]; then
        mkdir -p "$PYAV_VENV"
        virtualenv -p "$PYAV_PYTHON" "$PYAV_VENV"
        "$PYAV_VENV/bin/pip" install --upgrade pip setuptools
    fi

    if [[ -e "$PYAV_VENV/bin/activate" ]]; then
        source "$PYAV_VENV/bin/activate"
    else
        # Not a virtualenv (perhaps a debug Python); lets manually "activate" it.
        PATH="$PYAV_VENV/bin:$PATH"
    fi
fi

# Just a flag so that we know this was supposedly run.
export _PYAV_ACTIVATED=1

export PYAV_LIBRARY_ROOT="${PYAV_LIBRARY_ROOT-$PYAV_ROOT/vendor}"
export PYAV_LIBRARY_BUILD="${PYAV_LIBRARY_BUILD-$PYAV_LIBRARY_ROOT/build}"
export PYAV_LIBRARY_PREFIX="$PYAV_LIBRARY_BUILD/$PYAV_LIBRARY"

export PATH="$PYAV_LIBRARY_PREFIX/bin:$PATH"
export PYTHONPATH="$PYAV_ROOT:$PYTHONPATH"
export PKG_CONFIG_PATH="$PYAV_LIBRARY_PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="$PYAV_LIBRARY_PREFIX/lib:$LD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH="$PYAV_LIBRARY_PREFIX/lib:$DYLD_LIBRARY_PATH"
