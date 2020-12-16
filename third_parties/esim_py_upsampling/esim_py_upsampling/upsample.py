import argparse
import os

from . import SUPERSLO_CKPT
from .utils import Upsampler


def upsample(input_dir, output_dir, device):
    if os.path.exists(output_dir):
        print("Upsampling already exists!")
        return

    try:
        upsampler = Upsampler(
            input_dir=input_dir,
            output_dir=output_dir,
            device=device,
            ckpt_dir=SUPERSLO_CKPT,
        )
        upsampler.upsample()
    except:  # noqa: E722
        print(
            f"Upsampling failed, but directory '{output_dir}' was created. Remove it if you need to try again "
        )


def get_flags():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_dir",
        required=True,
        help="Path to input directory. See README.md for expected structure of the directory.",
    )
    parser.add_argument(
        "--output_dir",
        required=True,
        help="Path to non-existing output directory. This script will generate the directory.",
    )
    parser.add_argument(
        "--device", type=str, default="cpu", help="Device to be used (cpu, cuda:X)"
    )
    args = parser.parse_args()
    return args


def main():
    flags = get_flags()

    upsampler = Upsampler(
        input_dir=flags.input_dir, output_dir=flags.output_dir, device=flags.device
    )
    upsampler.upsample()


if __name__ == "__main__":
    main()
