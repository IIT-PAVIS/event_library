"""
Event-library
"""


__author__ = "gscarpellini"
__version__ = "0.3"
__author_email__ = "gianluca.scarpellini@iit.it"
__license__ = "GPLv3"
__copyright__ = f"Copyright (c) 2020 under {__license__}, {__author__}."

try:
    # This variable is injected in the __builtins__ by the build
    # process.
    __EL_SETUP__  # type: ignore
except NameError:
    __EL_SETUP__ = False

if __EL_SETUP__:
    import sys  # pragma: no-cover

    sys.stdout.write(
        f"Partial import of `{__name__}` during the build process.\n"
    )  # pragma: no-cover
    # We are not importing the rest of the lightning during the build process, as it may not be compiled yet
else:
    import torch

    if torch.cuda.is_available():
        DEVICE = "cuda"
    else:
        DEVICE = "cpu"
