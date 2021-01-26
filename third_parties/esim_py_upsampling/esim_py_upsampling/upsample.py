import argparse
import os
from datetime import datetime
from multiprocessing.pool import ThreadPool

from . import SUPERSLO_CKPT
from .utils import Upsampler


def upsample(input_dir, output_dir, device, n_threads=1):
    breakpoint()
    if os.path.exists(output_dir):
        print("Upsampling already exists!")
        return

    try:
        os.makedirs(SUPERSLO_CKPT, exist_ok=True)
        ckpt_file = os.path.join(SUPERSLO_CKPT, "SuperSloMo.ckpt")

        if not os.path.exists(ckpt_file):
            Upsampler._download_net(ckpt_file)

        # Preparing
        assert os.path.isdir(input_dir), "The input directory must exist"
        assert not os.path.exists(output_dir), "The output directory must not exist"
        Upsampler._prepare_output_dir(input_dir, output_dir)

        # get inputs
        sequences = Upsampler.get_sequences(input_dir, output_dir)
        breakpoint()

        # pool of threads
        def _upsample_sequence(seq):
            return Upsampler(device=device, ckpt_file=ckpt_file).upsample_sequence(
                **seq
            )

        with ThreadPool(n_threads) as pool:
            start = datetime.now()
            pool.map(_upsample_sequence, sequences)
            print(f"Total time: {datetime.now() - start}")
    except Exception as ex:  # noqa: E722
        print(ex)
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
