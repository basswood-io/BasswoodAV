from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codecs", action="store_true")
    parser.add_argument("--hwdevices", action="store_true")
    parser.add_argument("--hwconfigs", action="store_true")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        import bv
        import bv._core

        print(f"BasswoodAV v{bv.__version__}")

        by_config: dict = {}
        for libname, config in sorted(bv._core.library_meta.items()):
            version = config["version"]
            if version[0] >= 0:
                by_config.setdefault(
                    (config["configuration"], config["license"]), []
                ).append((libname, config))

        for (config, license), libs in sorted(by_config.items()):
            print("library configuration:", config)
            print("library license:", license)
            for libname, config in libs:
                version = config["version"]
                print(f"{libname:<13} {version[0]:3d}.{version[1]:3d}.{version[2]:3d}")

    if args.hwdevices:
        from bv.codec.hwaccel import hwdevices_available

        print("Hardware device types:")
        for x in hwdevices_available():
            print("   ", x)

    if args.hwconfigs:
        from bv.codec.codec import dump_hwconfigs

        dump_hwconfigs()

    if args.codecs:
        from bv.codec.codec import dump_codecs

        dump_codecs()


if __name__ == "__main__":
    main()
