"""
Implementation of `raw` events representation (no representation!)
"""
from typing import Iterator, Tuple

import numpy as np


def get_generator(events: np.ndarray, **kwargs) -> Iterator[np.ndarray]:
    yield events


def display(frame: np.ndarray):
    raise NotImplementedError()
