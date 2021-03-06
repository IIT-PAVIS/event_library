"""
Implementation of `constant_count` representation per fixed time batch
"""
from typing import Tuple

import numpy as np

from .base import BaseRepresentation


class ConstantTime(BaseRepresentation):
    def __init__(self, num_events: int, frame_size: Tuple[int, int], frequence: float):
        super().__init__()
        self.frame_size = frame_size
        self.num_events = num_events
        self.frequence = frequence

    def get_generator(
        self,
        events: np.array,
    ) -> np.ndarray:
        event_count_frame = np.zeros(
            (self.frame_size[0], self.frame_size[1], 1), dtype="int"
        )
        time_start = 0
        time_batch = 1 / self.frequence  # Convert from Hz

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
