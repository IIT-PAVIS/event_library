class Representation:
    def __init__(self):
        pass

    def display(self, file_path):
        pass


class FrameRepresentation(Representation):
    def __init__(self, num_events: int):
        super(FrameRepresentation, self).__init__()
        self.num_events = num_events


class RawRepresentation(Representation):
    def __init__(self):
        super(RawRepresentation, self).__init__()


class VoxelRepresentation(FrameRepresentation):
    def __init__(self):
        super(VoxelRepresentation, self).__init__()
