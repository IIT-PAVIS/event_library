"""
Implementation of `spatio-temporal voxel-grid` representation
"""
from typing import Tuple

import numpy as np
from matplotlib import pyplot as pl


def get_generator(
    events: np.array, num_events: int, frame_size: Tuple[int, int], bins: int, **kwargs
) -> np.array:

    event_count_frame = np.zeros((frame_size[0], frame_size[1], bins))
    t0 = events[0][2]
    dt = events[num_events - 1][2] - t0

    for ind, event in enumerate(events):
        y = int(event[0])
        x = int(event[1])
        ti = event[2]
        p = int(event[3])
        t = (bins - 1) / dt * (ti - t0)

        for tn in range(bins):
            event_count_frame[x, y, tn] += p * max(0, 1 - abs(tn - t))

        if ind % num_events == 0:
            yield event_count_frame
            event_count_frame = np.zeros_like(event_count_frame)
            t0 = events[ind][2]

            # Next frame has size self.num_events
            end_index = min(len(events) - 1, ind + num_events - 1)
            dt = events[end_index][2] - t0


def display(frame: np.array):
    raise NotImplementedError
