"""
This script provides a easy-to-use API for esim_rpg simulator. ESIM_RPG provides
a toolbox for converting a standard image to a sequence of simulated events. It
does so by simulating homographic movements of the camera.

This scripts uses the attached Dockerfile to launch esim_rpg and produce a
`.txt` output of ordered events

Pleas note: in order to give writing access to docker, you need to set an `output` directory
with low permission. You can do this with:
'''
mkdir output_dir
chown -R $(whoami):1000 output_dir
'''

Gianluca Scarpellini - gianluca.scarpellini@iit.it - 2020
"""
import argparse
import logging
import subprocess
import threading
from pathlib import Path

logging.basicConfig(filename="logging.txt", level=logging.DEBUG)


def _get_command(img_name: str, input_dir: str, out_dir: str, conf_file: str) -> str:
    out_name = img_name.split(".")[0] + ".txt"
    setup_cmd = "source ~/setupeventsim.sh; roscore"
    source_esim_cmd = "source ~/sim_ws/devel/setup.bash; roscd esim_ros"
    parameters = f"--flagfile=/home/esim_user/confs/{conf_file} --renderer_texture=/home/esim_user/data/{img_name} --path_to_events_text_file=/home/esim_user/out/{out_name}"

    rosrun_cmd = (
        f"{setup_cmd} & ({source_esim_cmd}; rosrun esim_ros esim_node {parameters})"
    )
    v_flags = f"-v $(pwd)/confs:/home/esim_user/confs -v {out_dir}:/home/esim_user/out -v {input_dir}:/home/esim_user/data"

    docker_cmd = f'docker run --rm -it {v_flags} --user esim_user $(docker build -q .) bash -c "{rosrun_cmd}"'

    return docker_cmd


def _spawn_processing_thread(
    thread_id: int, img_names: list, input_dir: str, out_dir: str, conf_file: str
) -> None:
    logging.info(f"Thread {thread_id} computing ...")
    for img_name in img_names:
        cmd = _get_command(img_name, input_dir, out_dir, conf_file)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output, error = process.communicate()
        logging.debug(output)
        logging.debug(error)

    logging.debug(f"Thread {thread_id} Done!")
    return None


def main():

    parser = argparse.ArgumentParser(
        description="Script for launch esim_rpg simulator."
    )
    parser.add_argument("--img_dir", help="Directory of input images")
    parser.add_argument("--img_names", nargs="+", help="Names of input images")
    parser.add_argument("--out_dir", help="output dir. Please set ownership")
    parser.add_argument(
        "--conf_file", default="config.conf", help="General configuraion file"
    )
    parser.add_argument(
        "--spawn_n", default=1, type=int, help="Number of thread to spawn"
    )

    args = parser.parse_args()
    img_names = args.img_names
    input_dir = args.img_dir
    out_dir = args.out_dir
    conf_file = args.conf_file
    spawn_n = args.spawn_n
    logging.info(f"N of images to process:{len(img_names)}")

    images_per_thread = int(len(img_names) / spawn_n)
    for thread_n in range(spawn_n):
        start_i = images_per_thread * thread_n
        end_i = min(len(img_names), start_i + images_per_thread)
        args = (thread_n, img_names[start_i:end_i], input_dir, out_dir, conf_file)
        x = threading.Thread(target=_spawn_processing_thread, args=args)
        x.start()


if __name__ == "__main__":
    main()
