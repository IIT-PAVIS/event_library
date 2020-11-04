import os
from tqdm import tqdm
import hydra
from omegaconf import DictConfig

from event_library.generator.upsample import upsample

import logging

# A logger for this file
log = logging.getLogger(__name__)


def _do_extraction(cfg, input_dir, tmp_frames_dir):
    extractor = hydra.utils.instantiate(cfg.extractor)
    log.info("Extract RGB frames from videos")
    extractor.extract_frames(input_dir, tmp_frames_dir)

    log.info("Extraction completed")


def _do_upsample(tmp_frames_dir, tmp_upsample_dir):
    log.info("Upsampling")
    upsample(tmp_frames_dir, tmp_upsample_dir)
    log.info("Upsampling completed")


def _do_simulation(cfg, tmp_upsample_dir, base_output_dir):
    simulator = hydra.utils.instantiate(cfg.vid2e)
    video_dirs = []
    for root, dirs, _ in os.walk(tmp_upsample_dir):
        for d in dirs:
            if d == 'imgs':
                video_dirs.append(root)

    with_errors = []
    for input_video_dir in tqdm(video_dirs):
        video_struct = os.path.relpath(input_video_dir, tmp_upsample_dir)
        output_dir = os.path.join(base_output_dir, video_struct)
        try:
            representation = hydra.utils.instantiate(cfg.representation)
            os.makedirs(output_dir, exist_ok=True)
            simulator.generate(input_video_dir, output_dir, representation)
        except Exception as ex:
            print(f"Error with {input_video_dir} {ex}")
            with_errors.append(input_video_dir)

    log.debug(with_errors)
    log.info("Simulation end")


@hydra.main(config_path='../confs', config_name='generate.yaml')
def main(cfg: DictConfig):
    print(cfg.pretty())

    input_dir = cfg.input_dir
    tmp_dir = cfg.tmp_dir
    base_output_dir = cfg.output_dir

    do_extract = cfg.extract
    do_upsample = cfg.upsample
    do_emulation = cfg.emulate

    if input_dir is None and base_output_dir is None:
        log.error("Specify INPUT! and OUTPUT")

    if cfg.frames_dir is None:
        tmp_frames_dir = os.path.join(tmp_dir, "frames")
    else:
        tmp_frames_dir = cfg.frames_dir

    if cfg.upsample_dir is None:
        tmp_upsample_dir = os.path.join(tmp_dir, "upsample")
    else:
        tmp_upsample_dir = cfg.upsample_dir

    if do_extract:
        _do_extraction(cfg, input_dir, tmp_frames_dir)

    if do_upsample:
        _do_upsample(tmp_frames_dir, tmp_upsample_dir)

    if do_emulation:
        _do_simulation(cfg, tmp_upsample_dir, base_output_dir)


if __name__ == '__main__':
    main()
