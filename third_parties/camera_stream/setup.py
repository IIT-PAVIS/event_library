"""
My package version of G. Bailo event_camera stream

"""

import setuptools

setuptools.setup(
    name="event_camera_stream",
    version="0.1",
    author="Gian Luca Bailo",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["stream_camera = event_camera_stream:main"]},
    install_requires=["opencv-python", "pyturboJpeg", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: Linux",
    ],
    python_requires=">=3.8",
)
