"""
Implementation of `raw` events representation (no representation!)
"""
from typing import Tuple

import numpy as np


def get_generator(events: np.array, **kwargs) -> np.array:
    yield events


def display(frame: np.array):
    raise NotImplementedError()
