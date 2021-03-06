"""
Set of events representations. Each representation is implemented as a python module with a
standard interface. Each module must implement at least the `get_generator` function:

def get_generator(events: np.array, ...) -> np.array:
    pass

It receives a numpy array of events of shape (Nx4). Each `row` i is an event tuple as:

- events[i][0] = y axis
- events[i][1] = x axis
- events[i][2] = timestamp in ns
- events[i][3] = boolean value (increasing or decreasing light intensity change)

"""

from typing import Any, Callable, Iterable

import numpy as np

from .base import BaseRepresentation
from .constant_count import ConstantCount
from .pos_neg import PosNeg
from .raw import Raw
from .spatiotemporal_voxel_grid import VoxelGrid
from .time_count import ConstantTime


def get_representation(representation_type: str):
    """
    Dispatcher for implemented representations. It receive one of the following representation type
    (`raw`, `voxel`, `constant-count`)
    """

    switcher = {
        "constant-count": ConstantCount,
        "voxel": VoxelGrid,
        "raw": Raw,
        "pos-neg": PosNeg,
        "constant-time": ConstantTime,
    }

    return switcher[representation_type]


def get_generator(
    representation_type: str, **kwargs
) -> Callable[[Any], Iterable[np.ndarray]]:
    """
    Dispatcher for `get_generator` from an implemented representation. It returns the generator
    for the specified representation type

    Parameters
    ----------
    representation_type:
        name of the representation to use
    kwargs:
        arguments for representation generator


    """

    def _generator(events: np.ndarray):
        return get_representation(representation_type).get_generator(events, **kwargs)

    return _generator
