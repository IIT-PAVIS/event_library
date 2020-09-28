import numpy as np
import cv2
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
    def __init__(self, H, W, C, num_events):
        super(FrameRepresentation, self).__init__()
        self.H = H
        self.W = W
        self.C = C
        self.num_events = num_events

    def get_size(self):
        return (self.W, self.H)

    def display(self, frame_path):
        fig, ax = plt.subplots(ncols=self.C, nrows=1, figsize=(20, 20))
        frame = np.load(frame_path)
        for i in range(self.C):
            ax[i].imshow(frame[:, :, i])
            ax[i].axis('off')
        plt.show()


class ConstantRepresentation(FrameRepresentation):
    def __init__(self, H, W, num_events):
        super(ConstantRepresentation, self).__init__(H, W, 1, num_events)

    def frame_generator(self, events):
        event_count_frame = np.zeros((self.W, self.H))
        for ind, event in enumerate(events):
            x = int(event[0])
            y = int(event[1])
            event_count_frame[x, y] += 1
            if ind % self.num_events == 0:
                yield event_count_frame
                event_count_frame = np.zeros_like(event_count_frame)


class RawRepresentation(Representation):
    def __init__(self):
        super(RawRepresentation, self).__init__()

    def frame_generator(self, events):
        yield events


class VoxelRepresentation(FrameRepresentation):
    def __init__(self, H, W, C, num_events):
        super(VoxelRepresentation, self).__init__(H, W, C, num_events)

    def frame_generator(self, events):
        event_count_frame = np.zeros((self.W, self.H, self.C))
        t0 = events[0][2]
        dt = events[self.num_events - 1][2] - t0

        for ind, event in enumerate(events):
            x = int(event[0])
            y = int(event[1])
            ti = event[2]
            p = int(event[3])

            t = (self.C - 1) / dt * (ti - t0)

            for tn in range(self.C):
                event_count_frame[x, y, tn] += p * max(0, 1 - abs(tn - t))

            if ind % self.num_events == 0:
                yield event_count_frame
                event_count_frame = np.zeros_like(event_count_frame)
                t0 = events[ind][2]

                # Next frame has size self.num_events
                end_index = min(len(events) - 1, ind + self.num_events - 1)
                dt = events[end_index][2] - t0
