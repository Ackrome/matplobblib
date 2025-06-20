import requests
from io import BytesIO
from PIL import Image
import IPython.display as display
from ...forall import *

BASE_API_URL = r"https://api.github.com/repos/Ackrome/matplobblib/contents"
BASE_GET_URL = r"https://raw.githubusercontent.com/Ackrome/matplobblib/master"

# Список для хранения динамически созданных функций отображения теории.
####################################################################################################
def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Проверяет наличие интернет-соединения.
    """
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        return False
####################################################################################################
THEORY = []
####################################################################################################
def list_subdirectories(url=BASE_API_URL):
    """
    Получает список подкаталогов из репозитория GitHub.
    """
    if not check_internet_connection():
        print("Ошибка: Для выполнения этой функции требуется интернет-соединение.")
        return []
    
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        return [item['name'] for item in contents if item['type'] == 'dir']
    else:
        print(f"Ошибка при получении подпапок: {response.status_code}")
        return []
####################################################################################################
def get_exact_format_files_from_subdir(subdir,url=BASE_API_URL,exact_format='png'):
    """
    Получает список URL-адресов .`exact_format`-файлов из указанного подкаталога в репозитории GitHub.
    """
    if not check_internet_connection():
        print("Ошибка: Для выполнения этой функции требуется интернет-соединение.")
        return []
    url = url +f"/{subdir}"
    
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        exact_format_files = [item['name'] for item in contents if item['name'].endswith('.'+exact_format)]
        return [BASE_GET_URL + f"/{subdir}/{file}" for file in exact_format_files]
    else:
        print(f"Ошибка доступа к {subdir}: {response.status_code}")
        return []
####################################################################################################
def display_exact_format_files_from_subdir(subdir,url=BASE_API_URL,exact_format='png'):
    """
    Отображает exact_format-файлы из указанного подкаталога.
    """
    if not check_internet_connection():
        print("Ошибка: Для выполнения этой функции требуется интернет-соединение.")
        return
    exact_format_urls = get_exact_format_files_from_subdir(subdir,url,exact_format)
    if exact_format == 'png':
        
        for url in exact_format_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                display.display(img)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка загрузки {url}: {e}")
                
    if exact_format == 'md':
        for url in exact_format_urls:
            response = requests.get(url)
            if response.status_code == 200:
                display.display(display.Markdown(response.text))
            else:
                print(f"Ошибка загрузки файла: {response.status_code}")    
####################################################################################################
# Динамическое создание функций для каждого подкаталога
def create_subdir_function(subdir,url=BASE_API_URL,exact_format='png'):
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
        display_exact_format_files_from_subdir(subdir,url,exact_format)
    
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
####################################################################################################   
####################################################################################################
# По идее в pdfs должны лежать только файлы с матстатом, поэтому не стоит сильно надеяться на автосоздание этого всего
# Динамическое получение списка подкаталогов
url = BASE_API_URL+"/theory_files/pdfs"
subdirs_disp = list_subdirectories(url)
# Динамическое создание функций для каждого подкаталога
for subdir in subdirs_disp:
    if subdir.startswith('MS'):
        create_subdir_function(subdir, url)