"""
Implementation of `spatio-temporal voxel-grid` representation
"""
from typing import Iterator, Tuple

import numpy as np

from .base import BaseRepresentation


class VoxelGrid(BaseRepresentation):
    def __init__(self, num_events: int, frame_size: Tuple[int, int], bins=4):
        super().__init__()
        self.frame_size = frame_size
        self.num_events = num_events
        self.bins = bins

    def get_generator(
        self,
        events: np.ndarray,
    ) -> Iterator[np.ndarray]:
        event_count_frame = np.zeros(
            (self.frame_size[0], self.frame_size[1], self.bins)
        )
        t0 = events[0][2]
        dt = events[self.num_events - 1][2] - t0
        for ind, event in enumerate(events):
            y = int(event[0])
            x = int(event[1])
            ti = event[2]

            t = (self.bins - 1) / dt * (ti - t0)

            for tn in range(self.bins):
                event_count_frame[x, y, tn] += max(0, 1 - abs(tn - t))

            if ind % self.num_events == 0:
                yield event_count_frame
                event_count_frame = np.zeros_like(event_count_frame)
                t0 = events[ind][2]

                # Next frame has size self.num_events
                end_index = min(len(events) - 1, ind + self.num_events - 1)
                dt = events[end_index][2] - t0
