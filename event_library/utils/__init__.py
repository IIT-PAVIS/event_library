from collections import namedtuple

from .load import *

HardwareProperties = namedtuple('HardwareProperties', ['size'])


def get_hw_property(hw_type: str):
    switch = {'dvs': HardwareProperties(size=(346, 260))}
    return switch[hw_type]
