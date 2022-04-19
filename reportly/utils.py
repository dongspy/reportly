"""
reportly utils
"""

import base64
import io
import os
import pathlib

__author__ = "dongspy"
__email__ = "lipidong@126.com"


def include_file(
    name, fdir=os.path.join(pathlib.Path(__file__).parents[1], "template"), b64=False
):
    """convert the file, especially the image file, to data:image/png;base64.
    Mainly used in the jinja template

    Parameters
    ----------
    name : str
        The file name
    fdir : str
        The file directory
    b64 : bool
        wheather to deode("utf-8")

    Returns
    -------
    str : data:image
    """
    try:
        if fdir is None:
            fdir = ""
        if b64:
            with io.open(os.path.join(fdir, name), "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            with io.open(os.path.join(fdir, name), "r", encoding="utf-8") as f:
                return f.read()
    except (OSError, IOError) as e:
        raise IOError("Could not include file '{}': {}".format(name, e))


def file2data(filename, b64=True):
    """convert the file, especially the image file, to data:image/png;base64

    Parameters
    ----------
    filename : str
        The file directory
    b64 : bool, default=True
        wheather to deode("utf-8")

    Returns
    -------
    str : data:image
    """
    if b64:
        with io.open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    else:
        with io.open(filename, "r", encoding="utf-8") as f:
            return f.read()
