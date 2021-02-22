"""
Implementation of `raw` events representation (no representation!)
"""
from typing import Iterator, Tuple

import numpy as np


def get_generator(events: np.array, **kwargs) -> Iterator[np.ndarray]:
    yield events


def display(frame: np.ndarray):
    raise NotImplementedError()
