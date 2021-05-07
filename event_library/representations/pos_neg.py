"""
Implementation of `pos_neg` representation. Similar to `constant_count`, but
keeps positive and negative events in two separated layers and apply some
preprocessing.
"""
from typing import Iterator, Tuple

import numpy as np

from .base import BaseRepresentation


class PosNeg(BaseRepresentation):
    def __init__(self, num_events: int, frame_size: Tuple[int, int]):
        super().__init__()
        self.frame_size = frame_size
        self.num_events = num_events

    def get_generator(self, events: np.ndarray) -> Iterator[np.ndarray]:
        event_frame = np.zeros((self.frame_size[0], self.frame_size[1], 3), dtype="int")
        for ind, event in enumerate(events):
            y = int(event[0])
            x = int(event[1])
            p = int(event[3]) > 0
            event_frame[x, y, p] += 1
            event_frame *= 50
            yield event_frame
            event_frame = np.zeros_like(event_frame)
