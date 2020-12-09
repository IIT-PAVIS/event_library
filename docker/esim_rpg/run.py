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

cGianluca Scarpellini - gianluca.scarpellini@iit.it - 2020
"""
import argparse
import logging
import subprocess
import threading
from pathlib import Path
import os
logging.basicConfig(level=logging.DEBUG)


def _get_command(
        container_name: str, input_name: str, conf_file: str, out_path: str
) -> str:

    parameters = f"--flagfile=/home/esim_user/confs/{conf_file} --renderer_texture=/home/esim_user/data/{input_name} --calib_filename=/home/esim_user/confs/pinhole_mono_nodistort.yaml --path_to_events_text_file={out_path}"

    source_esim_cmd = "source ~/sim_ws/devel/setup.bash; roscd esim_ros"    
    rosrun_cmd = (
        f"{source_esim_cmd}; rosrun esim_ros esim_node {parameters}"
    )

    docker_cmd = f'docker exec -d {container_name} bash -c "{rosrun_cmd}"'

    return docker_cmd


def _run_cmd(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")[:-1]


def _clean_existing_containers():
    cmd = "docker container kill $(docker ps -aq)"
    return _run_cmd(cmd)


def _run_container(input_dir: str, out_dir: str) -> str:
    setup_cmd = '"source ~/setupeventsim.sh; roscore"'
    v_flags = f"-v $(pwd)/confs:/home/esim_user/confs -v {out_dir}:/home/esim_user/out -v {input_dir}:/home/esim_user/data"    
    docker_cmd = f'docker run --rm -it -d {v_flags} --user esim_user $(docker build                   -q .) bash -c {setup_cmd}'
    return _run_cmd(docker_cmd)


def _spawn_processing_thread(
    thread_id: int, img_names: list, input_dir: str, out_dir: str, conf_file: str
) -> None:
    logging.info(f"Thread {thread_id} computing ...")

    docker_img = _run_container(input_dir, out_dir)

    for img_name in img_names:
        out_name = img_name.split(".")[0] + ".txt"
        out_path = f"/home/esim_user/out/{out_name}"
        if os.path.exists(os.path.join(out_dir, out_name)):
            continue
        try:
            cmd = _get_command(docker_img, img_name, conf_file, out_path)
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output, error = process.communicate()
            logging.debug(output)
            logging.error(error)
        except Exception as ex:
            logging.error(f"Error: {ex}")

    logging.info(f"Thread {thread_id} Done!")
    return None


def main():

    parser = argparse.ArgumentParser(
        description="Script for launch esim_rpg simulator."
    )
    parser.add_argument("--img_dir", help="Directory of input images")
    parser.add_argument("--img_names", nargs="+", help="Names of input images")
    parser.add_argument("--out_dir", help="output dir. Please set ownership")
    parser.add_argument("--sim_duration", type=float, help="Duration of the sim.")
    parser.add_argument(
        "--conf_file", default="config.conf", help="General configuraion file"
    )
    parser.add_argument(
        "--spawn_n", default=1, type=int, help="Number of thread to spawn"
    )

    args = parser.parse_args()
    img_names = sorted(args.img_names)[::-1]
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
