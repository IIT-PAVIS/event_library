import argparse
import logging
import os

import cv2
import hydra
import numpy as np
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

import event_library as el
import event_library.representations as representations

# A logger for this file
log = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser(
        description="Accumulates events to an event-frame."
    )
    parser.add_argument(
        "--input_dir", type=str, help="input_dir containing event files"
    )
    parser.add_argument("--output_dir", type=str, help="output_dir")
    parser.add_argument("--fps", type=int, default=50, help="fps")
    parser.add_argument("--hw_type", type=str, default='dvs', help="dvs frame size")

    args = parser.parse_args()
    return args


def normalized_3sigma(input_img: np.ndarray) -> np.ndarray:
    img = input_img.copy().astype('float')

    sig_img = img[img > 0].std()
    if sig_img < 0.1 / 255:
        sig_img = 0.1 / 255
    numSdevs = 3.0
    range = numSdevs * sig_img

    img[img != 0] *= 255 / range
    img[img < 0] = 0
    img[img > 255] = 255

    return img.astype('uint8')


def main():

    args = get_args()
    if args.input_dir is None:
        log.error("Please provide an input_dir")
        return

    log.info(f"Generating video for {args.input_dir}")
    os.makedirs(args.output_dir, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    size = el.utils.get_hw_property(args.hw_type).size
    out = cv2.VideoWriter(
        os.path.join(args.output_dir, 'out.avi'),
        fourcc,
        args.fps,
        (size[1], size[0]),
        0,
    )
    for frame_path in sorted(os.listdir(args.input_dir)):
        frame = np.load(os.path.join(args.input_dir, frame_path), allow_pickle=True)

        frame_normalized = normalized_3sigma(frame)

        out.write(frame_normalized)
    out.release()


if __name__ == "__main__":
    main()
