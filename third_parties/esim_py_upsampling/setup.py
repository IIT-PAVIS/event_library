import setuptools

setuptools.setup(
    name="esim_py_upsampling",
    packages=setuptools.find_packages(),
    install_requires=[
        "opencv-python",
        "hydra-core",
        "matplotlib",
        "numpy",
        "torch",
        "torchvision",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: Linux",
    ],
    python_requires=">=3.8",
)
