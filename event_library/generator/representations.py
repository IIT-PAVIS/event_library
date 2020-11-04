import numpy as np
from matplotlib import pyplot as plt

__all__ = [
    'ConstantRepresentation', 'VoxelRepresentation', 'RawRepresentation'
]


class Representation:
    def __init__(self):
        pass

    def display(self, file_path):
        pass


class FrameRepresentation(Representation):
    def __init__(self, num_events):
        super(FrameRepresentation, self).__init__()
        self.num_events = num_events


class ConstantRepresentation(FrameRepresentation):
    def __init__(self, num_events):
        super(ConstantRepresentation, self).__init__(num_events)

    def frame_generator(self, events: np.array, H, W, C):
        event_count_frame = np.zeros((W, H))
        for ind, event in enumerate(events):
            x = int(event[0])
            y = int(event[1])
            event_count_frame[x, y] += 1
            if ind % self.num_events == 0:
                yield event_count_frame
                event_count_frame = np.zeros_like(event_count_frame)

    def display(self, frame_path):
        frame = np.load(frame_path)
        plt.imshow(frame)
        plt.show()

        
class RawRepresentation(Representation):
    def __init__(self):
        super(RawRepresentation, self).__init__()

    def frame_generator(self, events):
        yield events


class VoxelRepresentation(FrameRepresentation):
    def __init__(self):
        super(VoxelRepresentation, self).__init__()

    def frame_generator(self, events, H, W, C, num_events):
        event_count_frame = np.zeros((H, W, C))
        t0 = events[0][2]
        dt = events[num_events - 1][2] - t0

        for ind, event in enumerate(events):
            x = int(event[0])
            y = int(event[1])
            ti = event[2]
            p = int(event[3])
            t = (C - 1) / dt * (ti - t0)

            for tn in range(C):
                event_count_frame[x, y, tn] += p * max(0, 1 - abs(tn - t))

            if ind % self.num_events == 0:
                yield event_count_frame
                event_count_frame = np.zeros_like(event_count_frame)
                t0 = events[ind][2]

                # Next frame has size self.num_events
                end_index = min(len(events) - 1, ind + num_events - 1)
                dt = events[end_index][2] - t0

    def display(self, frame_path):
        fig, ax = plt.subplots(ncols=self.C, nrows=1, figsize=(20, 20))
        frame = np.load(frame_path)
        for i in range(self.C):
            ax[i].imshow(frame[:, :, i])
            ax[i].axis('off')
        plt.show()
