# Must be set before importing torch.
import os
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
import torch

if torch.cuda.is_available():
    DEVICE = 'cuda'
else:
    DEVICE = 'cpu'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUPERSLO_CKPT = os.path.join(BASE_DIR, 'models', 'SuperSloMo.ckpt')
