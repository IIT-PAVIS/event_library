import argparse
import os
from pathlib import Path

import cv2
import numpy as np
from matplotlib import pyplot as plt

import event_library
import event_library.representations as representations
import event_library.utils as utils


def accumulate_and_save(
    input_path: str, output_path: str, representation_name: str, **kwargs
) -> None:
    events = utils.load_from_file(input_path, 100000)
    os.makedirs(output_path, exist_ok=True)
    representation = representations.get_representation(representation_name)

    for i, frame in enumerate(representation.get_generator(events=events, **kwargs)):
        # debug only
        dist = frame / frame.max()
        cv2.imshow("test1", dist)

        np.save(f"{output_path}/frame{i:04d}.npy", frame)
        if cv2.waitKey(1002) & 0xFF == ord("q"):
            break


def main():
    parser = argparse.ArgumentParser(
        description="Accumulates events to an event-frame."
    )
    parser.add_argument("--input_files", nargs="+", help="file(s) to convert to output")
    parser.add_argument("--output_dir", type=str, help="output_dir")
    parser.add_argument(
        "--num_events", type=int, default=5000, help="num events to accumulate"
    )
    parser.add_argument("--representation", default="pos-neg", help="height")
    parser.add_argument("--height", default=211, help="height frame")
    parser.add_argument("--width", default=84, help="width of frame")

    args = parser.parse_args()
    input_files = args.input_files
    output_dir = args.output_dir
    representation = args.representation
    args = {"num_events": args.num_events, "frame_size": (args.height, args.width)}

    for input_path in input_files:
        out_name = Path(input_path).name.split(".")[0]

        out_path = os.path.join(output_dir, out_name)
        accumulate_and_save(input_path, out_path, representation, **args)


if __name__ == "__main__":
    main()
