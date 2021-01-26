"""
Implementation of `constant_count` representation per fixed time batch
"""
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt


def get_generator(
    events: np.array, frame_size: Tuple[int, int], frequence: float
) -> np.array:
    event_count_frame = np.zeros((frame_size[0], frame_size[1], 1), dtype="int")
    time_start = 0
    time_batch = 1 / frequence  # Convert from Hz
    breakpoint()
    for ind, event in enumerate(events):
        y = int(event[0])
        x = int(event[1])
        ti = event[2]
        event_count_frame[x, y] += 1
        if ti > time_start + time_batch:
            yield event_count_frame
            time_start = ti
            event_count_frame = np.zeros_like(event_count_frame)
    yield event_count_frame


def display(frame: np.array):
    plt.imshow(frame)
    plt.show()
