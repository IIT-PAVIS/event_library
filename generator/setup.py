import setuptools

setuptools.setup(
    name="event_library",
    version="0.1",
    author="gianscarpe",
    author_email="gianluca@scarpellini.dev",
    description="Event-camera library",
    url="https://github.com/gianscarpe/event_library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
