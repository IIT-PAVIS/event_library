import logging
import os

import hydra
import numpy as np
from esim_py_upsampling import upsample
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

import event_library as el
import event_library.representations as representations
from event_library.generator import SimulatorWrapper, find_best_events_parameters

# A logger for this file
log = logging.getLogger(__name__)


def _do_upsample(tmp_frames_dir, tmp_upsample_dir, output_size, n_threads=32):
    log.info("Upsampling")
    upsample.upsample(
        tmp_frames_dir, tmp_upsample_dir, n_threads=n_threads, output_size=output_size,
    )
    log.info("Upsampling completed")


def _do_simulation(cfg, tmp_upsample_dir, base_output_dir):
    simulator = hydra.utils.instantiate(cfg.vid2e)
    video_dirs = []
    for root, dirs, _ in os.walk(tmp_upsample_dir):
        for d in dirs:
            if d == "imgs":
                video_dirs.append(root)

    for input_video_dir in tqdm(video_dirs):

        video_struct = os.path.relpath(input_video_dir, tmp_upsample_dir)
        output_dir = os.path.join(base_output_dir, video_struct)

        try:
            simulator.set_input_dir(input_video_dir)
            _generate_frames_and_save(cfg, simulator, output_dir)
        except Exception as ex:
            print(ex)
            log.debug(f"Error with {input_video_dir} {ex}")

    log.info("Simulation end")


def _get_representation_generator_from_cfg(cfg: DictConfig, frame_shape):
    return representations.get_generator(
        cfg.representation.type,
        **{"frame_size": (frame_shape[0], frame_shape[1]), **cfg.representation.args},
    )


def _generate_frames_and_save(
    cfg: DictConfig, simulator: SimulatorWrapper, output_dir: str
):
    os.makedirs(output_dir, exist_ok=True)
    events_frame_index = 0
    hw_properties = el.utils.get_hw_property(cfg.hw_type)
    if simulator.get_frames_dimension() != hw_properties.size:
        raise Exception(
            f'Cannot convert video with different sizes! Size mismatch {simulator.get_frames_dimension()}'
        )

    if len(os.listdir(output_dir)) > 0:
        return

    for events_batch in tqdm(simulator):
        representation_gen = _get_representation_generator_from_cfg(
            cfg, hw_properties.size
        )

        for frame in representation_gen(events_batch):
            np.save(
                os.path.join(output_dir, f"frame{events_frame_index:07d}.npy"), frame
            )
            events_frame_index += 1


def _do_search(cfg, tmp_upsample_dir):
    video_dirs = []
    for root, dirs, _ in os.walk(tmp_upsample_dir):
        for d in dirs:
            if d == "imgs":
                video_dirs.append(root)

    simulator = hydra.utils.instantiate(cfg.vid2e)
    simulator.set_input_dir(video_dirs[0])
    representation_gen = _get_representation_generator_from_cfg(
        cfg, simulator.get_frames_dimension()
    )
    best = find_best_events_parameters(video_dirs, representation_gen)

    log.info(f"Best parameters found! {best}")


@hydra.main(config_path="confs", config_name="generate.yaml")
def main(cfg: DictConfig):

    log.info(OmegaConf.to_yaml(cfg))
    tmp_dir = cfg.tmp_dir
    base_output_dir = cfg.output_dir

    do_upsample = cfg.upsample
    do_emulation = cfg.emulate
    do_search = cfg.search

    os.makedirs(tmp_dir, exist_ok=True)
    hw_properties = el.utils.get_hw_property(cfg.hw_type)

    log.info(hw_properties)

    if cfg.frames_dir is None:
        tmp_frames_dir = os.path.join(tmp_dir, "frames")
    else:
        tmp_frames_dir = cfg.frames_dir

    if cfg.upsample_dir is None:
        tmp_upsample_dir = os.path.join(tmp_dir, "upsample")
    else:
        tmp_upsample_dir = cfg.upsample_dir

    if do_upsample:
        _do_upsample(tmp_frames_dir, tmp_upsample_dir, output_size=hw_properties.size)

    if do_search:
        _do_search(cfg, tmp_upsample_dir)

    if do_emulation:
        _do_simulation(cfg, tmp_upsample_dir, base_output_dir)


if __name__ == "__main__":
    main()
