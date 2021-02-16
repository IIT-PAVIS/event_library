import argparse
import os
from pathlib import Path

import cv2
import numpy as np
from matplotlib import pyplot as plt

import event_library
import event_library.representations as representations
import event_library.utils as utils


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


def accumulate_and_save(
    input_path: str, output_path: str, representation_name: str, **kwargs
) -> None:
    events = utils.load_from_file(input_path, num_events=-1)
    os.makedirs(output_path, exist_ok=True)
    representation = representations.get_representation(representation_name)

    for i, frame in enumerate(representation.get_generator(events=events, **kwargs)):
        cv2.imwrite(f"{output_path}/frame{i:04d}.png", normalized_3sigma(frame))


def main():
    parser = argparse.ArgumentParser(
        description="Accumulates events to an event-frame."
    )
    parser.add_argument("--input_files", nargs="+", help="file(s) to convert to output")
    parser.add_argument("--output_dir", type=str, help="output_dir")
    parser.add_argument(
        "--num_events", type=int, default=5000, help="num events to accumulate"
    )
    parser.add_argument("--representation", default="constant-count", help="height")
    parser.add_argument("--height", default=360, help="height frame")
    parser.add_argument("--width", default=360, help="width of frame")

    args = parser.parse_args()
    input_files = args.input_files
    output_dir = args.output_dir
    representation = args.representation
    args = {"num_events": 7500, "frame_size": (args.height, args.width)}
    for input_path in input_files:
        out_name = Path(input_path).name.split(".")[0]

        out_path = os.path.join(output_dir, out_name)
        accumulate_and_save(input_path, out_path, representation, **args)


if __name__ == "__main__":
    main()
