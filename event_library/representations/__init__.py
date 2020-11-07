"""
Set of events representations
"""
from . import constant_count, raw, spatiotemporal_voxel_grid


def get_representation(representation_type):
    """
    Dispatcher for implemented representations
    """
    switcher = {
        "constant-count": constant_count,
        "voxel": spatiotemporal_voxel_grid,
        "raw": raw,
    }

    return switcher[representation_type]


def get_generator(representation_type, **kwargs):
    def _generator(events):
        return get_representation(representation_type).get_generator(events, **kwargs)

    return _generator
