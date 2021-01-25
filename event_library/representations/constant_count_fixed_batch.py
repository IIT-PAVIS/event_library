"""
Implementation of `constant_count` representation per fixed time batch
"""
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt


def get_generator(
    events: np.array, num_events: int, frame_size: Tuple[int, int], time_batch: float
) -> np.array:
    event_count_frame = np.zeros((frame_size[0], frame_size[1], 1), dtype="int")
    time_start = 0
    time_batch = time_batch * 1e9  # Convert Hz to ns range
    for ind, event in enumerate(events):
        y = int(event[0])
        x = int(event[1])
        ti = event[2]
        event_count_frame[x, y] += 1
        if ti > time_start + time_batch:
            yield event_count_frame
            time_start = ti
            event_count_frame = np.zeros_like(event_count_frame)


def display(frame: np.array):
    plt.imshow(frame)
    plt.show()
