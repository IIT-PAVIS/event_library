# event-library
Library for event-based vision

## Setup
Clone the repo:

`git clone https://gitlab.iit.it/gscarpellini/event-library`

Install event_library:
```
python -m pip install .
```

## Contributing
If you want to contribute to `event-library`, we suggest to create a virtualenv first. You can use `pipenv` for that. 
```
git clone https://gitlab.iit.it/gscarpellini/event-library
cd event-library
pipenv install
pre-commit install
```

## Generator

### Example: conversion from `avi` files to `events`
```
python scripts/generate.py input_dir={INPUT_DIR} output_dir={OUTPUT_DIR}
upsample=true extract=true emulate=true representation=voxel  show_debug_images=2

```

Tree:
```bash
+-- inputdir
|	+-- videodir1
|
+-- outputdir
|   +-- videodir1
|     +-- part_0
```

### Example: conversion from `png` files to `events`
```
python scripts/generate.py frames_dir={FRAME_VIDEO_DIR} output_dir={OUTPUT_DIR}
upsample=true extract=false emulate=true representation=voxel  show_debug_images=2
```

Each video has a `imgs` directory, where you put the set of frames. Create a
`fps.txt` file in each video directory where you specify the
frame-rate of the video as a single integer number (e.g., 30)

Tree:
```bash
+-- inputdir
|     +-- videodir1
|         +-- imgs
|         +-- fps.txt
+-- outputdir
|     +-- videodir1
|         +-- part_0
```

### Parameters

Representation:
- voxelgrid
- constant-count
- raw

`extract`: if true, extract frames from `avi` files. To provide frames instead of
videos, set 'frame_dir' instead

`upsample`: if true, upsample frames to higher fps using SuperSloMo model

`emulate`: if true, create output events files as `npy` using `representation` stretegy
