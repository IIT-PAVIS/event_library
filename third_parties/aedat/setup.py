import glob
import os
import re
import subprocess
import sys

import setuptools

setuptools.setup(
    name="aedat_tools",
    version="0.0.1",
    author="Gianluca Scarpellini",
    author_email="gianluca.scarpellini@iit.it",
    description="Event library - aedat tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: Linux",
    ],
    python_requires=">=3.8",
)
