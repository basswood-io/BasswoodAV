from struct import calcsize
import argparse
import os
import platform
import shutil
import subprocess


def get_platform():
    system = platform.system()
    machine = platform.machine()

    if system == "Linux":
        return f"manylinux_{machine}"

    if system == "Darwin":
        # cibuildwheel sets ARCHFLAGS:
        # https://github.com/pypa/cibuildwheel/blob/5255155bc57eb6224354356df648dc42e31a0028/cibuildwheel/macos.py#L207-L220
        if "ARCHFLAGS" in os.environ:
            machine = os.environ["ARCHFLAGS"].split()[1]
        return f"macosx_{machine}"

    if system == "Windows":
        return "win_amd64" if calcsize("P") * 8 == 64 else "win32"

    raise Exception(f"Unsupported system {system}")


parser = argparse.ArgumentParser(description="Fetch and extract tarballs")
parser.add_argument("destination_dir")
parser.add_argument("--cache-dir", default="tarballs")
args = parser.parse_args()

print(f"Creating directory {args.destination_dir}")
if os.path.exists(args.destination_dir):
    shutil.rmtree(args.destination_dir)
os.makedirs(args.destination_dir)

tarball_url = f"https://github.com/PyAV-Org/pyav-ffmpeg/releases/download/5.1.2-1/ffmpeg-{get_platform()}.tar.gz"

tarball_name = tarball_url.split("/")[-1]
tarball_file = os.path.join(args.cache_dir, tarball_name)

if not os.path.exists(tarball_file):
    print(f"Downloading {tarball_url}")
    if not os.path.exists(args.cache_dir):
        os.mkdir(args.cache_dir)
    subprocess.run(
        ["curl", "--location", "--output", tarball_file, "--silent", tarball_url]
    )

print(f"Extracting {tarball_name}")
subprocess.run(["tar", "-C", args.destination_dir, "-xf", tarball_file])
