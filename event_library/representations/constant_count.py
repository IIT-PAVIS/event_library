"""
Implementation of `constant_count` representation
"""
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt


def get_generator(
    events: np.array, num_events: int, frame_size: Tuple[int, int]
) -> np.array:
    event_count_frame = np.zeros((frame_size[0], frame_size[1], 1), dtype="int")

    for ind, event in enumerate(events):
        y = int(event[0])
        x = int(event[1])
        event_count_frame[x, y] += 1
        if ind % num_events == 0:
            yield event_count_frame
            event_count_frame = np.zeros_like(event_count_frame)


def display(frame: np.array):
    plt.imshow(frame)
    plt.show()
