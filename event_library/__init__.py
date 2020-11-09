import os

import torch

if torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

ROOT_PACKAGE = os.path.dirname(os.path.abspath(__file__))
