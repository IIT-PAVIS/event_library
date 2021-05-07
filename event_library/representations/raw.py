"""
Implementation of `raw` events representation (no representation!)
"""
from typing import Iterator, Tuple

import numpy as np

from .base import BaseRepresentation


class Raw(BaseRepresentation):
    def __init__(self):
        super().__init__()

    def get_generator(self, events: np.ndarray) -> Iterator[np.ndarray]:
        yield events
