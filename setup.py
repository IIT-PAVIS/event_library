import setuptools

setuptools.setup(
    name="event_library",
    version="0.1",
    author="gianscarpe",
    author_email="gianluca@scarpellini.dev",
    description="Event library",
    url="https://github.com/gianscarpe/event_library",
    entry_points = {
        'console_scripts': ['recycle_for_event_camera = event_library.generator:main']
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python',
        'torch',
        'torchvision',
        'hydra-core'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)
