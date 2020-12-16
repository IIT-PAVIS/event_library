# PACKAGE for camera_stream

## Install

### Using conda for dependencies
```
conda env create -f env.yml
conda activate eventcamera
python -m pip install .
```

### Otherwise, with ubuntu
```
sudo apt-get update
sudo apt-get install libturbojpeg
python -m pip install .
```
## Usage in python
How to use the client in your code.

1. Define a \callback\ that processes the information. Callback fucntion
receives the accumulate event frames and some metadata: 
- min\_ts
- max\_ts
- events
- amplification
- length

```
def toy_callback(self, image, min_ts, max_ts, events, amplification, length):
    self.stop_time = int(round(time.time() * 1000))
    self.accumulation_bytes += lenght
     if (self.stop_time - self.start_time) >= 1000:
        print("Bitrate: {0} Kb/s, Framerate: {1} fps"
            .format((self.accumulation_bytes * 8/1000), self.frames))
```

2. Declare the Mjpeg connector with HTTP\_SOURCE 
```
sc = MjpegConnector(HTTP_SOURCE, CALLBACK)
# Start decoder thread
sc.start()

```

## CLI
For currently running event-camera, use 'http://10.245.83.34:5005'
```
stream_camera --source {SOURCE}
```
