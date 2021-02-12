import argparse
import os
from datetime import datetime
from multiprocessing.pool import ThreadPool

import numpy as np
import torch

from . import SUPERSLO_CKPT
from .utils import Upsampler


def get_freer_gpu():
    os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >tmp')
    memory_available = [int(x.split()[2]) for x in open('tmp', 'r').readlines()]
    return np.argmax(memory_available)


def upsample(input_dir, output_dir, output_size=None, n_threads=1):
    try:
        os.makedirs(SUPERSLO_CKPT, exist_ok=True)
        assert os.path.isdir(input_dir), "The input directory must exist"
        assert not os.path.exists(output_dir), "The output directory must not exist"

        ckpt_file = os.path.join(SUPERSLO_CKPT, "SuperSloMo.ckpt")

        if not os.path.exists(ckpt_file):
            Upsampler._download_net(ckpt_file)
            if not os.path.exists(ckpt_file):
                raise Exception("MODEL not found. Please provide it manually")

        # get inputs
        sequences = Upsampler.get_sequences(input_dir, output_dir)
        Upsampler._prepare_output_dir(input_dir, output_dir)
        # pool of threads
        def _upsample_sequence(seq):
            device_id = get_freer_gpu()
            device = torch.device(f"cuda:{device_id}")
            return Upsampler(device=device, ckpt_file=ckpt_file).upsample_sequence(
                **seq, output_size=output_size
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
