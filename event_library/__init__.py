import torch
import os
if torch.cuda.is_available():
    DEVICE = 'cuda'
else:
    DEVICE = 'cpu'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUPERSLO_CKPT = os.path.join(BASE_DIR, 'models', 'SuperSloMo.ckpt')
