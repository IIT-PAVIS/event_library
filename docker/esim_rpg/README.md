# ESIM_RPG docker images

## Instructions
### Pull
`docker pull gianscarpe/esim_rpg:latest`

### Launch the image
```
nvidia-docker run -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics -v /tmp/.X11-unix:/tmp/.X11-unix --name esim_rpg_docker -ti --rm -e DISPLAY -e QT_X1_NO_MITSHM=1 esim_rpg:v2 /bin/bash
```
From now on, you are in the `bash` shell of the image. The image is running
`ubuntu16.04` and has support for `ROS`, `catlin`, and `rpg_esim` simulator.
To activate this environment, call `ssim` from command line.

You can manage multiple parallel bash sessions using `tmux`

### Notes
- You can add other shared directories (called `volumes`) using `-v PATH/TO/LOCAL/DIR:/PATH/TO/CONTAINER/DIR`
- `nvidia-docker` is necessary to use `nvidia` drivers and capabilities
- `x11` parameters are necessary for visualization
  - User is called `esim_user`, its home is at `/home/esim_user`. Password is `esim_user`


## Usage case: simulate events from a `.jpg` image and save them as `.txt`
Following commands generate events from a single image. More at
   [https://github.com/uzh-rpg/rpg_esim/wiki/Planar-Renderer](esim_rpg wiki)
   ```
   ssim
   roscd esim_ros
   rosrun esim_ros esim_node --flagfile=cfg/example.conf --renderer_texture={IMG_PATH} --path_to_events_text_file={OUTPUT_PATH}
   ```
   
   You can write a script to load `.txt` events, generate event-representations,
   and display them:
   ```python
   import event_library
   import event_library.utils as utils
   
   path = "./events_out.txt"
   events = utils.load_from_file(path, num_events=10000)
   representation = event_library.representation.get_generator("constant-count")
   for frame in representation.get_generator(frame_size=(500, 500), num_events=1000)(events):
	   representation.display(frame)
   ```
### Parameters 
	`--renderer_extend_border`: `0` to disable, `1` to enable
	More at https://github.com/uzh-rpg/rpg_esim/issues/45
