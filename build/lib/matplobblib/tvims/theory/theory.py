import requests
from io import BytesIO
from PIL import Image
import IPython.display as display
from ...forall import *

THEORY = []

def list_subdirectories():
    url = "https://api.github.com/repos/Ackrome/matplobblib/contents/pdfs"
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        return [item['name'] for item in contents if item['type'] == 'dir']
    else:
        print(f"Ошибка при получении подпапок: {response.status_code}")
        return []

def get_png_files_from_subdir(subdir):
    url = f"https://api.github.com/repos/Ackrome/matplobblib/contents/pdfs/{subdir}"
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        png_files = [item['name'] for item in contents if item['name'].endswith('.png')]
        return [f"https://raw.githubusercontent.com/Ackrome/matplobblib/master/pdfs/{subdir}/{file}" for file in png_files]
    else:
        print(f"Ошибка доступа к {subdir}: {response.status_code}")
        return []

def display_png_files_from_subdir(subdir):
    png_urls = get_png_files_from_subdir(subdir)
    for url in png_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            display.display(img)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки {url}: {e}")

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


# Get subdirectories dynamically
subdirs = list_subdirectories()


# Create functions for each subdirectory dynamically
for subdir in subdirs:
    create_subdir_function(subdir)
