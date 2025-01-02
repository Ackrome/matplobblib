from ...forall import *
import importlib.resources as pkg_resources
import os

def get_png_files():
    """
    Returns a list of paths to PNG files in the MS-11-12 directory.
    """
    package = "matplobblib.tvims.theory.pdfs.MS-11-12"
    png_files = []
    try:
        for resource in pkg_resources.contents(package):
            if resource.endswith(".png"):
                path = pkg_resources.path(package, resource)
                png_files.append(str(path))
    except Exception as e:
        print(f"Error accessing PNG files: {e}")
    return png_files