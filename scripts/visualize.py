import logging
import os

import hydra
import numpy as np
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

import event_library as el
import event_library.representations as representations

# A logger for this file
log = logging.getLogger(__name__)


@hydra.main(config_path="../confs", config_name="visualize.yaml")
def main(cfg: DictConfig):
    log.info(OmegaConf.to_yaml(cfg))
    file_path = cfg.file_path
    if file_path is None:
        log.error("Please provide an input_file")
        return

    log.info(f"Visualizing {file_path}")
    representation = representations.get_representation(cfg.representation.type)
    frame = np.load(file_path, allow_pickle=True)
    representation.display(frame)


if __name__ == "__main__":
    main()
