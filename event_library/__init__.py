import os

import torch

if torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

ROOT_PACKAGE = os.path.dirname(os.path.abspath(__file__))

__author__ = "gscarpellini"
__version__ = "0.3"
__author_email__ = "gianluca.scarpellini@iit.it"
__license__ = "GPLv3"
__copyright__ = f"Copyright (c) 2020 under {__license__}, {__author__}."
