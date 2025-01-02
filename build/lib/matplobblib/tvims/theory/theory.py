from ...forall import *
import importlib.resources as pkg_resources
from PIL import Image
import IPython.display as display

THEORY = []

def get_png_files_from_subdir(subdir):
    """
    Returns a list of file paths to PNG files in the given subdirectory.
    """
    package = f"matplobblib.tvims.theory.pdfs.{subdir}"
    png_files = []
    try:
        for resource in pkg_resources.contents(package):
            if resource.endswith(".png"):
                with pkg_resources.path(package, resource) as file_path:
                    png_files.append(file_path)
    except Exception as e:
        print(f"Error accessing PNG files in {subdir}: {e}")
    return png_files

def display_png_files_from_subdir(subdir):
    """
    Displays PNG files from a given subdirectory in the Jupyter notebook.
    """
    png_files = get_png_files_from_subdir(subdir)
    for file in png_files:
        img = Image.open(file)
        display.display(img)

# Dynamically create functions for each subdirectory
def create_subdir_function(subdir):
    """
    Dynamically creates a function to display PNG files from a given subdirectory.
    The function is named display_png_files_{subdir}.
    """
    global THEORY
    # Define the function dynamically
    def display_function():
        """
        Automatically generated function to display PNG files.
        """
        display_png_files_from_subdir(subdir)
    
    # Set the function name dynamically
    display_function.__name__ = f"display_{subdir}"
    
    # Add a descriptive docstring
    display_function.__doc__ = (
        f"Вывести все страницы из файла с теорией '{subdir.replace('_','-')}'.\n"
        f"Эта функция сгенерирована автоматически из файла '{subdir.replace('_','-')+'.pdf'}' "
        f"из внутрибиблиотечного каталога файлов с теорией."
    )
    
    # Add the function to the global namespace
    globals()[display_function.__name__] = display_function
    THEORY.append(display_function)

def list_subdirectories():
    """
    List subdirectories in the 'matplobblib.tvims.theory.pdfs' package.
    """
    package = "matplobblib.tvims.theory.pdfs"
    subdirs = []

    # Iterate through items in the package directory
    package_path = pkg_resources.files(package)
    for item in package_path.iterdir():
        if item.is_dir():  # Check if the item is a directory
            subdirs.append(item.name)
    
    return subdirs

# Get subdirectories dynamically
subdirs = list_subdirectories()


# Create functions for each subdirectory dynamically
for subdir in subdirs:
    create_subdir_function(subdir)
