"""
Set of events representations
"""
from . import constant_count, raw, spatiotemporal_voxel_grid


def get_representation(representation_type):
    switcher = {
        "constant-count": constant_count,
        "voxel": spatiotemporal_voxel_grid,
        "raw": raw,
    }

    return switcher[representation_type]
