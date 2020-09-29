# event_library
Event library

## Start
Clone the repo:

`git clone https://github.com/gianscarpe/event_library.git`

Create conda env:
`conda env create -f environment.yml`

Install event_library:
```
python -m pip install .
```

## Generator

### Example: conversion from `avi` files to `events`
```
python scripts/generate.py input_dir={INPUT_DIR} output_dir={OUTPUT_DIR}
upsample=true extract=true emulate=true representation=voxel  show_debug_images=2

```

Tree:
.
+-- inputdir
|	+-- videodir1
|
+-- outputdir
|   +-- videodir1
|     +-- part_0


### Example: conversion from `png` files to `events`
```
python scripts/generate.py frames_dir={FRAME_VIDEO_DIR} output_dir={OUTPUT_DIR}
upsample=true extract=false emulate=true representation=voxel  show_debug_images=2
```

Each video has a `imgs` directory, where you put the set of frames. Create a
`fps.txt` file in each video directory where you specify the
frame-rate of the video as a single integer number (e.g., 30)

Tree:
.
+-- inputdir
|     +-- videodir1
|         +-- imgs
|         +-- fps.txt
+-- outputdir
|     +-- videodir1
|         +-- part_0


### Parameters

Representation:
- voxelgrid
- constant-count
- raw

`extract`: if true, extract frames from `avi` files. To provide frames instead of
videos, set 'frame_dir' instead

`upsample`: if true, upsample frames to higher fps using SuperSloMo model

`emulate`: if true, create output events files as `npy` using `representation` stretegy

`show_debug_images`: n of image to show for debug at the end of the script
