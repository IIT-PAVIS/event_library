##################################################
## mjpeg_connector.py
## Accumulation image receiver/decoder
##################################################
## Author: Gian Luca Bailo (IIT)
## Email: gian.bailo@iit.it
##################################################

import argparse
import datetime
import os
import queue
import signal
import sys
import threading
import time
from urllib.parse import urlparse

import cv2
import numpy as np
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from turbojpeg import TJFLAG_PROGRESSIVE, TJPF_GRAY, TJSAMP_GRAY, TurboJPEG


class MjpegConnector(threading.Thread):
    """Connect to mjpeg source, decoding mjpeg with turbojpeg.
    Read metadata and decode image, call a function to pass these data
    """

    def __init__(self, address, callback):
        threading.Thread.__init__(self)
        self.callback = callback

        # set params
        self.address = address  # Remote address

        # Interface queue
        self.stream_queue = queue.Queue(2)

        # Read until running is true
        self.running = True

        # turbo jpeg initialization
        self.jpeg = TurboJPEG()

        # get username and password from address
        parsed = urlparse(self.address)

        self.username = parsed.username
        self.password = parsed.password

    def connect(self):
        try:
            # Connect to remote source as streaming request, no verify https, auth as Digest
            self.stream = requests.get(
                self.address,
                stream=True,
                verify=False,
                auth=HTTPDigestAuth(self.username, self.password),
            )

            # Check response error
            self.stream.raise_for_status()

            # Start acquire
            threading.Thread(target=self.video_handler).start()

            return True

        # If connection is ok but there is an http error
        except requests.exceptions.HTTPError as e:
            print("Status Error: {0}".format(e), flush=True)
            return False

        # If connection is not possibile
        except requests.exceptions.RequestException as e:
            print("Connection Error: {0}".format(e), flush=True)
            return False

    def disconnect(self):
        self.running = False

    def readline(self):
        """Read text line from remote server

        Returns:
            string: remote string
        """
        string_buffer = bytes()

        while self.running:
            # Read one byte
            string_buffer += self.stream.raw.read(1)

            # If typical http eol founded return string
            if b"\r\n" in string_buffer:
                return string_buffer.decode("ascii")

    def video_handler(self):
        """Read data from socket using requests module, decode multipart metadata, put image and data over
        a syncronized queue, no waiting
        """
        while self.run:
            # Receive boundary
            self.readline()

            # Receive content type
            self.readline()

            # Receive minimal timestamp
            min_ts = int(self.readline().split(" ")[1])

            # Receive maximum timestamp
            max_ts = int(self.readline().split(" ")[1])

            # Receive accumulation image event number
            events = int(self.readline().split(" ")[1])

            # Receive accumulation image event number
            amplification = int(self.readline().split(" ")[1])

            # Receive Content-Length
            image_length = int(self.readline().split(" ")[1])

            # Receive blank
            self.readline()

            # Read data block
            image_buffer = self.stream.raw.read(image_length)

            if len(image_buffer) != image_length:
                print("Error: reading data from remote source", flush=True)
                break

            # Check if there is jpeg starting code
            position = image_buffer.find(b"\xff\xd8")

            # If jpeg starting code is founded in frame
            if position != -1:
                # Put encoded image into buffer
                try:
                    self.stream_queue.put(
                        [
                            image_buffer,
                            min_ts,
                            max_ts,
                            events,
                            amplification,
                            image_length,
                        ],
                        False,
                        0,
                    )
                except queue.Full:
                    pass

            # Receive blank
            self.readline()

    def run(self):
        """Decoding thread, receive from syncronized queue and decode as fast as possible. decoded image
        and metadata is passed to callback
        """
        while running:
            try:
                block = self.stream_queue.get(True, 5)
            except queue.Empty:
                return None

            self.callback(
                self.jpeg.decode(block[0]),
                block[1],
                block[2],
                block[3],
                block[4],
                block[5],
                self,
            )  # 1.5x faster than ffmpeg embedded into opencv


class RenderAccumulation:
    """Render accumulation image and print some statistics"""

    def __init__(self):
        self.start_time = int(round(time.time() * 1000))
        self.stop_time = int(round(time.time() * 1000))
        self.accumulation_bytes = 0
        self.frames = 0

    def callback(self, image, min_ts, max_ts, events, amplification, lenght, client):
        self.stop_time = int(round(time.time() * 1000))
        self.accumulation_bytes += lenght

        if (self.stop_time - self.start_time) >= 1000:
            print(
                "Bitrate: {0} Kb/s, Framerate: {1} fps".format(
                    (self.accumulation_bytes * 8 / 1000), self.frames
                )
            )

            self.accumulation_bytes = 0
            self.frames = 0
            self.start_time = int(round(time.time() * 1000))
            self.min_size = 0
            self.max_size = 0

        # Show accumulation image GRAY
        cv2.imshow("Receiver image", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            client.disconnect()

        self.frames += 1


running = True


def exit_gracefully(sc, signum, frame):
    global running

    # Disconnect
    sc.disconnect()
    running = False
    __import__("pdb").set_trace()

    # Wait one second
    time.sleep(1)
    sys.exit(0)


def parse_args():
    # Parse input
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", default="", help="config file")

    args = parser.parse_known_args()
    return args


def main():
    args = parse_args()

    render_accumulation = RenderAccumulation()

    # Create SourceConnector object
    sc = MjpegConnector(args[0].source, render_accumulation.callback)

    # Connect to remote source
    if not sc.connect():
        sys.exit(0)

    # Intercept signals
    signal.signal(
        signal.SIGINT, lambda signum, frame: exit_gracefully(sc, signum, frame)
    )
    signal.signal(
        signal.SIGTERM, lambda signum, frame: exit_gracefully(sc, signum, frame)
    )

    # Start decoder thread

    sc.start()

    while sc.join():
        pass
    # Disconenct from source
    sc.disconnect()


if __name__ == "__main__":
    main()
