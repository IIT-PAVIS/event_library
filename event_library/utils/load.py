import numpy as np
import pathlib


def load_from_file(file_path: str, num_events: int) -> np.array:
    ext = pathlib.Path(file_path).suffix
    switcher = {'.txt': load_from_txt}
    return switcher[ext](file_path, num_events)


def load_from_txt(file_path: str, num_events: int) -> np.array:
    with open(file_path, 'r') as file_txt:
        count = 0
        reading = []
        while ((line := file_txt.readline()) and count < num_events):
            reading.append(line)
            count += 1

        result = np.loadtxt(reading, dtype='float')
        if num_events == 1:
            # Simple trick to get 1x4 np array
            result = np.expand_dims(result, 0)

        return result[:, [1, 2, 0, 3]]
