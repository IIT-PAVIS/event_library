"""
Implementation of `pos_neg` representation. Similar to `constant_count`, but
keeps positive and negative events in two separated layers and apply some
preprocessing. For more, 
"""
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt


def get_generator(
    events: np.array, num_events: int, frame_size: Tuple[int, int]
) -> np.array:
    event_frame = np.zeros((frame_size[0], frame_size[1], 3), dtype="int")
    
    for ind, event in enumerate(events):
        y = int(event[0])
        x = int(event[1])
        p = int(event[3])
        event_count_frame[x, y, p] += 1

        if ind % num_events == 0:
            event_frame *= 50            
            yield event_count_frame
            event_count_frame = np.zeros_like(event_count_frame)


def display(frame: np.array):
    plt.imshow(frame)
    plt.show()
