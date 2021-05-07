from abc import ABC, abstractmethod
from typing import Iterator

import numpy as np
from matplotlib import pyplot as plt


class BaseRepresentation(ABC):
    @abstractmethod
    def get_generator(self, events: np.ndarray) -> Iterator[np.ndarray]:
        pass

    @staticmethod
    def show(frame: np.ndarray):
        plt.imshow(frame)
        plt.show()
