import glob
import os
import re
import subprocess
import sys

import setuptools


def get_info():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        version = re.search(
            r'^__version__\s*=\s*"(.*)"',
            open("event_library/__init__.py").read(),
            re.MULTILINE,
        ).group(1)
    return long_description, version


long_description, version = get_info()


def install_subs():
    for sub_mod in glob.glob("./third_parties/*.whl"):
        print(f"Installing {sub_mod}")
        subprocess.call([sys.executable, "-m", "pip", "install", sub_mod])
    for sub_mod in glob.glob("./third_parties/esim_py_upsampling"):
        submod_setup_path = sub_mod + "/setup.py"
        if os.path.exists(submod_setup_path):
            # Run submodule setup.py file
            print(f"Installing {sub_mod}")
            subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    os.getcwd() + "/" + sub_mod + "/",
                ]
            )


long_description, version = get_info()

setuptools.setup(
    name="event_library",
    version="0.2",
    author="Gianluca Scarpellini",
    author_email="gianluca.scarpellini@iit.it",
    description="Event library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gianscarpe/event_library",
    packages=setuptools.find_packages(exclude=("tests", "scripts")),
    install_requires=[
        "opencv-python",
        "torch",
        "torchvision",
        "hydra-core",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: Linux",
    ],
    python_requires=">=3.8",
)

install_subs()
