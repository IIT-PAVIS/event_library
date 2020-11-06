import numpy as np
from matplotlib import pyplot as plt


def get_generator(events: np.array, num_events: int, H: int, W: int, C=1):
    event_count_frame = np.zeros((H, W, C))

    for ind, event in enumerate(events):
        x = int(event[0])
        y = int(event[1])
        event_count_frame[x, y] += 1
        if ind % num_events == 0:
            yield event_count_frame
            event_count_frame = np.zeros_like(event_count_frame)


def display(self, frame_path):
    frame = np.load(frame_path)
    plt.imshow(frame)
    plt.show()
