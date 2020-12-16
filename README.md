# event-library
Library for event-based vision

## Setup
Clone the repo:

`git clone https://gitlab.iit.it/gscarpellini/event-library`

Install event_library:
```
python setup.py install
```

## Contributing
If you want to contribute to `event-library`, we suggest to create a virtualenv first. You can use `pipenv` for that. 
```
git clone https://gitlab.iit.it/gscarpellini/event-library
cd event-library
pipenv install
pre-commit install
```

### Basic guidlines:
1. Start opening an issue on gitlab assessing the feature you're going to implement
or the bug you want to fix. 
2. Fork the project and start coding1! :fire:
3. We use `pre-commit` to check that code respect `PEP8` and good practices
4. Submit your `pull-request` to the main repository :)

### Building docs
```
python -m pip install .
python -m pip install -r requirements/docs.txt
sphinx-build -b html docs/source docs/build
```

## Tools
### Generator

#### Example: conversion from `avi` files to `events`
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

#### Example: conversion from `png` files to `events`
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

### Visualization
You can visualize a `npy` events files using the `visualize` script:
```
python scripts/visualize.py file_path={YOUR_FILE.npy} representation={REPRESENTATION}
```
### Parameters and help

You can obtain a tool help using `python {TOOL}.py --help`

#### Representation:
- voxelgrid
- constant-count
- raw

`extract`: if true, extract frames from `avi` files. To provide frames instead of
videos, set 'frame_dir' instead

`upsample`: if true, upsample frames to higher fps using SuperSloMo model

`emulate`: if true, create output events files as `npy` using `representation` stretegy
