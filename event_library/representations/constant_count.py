"""
Implementation of `constant_count` representation
"""
from typing import Iterator, Tuple

import numpy as np

from .base import BaseRepresentation


class ConstantCount(BaseRepresentation):
    def __init__(self, num_events: int, frame_size: Tuple[int, int]):
        super().__init__()
        self.frame_size = frame_size
        self.num_events = num_events

    def get_generator(self, events: np.ndarray) -> Iterator[np.ndarray]:
        event_count_frame = np.zeros(
            (self.frame_size[0], self.frame_size[1], 1), dtype="int"
        )
        for ind, event in enumerate(events):
            y = int(event[0])
            x = int(event[1])
            event_count_frame[x, y] += 1
            if ind % self.num_events == 0:
                yield event_count_frame
                event_count_frame = np.zeros_like(event_count_frame)
