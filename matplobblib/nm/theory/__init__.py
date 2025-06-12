import requests
from io import BytesIO
from PIL import Image
import IPython.display as display
from ...forall import *
# Список для хранения динамически созданных функций отображения теории.
THEORY = []

def list_subdirectories():
    """
    Получает список подкаталогов из репозитория GitHub, имена которых начинаются с 'NM'.
    """
    url = "https://api.github.com/repos/Ackrome/matplobblib/contents/pdfs"
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        return [item['name'] for item in contents if item['type'] == 'dir' and item['name'].startswith('NM')]
    else:
        print(f"Ошибка при получении подпапок: {response.status_code}")
        return []

def get_png_files_from_subdir(subdir):
    """
    Получает список URL-адресов PNG-файлов из указанного подкаталога в репозитории GitHub.
    """
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
    """
    Отображает PNG-файлы из указанного подкаталога.
    """
    png_urls = get_png_files_from_subdir(subdir)
    for url in png_urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            display.display(img)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки {url}: {e}")

# Динамическое создание функций для каждого подкаталога
def create_subdir_function(subdir):
    """
    Динамически создает функцию для отображения PNG-файлов из заданного подкаталога.
    Функция именуется display_{subdir}.
    """
    global THEORY
    # Динамическое определение функции
    def display_function():
        """
        Автоматически сгенерированная функция для отображения PNG-файлов.
        """
        display_png_files_from_subdir(subdir)
    
    # Динамическое присвоение имени функции
    display_function.__name__ = f"display_{subdir}"
    
    # Добавление описательной строки документации
    display_function.__doc__ = (
        f"Вывести все страницы из файла с теорией '{subdir.replace('_','-')}'.\n"
        f"Эта функция сгенерирована автоматически из файла '{subdir.replace('_','-')+'.pdf'}' "
        f"из внутрибиблиотечного каталога файлов с теорией."
    )
    
    # Добавление функции в глобальное пространство имен
    globals()[display_function.__name__] = display_function
    THEORY.append(display_function)

# Динамическое получение списка подкаталогов
subdirs = list_subdirectories()
# Динамическое создание функций для каждого подкаталога
for subdir in subdirs:
    create_subdir_function(subdir)
