"""

Events: numpy array as Nx4
Each event is a tuple (y, x, t, p):
y, x: position of the event on the image plane
t: timestamp in second, starting at 0
p: polarity (+1, -1)

"""

import pathlib

import numpy as np


def load_from_file(file_path: str, **kwargs) -> np.array:
    ext = pathlib.Path(file_path).suffix
    switcher = {
        ".txt": load_from_txt,
        ".aedat": load_from_aedat_multi_cam,
        '.npy': load_from_numpy,
    }
    return switcher[ext](file_path, **kwargs)  # type: ignore


def load_from_numpy(file_path: str, num_events: int = -1) -> np.array:
    events = np.load(file_path, allow_pickle=True)

    # normalize events time starting at 0

    events[:, 2] -= events[0, 2]
    return events


def load_from_aedat_multi_cam(
    file_path: str, num_events: int, cam: int = 1
) -> np.array:
    from aedat import import_aedat

    events = import_aedat({'filePathAndName': file_path})
    # timestamps in seconds
    timestamps = events['data']['polarity']['timeStamp'] / 1e6
    timestamps -= timestamps[0]

    x = events['data']['polarity']['x']
    y = events['data']['polarity']['y']
    mask = events['data']['polarity']['cam'] == cam
    polarity = events['data']['polarity']['polarity']

    return np.stack([y[mask], x[mask], timestamps[mask], polarity[mask]], 1)


def load_from_txt(file_path: str, num_events: int) -> np.array:
    with open(file_path, "r") as file_txt:
        reading = []

        while (line := file_txt.readline()) and num_events != 0:  # noqa
            reading.append(line)
            num_events -= 1

        result = np.loadtxt(reading, dtype="float")
        if num_events == 1:
            # Simple trick to get 1x4 np array
            result = np.expand_dims(result, 0)

        return result[:, [1, 2, 0, 3]]
