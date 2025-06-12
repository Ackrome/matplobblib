import requests
import importlib.resources
import pathlib
from typing import List, Dict, Set,Optional
from io import BytesIO
from PIL import Image
import IPython.display as display
import webbrowser
from pathlib import Path
from bs4 import BeautifulSoup

from ...forall import *
# Список для хранения динамически созданных функций отображения теории.

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

THEORY = []

def list_subdirectories():
    """
    Получает список подкаталогов из репозитория GitHub, имена которых начинаются с 'NM'.
    """
    if not check_internet_connection():
        print("Ошибка: Для выполнения этой функции требуется интернет-соединение.")
        return []
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
    if not check_internet_connection():
        print("Ошибка: Для выполнения этой функции требуется интернет-соединение.")
        return []
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
    if not check_internet_connection():
        print("Ошибка: Для выполнения этой функции требуется интернет-соединение.")
        return
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
    


def get_all_packaged_html_files(package_data_config: Dict[str, List[str]]) -> List[str]:
    """
    Составляет список имен всех уникальных HTML-файлов, найденных во всех директориях,
    указанных в конфигурации типа package_data, доступных изнутри установленного пакета.
    Возвращаются только имена файлов, а не полные пути.

    Args:
        package_data_config: Словарь, аналогичный параметру `package_data` в setup.py.
                             Ключи - это имена пакетов верхнего уровня (например, 'matplobblib').
                             Значения - это списки строк с путями относительно корня пакета,
                             обычно заканчивающиеся маской, такой как '*.html'.
                             Пример: {'matplobblib': ['matplobblib/nm/theory/htmls/*.html', 'other_data/*.html']}

    Returns:
        Отсортированный список уникальных имен HTML-файлов (например, ['page1.html', 'index.html']).
    """
    all_html_file_names: Set[str] = set()

    for package_name, path_patterns in package_data_config.items():
        try:
            # Получаем Traversable для корня пакета
            package_root_traversable = importlib.resources.files(package_name)
        except (ModuleNotFoundError, TypeError):
            # Пакет не найден или не является валидным контейнером ресурсов
            # Можно добавить логирование предупреждения, если необходимо
            print(f"Предупреждение: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
            continue

        for pattern_str in path_patterns:
            # Нормализуем разделители пути для pathlib
            normalized_pattern = pattern_str.replace("\\", r'/')
            
            # Получаем директорию из шаблона пути
            # Например, для 'sub_pkg/data/htmls/*.html', parent_dir_str будет 'sub_pkg/data/htmls'
            # Для '*.html', parent_dir_str будет '.'
            path_obj_for_parent = pathlib.Path(normalized_pattern)
            parent_dir_str = str(path_obj_for_parent.parent)

            current_traversable = package_root_traversable
            is_valid_target_dir = True

            # Переходим к целевой директории, если это не корень пакета ('.')
            if parent_dir_str != '.':
                path_segments = parent_dir_str.split('/')
                for segment in path_segments:
                    if not segment: # Пропускаем пустые сегменты (маловероятно при корректных путях)
                        continue
                    try:
                        current_traversable = current_traversable.joinpath(segment)
                        # Важно проверять is_dir() после каждого шага, если это промежуточный сегмент
                        if not current_traversable.is_dir():
                            is_valid_target_dir = False
                            break
                    except (FileNotFoundError, NotADirectoryError):
                        is_valid_target_dir = False
                        break
            
            if not is_valid_target_dir or not current_traversable.is_dir():
                # Целевая директория не найдена или не является директорией
                print(f"Предупреждение: Директория '{parent_dir_str}' не найдена или не является директорией в пакете '{package_name}'.")
                continue

            # Теперь ищем .html файлы в этой директории (current_traversable)
            try:
                for item in current_traversable.iterdir():
                    # item.name содержит имя файла (например, "page.html")
                    if item.is_file() and item.name.lower().endswith('.html'):
                        all_html_file_names.add(item.name)
            except Exception:
                # Обработка возможных ошибок при итерации по директории
                print(f"Предупреждение: Ошибка при итерации по директории в пакете '{package_name}', путь '{parent_dir_str}'.")
                pass
                
    return sorted(list(all_html_file_names))



def open_packaged_html_files_in_browser(
    package_name: str,
    relative_html_paths: List[str],
    give_path_back: Optional[bool] = False,
) -> None:
    """
    Открывает указанные HTML файлы из пакета в новых вкладках браузера.

    Args:
        package_name: Имя пакета (например, 'matplobblib').
        relative_html_paths: Список относительных путей к HTML файлам внутри пакета.
                             Пути должны быть от корня пакета.
                             Пример: ['nm/theory/htmls/page1.html', 'assets/main.html']
    """
    opened_any = False
    paths = []
    try:
        package_root_traversable = importlib.resources.files(package_name)
    except (ModuleNotFoundError, TypeError):
        print(f"Ошибка: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
        return

    for rel_path_str in relative_html_paths:
        if not rel_path_str.lower().endswith('.html'):
            print(f"Пропуск: '{rel_path_str}' не является HTML файлом (ожидается расширение .html).")
            continue

        current_resource = package_root_traversable
        # Используем pathlib.Path для корректного разбора пути на сегменты
        path_segments = Path(rel_path_str).parts
        
        resource_found_and_valid_type = True

        if not path_segments or path_segments == ('.',): # Пустой путь или "."
            print(f"Пропуск: Некорректный относительный путь '{rel_path_str}'.")
            continue

        for i, segment in enumerate(path_segments):
            if not segment: # Пропускаем пустые сегменты, если они как-то образовались
                continue
            try:
                next_resource = current_resource.joinpath(segment)
                # Проверяем, является ли ресурс директорией, если это не последний сегмент пути
                if i < len(path_segments) - 1:
                    if not next_resource.is_dir():
                        print(f"Ошибка: Промежуточный путь '{'/'.join(path_segments[:i+1])}' в '{rel_path_str}' не является директорией в пакете '{package_name}'.")
                        resource_found_and_valid_type = False
                        break
                current_resource = next_resource
            except (FileNotFoundError, NotADirectoryError):
                print(f"Ошибка: Сегмент пути '{segment}' в '{rel_path_str}' не найден в пакете '{package_name}'.")
                resource_found_and_valid_type = False
                break
        
        if not resource_found_and_valid_type:
            continue

        # Теперь current_resource указывает на предполагаемый файл
        if current_resource.is_file():
            try:
                # importlib.resources.as_file гарантирует, что ресурс доступен как файл в файловой системе
                # (может быть извлечен во временное место, если пакет - это zip-архив)
                with importlib.resources.as_file(current_resource) as actual_file_path:
                    if give_path_back:
                        paths.append(current_resource)
                    else:
                        
                        uri = actual_file_path.as_uri() # Преобразуем путь в file URI
                        # print(current_resource)
                        # print(f"Открывается: {uri}")
                        print(webbrowser.open_new_tab(uri))
                    opened_any = True
                    
            except FileNotFoundError: 
                 print(f"Ошибка (as_file): Файл для '{rel_path_str}' не найден в пакете '{package_name}'.")
            except Exception as e:
                print(f"Не удалось открыть '{rel_path_str}' из пакета '{package_name}': {e}")
        else:
            print(f"Ошибка: Ресурс '{rel_path_str}' не является файлом в пакете '{package_name}'.")

    if not opened_any and relative_html_paths:
        print(f"Ни один из указанных HTML файлов не был открыт из пакета '{package_name}'.")

    if give_path_back:
        return paths
    
    

package_data={
        'matplobblib': ['nm/theory/htmls/*.html'],
    }

htmls = get_all_packaged_html_files(package_data)
to_open_dct = {}

for i in htmls:
    parts = i.split('_')
    try:
        to_open_dct[int(parts[0])] = 'nm/theory/htmls/'+i
    except:
        continue

with open(open_packaged_html_files_in_browser('matplobblib',['nm/theory/htmls/index.html'],True)[0]  , "r", encoding="utf-8") as actual_file_path:
    
    html_content = actual_file_path.read()

# Парсинг HTML
soup = BeautifulSoup(html_content, "html.parser")

# Извлечение всех заголовков h1
h1_tags = soup.find_all("h1")
tags = [h1.get_text(strip=True) for h1 in h1_tags]

to_open_dct = dict(sorted(to_open_dct.items()))    

  
def open_ticket(num = None, to_print = True):
    """
    Открывает HTML-файл, связанный с номером билета, в браузере и/или отображает его содержимое.

    Если номер билета не указан, функция выводит список доступных билетов.

    Args:
        num (str, int, optional): Номер билета для открытия. Если None,
                                  будет выведен список билетов. По умолчанию None.
        to_print (bool, optional): Если True и указан `num`, содержимое HTML-файла
                                   будет отображено в текущей среде вывода
                                   (например, в Jupyter Notebook).
                                   Если False, файл будет только открыт в браузере.
                                   По умолчанию True.
    """
    if num:
        num = int(num)
        if to_print:
            # Предполагается, что open_packaged_html_files_in_browser возвращает список путей,
            # и мы берем первый элемент.
            now_path = open_packaged_html_files_in_browser('matplobblib',[to_open_dct[num]],True)[0]
            with open(now_path  , "r", encoding="utf-8") as actual_file_path:
    
                html_content = actual_file_path.read()
                # Предполагается, что display импортирован, например, из IPython.display
                display.display(display.HTML(html_content))
        else:
            open_packaged_html_files_in_browser('matplobblib',[to_open_dct[num]])
    else:
        # Предполагается, что 'tags' - это глобальная переменная (список/кортеж)
        print(*tags,sep='\n')


THEORY.append(open_ticket)