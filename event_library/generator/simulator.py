"""
Simulator wrapper for esim_py EventSimulator. It wrapped the original simulator, which must be
present. More advance wrappers (e.g., with parameters sampling) can be implemented as well
"""

import glob
import os

import cv2
from esim_py import EventSimulator


class SimulatorWrapper(EventSimulator):
    def __init__(self, Cp, Cn, refractory_period, log_eps, use_log, batch_size=2000):
        super(SimulatorWrapper, self).__init__(
            Cp, Cn, refractory_period, log_eps, use_log
        )
        self.batch_size = batch_size
        self.ts = []
        self.images_path = []

    def set_input_dir(self, input_dir: str):
        """
        It loads images and timestamp from an input video frames. It expects
        a 'img' directory with the frames of the video ordered by name and a "timestamps.txt" file
        that specify the timestamp of the video. Must be called before the iterator!
        """

        img_dir = os.path.join(input_dir, "imgs", "*")
        self.ts = self._get_ts_from_file(input_dir)
        self.images_path = sorted(glob.glob(img_dir))

    def _get_ts_from_file(self, input_dir):
        ts_path = os.path.join(input_dir, "timestamps.txt")
        ts = []
        with open(ts_path) as ts_file:
            for x in ts_file:
                ts.append(float(x))
        return ts

    def get_frames_dimension(self) -> (int, int, int):
        """
        Returns
        -------
        Return the dimension of the frames of the video

        """
        shape = cv2.imread(self.images_path[0]).shape
        return shape

    def __len__(self):
        return len(self.images_path) // self.batch_size + 1

    def __iter__(self):
        for idx in range(len(self)):
            start_id = idx * self.batch_size
            end_id = min(start_id + self.batch_size, len(self.images_path))
            images_input_paths = self.images_path[start_id:end_id]
            ts_input_paths = self.ts[start_id:end_id]
            events = self.generateFromStampedImageSequence(
                images_input_paths, ts_input_paths
            )
            yield events
