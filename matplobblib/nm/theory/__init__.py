import requests
import importlib.resources
from importlib.abc import Traversable # Явный импорт для Traversable
import pathlib
from typing import List, Dict, Set,Optional,Union
from io import BytesIO
import io
from PIL import Image
import IPython.display as display
import webbrowser
from pathlib import Path
from bs4 import BeautifulSoup
import tempfile


from ...forall import *

BASE_API_URL = r"https://api.github.com/repos/Ackrome/matplobblib/contents"
BASE_GET_URL = r"https://raw.githubusercontent.com/Ackrome/matplobblib/master"


subdirs = {
    'htmls' :   r'theory_files/htmls',
    'pngs'  :   r'theory_files/lec',
    'mds'   :   r'theory_files/ipynbs',
}


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
    if subdir.startswith('NM'):
        create_subdir_function(subdir, url)
####################################################################################################
# Здесь уже лежат билеты по NM, так что это работать должно
subdir = subdirs['htmls']
htmls = get_exact_format_files_from_subdir(subdir,exact_format='html')

to_open_dct = {}

for i in htmls:
    parts = i.split('htmls')[1][1:]
    
    try:
        to_open_dct[int(parts.split('_')[0])] = i
    except:
        if parts == 'index.html':
            response = requests.get(i)
            if response.status_code == 200:
                # Парсинг HTML
                soup = BeautifulSoup(response.text, "html.parser")
                # Извлечение всех заголовков h1
                h1_tags = soup.find_all("h1")
                
                index_html_url = i
        elif parts == 'Tanya.html':
            response = requests.get(i)
            if response.status_code == 200:
                Tanya_html_url = i

tags = [h1.get_text(strip=True) for h1 in h1_tags if len(h1.get_text(strip=True))] + ['Tanya.html', 'index.html']



to_open_dct = dict(sorted(to_open_dct.items()))

to_open_dct['Tanya.html'] = index_html_url
to_open_dct['index.html'] = Tanya_html_url

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
        response = requests.get(to_open_dct[num])
        if response.status_code == 200:
            if to_print:
                display.display(display.HTML(response.text))
            else:
                    # Создаем временный файл
                with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False, encoding='utf-8') as tmpfile:
                    tmpfile.write(response.text)
                    tmpfile_path = tmpfile.name
                # Открываем файл в браузере
                webbrowser.open_new_tab(f'file://{tmpfile_path}')
        else:
            print(f"Ошибка загрузки файла: {response.status_code}")
    else:
        # Предполагается, что 'tags' - это глобальная переменная (список/кортеж)
        print(*tags,sep='\n')

THEORY.append(open_ticket)
####################################################################################################
subdir = subdirs['pngs']
pngs = get_exact_format_files_from_subdir(subdir,exact_format='png')

to_open_dct_png = {}

for i in pngs:
    parts = i.split('lec')[1][1:]
    num = int(parts.split('_')[1].split('.')[0])
    to_open_dct_png[num] = i

    
to_open_dct_png = dict(sorted(to_open_dct_png.items()))


    
def open_prez(pages: Union[int, List[int]]):
    """
    Функция для просмотра презентации
    Отображает изображения PNG, соответствующие указанным номерам страниц.

    Функция может принимать один номер страницы, список номеров страниц
    или диапазон страниц (в виде списка из двух чисел).

    Args:
        pages: Может быть одним из следующих:
            - int: Номер одной страницы для отображения.
            - List[int] с одним элементом: Список, содержащий номер одной страницы.
            - List[int] с двумя элементами: Список, указывающий начальный и конечный
              номера страниц (включительно) для отображения диапазона.
            - List[int] с более чем двумя элементами: Список номеров страниц,
              каждая из которых будет отображена.

    Raises:
        KeyError: Если номер страницы, указанный в `pages`, отсутствует
                  в словаре `to_open_dct_png`.
        TypeError: Если аргумент `pages` имеет неподдерживаемый тип или
                   содержит элементы неподходящего типа (не int).

    Notes:
        Предполагается, что существует глобальный или доступный в области видимости
        словарь `to_open_dct_png`, где ключи - это номера страниц (int),
        а значения - это пути к файлам PNG или данные изображения,
        которые могут быть обработаны `display.Image()`.
        Также предполагается, что используется `IPython.display.display` и
        `IPython.display.Image`.
    """
    if isinstance(pages, int):
        
        url = to_open_dct_png[pages]
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            display.display(img)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки {url}: {e}")
            
    elif isinstance(pages, list):
        if not all(isinstance(j, int) for j in pages):
            print('Неправильно предоставленный аргумент: все элементы в списке должны быть целыми числами.')
            return

        if len(pages) == 1:
            url = to_open_dct_png[pages[0]]
            try:
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                display.display(img)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка загрузки {url}: {e}")
                
                
        elif len(pages) == 2:
            start_page, end_page = pages[0], pages[1]
            if start_page > end_page:
                print('Неправильно предоставленный аргумент: начальная страница диапазона не может быть больше конечной.')
                return
            for i in range(start_page, end_page + 1):
                url = to_open_dct_png[i]
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                    display.display(img)
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка загрузки {url}: {e}") 
                                
                
        elif len(pages) > 2:
            for i in pages:
                url = to_open_dct_png[i]
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    img = Image.open(BytesIO(response.content))
                    display.display(img)
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка загрузки {url}: {e}") 
        else: # len(pages) == 0
             print('Неправильно предоставленный аргумент: список страниц не может быть пустым.')
    else:
        print('Неправильно предоставленный аргумент: ожидается int или list[int].')

THEORY.append(open_prez)
####################################################################################################
subdir = subdirs['mds']
mds = get_exact_format_files_from_subdir(subdir,exact_format='md')
to_open_dct_md = {}
to_open_dct_md_nums = {}


for i in mds:
    name = i.split('ipynbs')[1][1:]
    parts = name.split('.')
    try:
        to_open_dct_md_nums[int(parts[0])] = i
    except:
        to_open_dct_md[name] = i

to_open_dct_md = dict(sorted(to_open_dct_md.items()))
to_open_dct_md_nums = dict(sorted(to_open_dct_md_nums.items()))

response = requests.get(to_open_dct_md['h1_names.md'])

h1_names = response.text.split('|||||')

names = []
for i in range(len(h1_names)):
    names.append(f'{i} = {h1_names[i]}')
    

def open_md(md_num = None):
    """Открывает некоторые преобразованные ipynb

    Args:
        md_num (str, optional): название файла
    """
    if md_num:
        try:
            md_num = int(md_num)
            response = requests.get(to_open_dct_md_nums[md_num])
            display.display(display.Markdown(response.text))            
        except:
            response = requests.get(to_open_dct_md[md_num])
            display.display(display.Markdown(response.text))
    else:
        print(*(list(to_open_dct_md.keys()) + names), sep='\n')


THEORY.append(open_md)
####################################################################################################























####################################################################################################
# Depreciated 0.3.10
####################################################################################################
# def get_all_packaged_md_files(package_data_config: Dict[str, List[str]]) -> List[str]:
#     """
#     Составляет список имен всех уникальных md-файлов, найденных во всех директориях,
#     указанных в конфигурации типа package_data, доступных изнутри установленного пакета.
#     Возвращаются только имена файлов, а не полные пути.

#     Args:
#         package_data_config: Словарь, аналогичный параметру `package_data` в setup.py.
#                              Ключи - это имена пакетов верхнего уровня (например, 'matplobblib').
#                              Значения - это списки строк с путями относительно корня пакета,
#                              обычно заканчивающиеся маской, такой как '*.md'.
#                              Пример: {'my_package': ['my_package/images/*.md', 'other_assets/*.md']}

#     Returns:
#         Отсортированный список уникальных имен md-файлов (например, ['image1.md', 'logo.md']).
#     """
#     all_md_file_names: Set[str] = set()

#     for package_name, path_patterns in package_data_config.items():
#         try:
#             # Получаем Traversable для корня пакета
#             package_root_traversable = importlib.resources.files(package_name)
#         except (ModuleNotFoundError, TypeError):
#             # Пакет не найден или не является валидным контейнером ресурсов
#             # Можно добавить логирование предупреждения, если необходимо
#             print(f"Предупреждение: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
#             continue

#         for pattern_str in path_patterns:
#             # Нормализуем разделители пути для pathlib
#             normalized_pattern = pattern_str.replace("\\", r'/')

#             # Получаем директорию из шаблона пути
#             # Например, для 'sub_pkg/data/htmls/*.html', parent_dir_str будет 'sub_pkg/data/htmls'
#             # Для '*.html', parent_dir_str будет '.'
#             path_obj_for_parent = pathlib.Path(normalized_pattern)
#             parent_dir_str = str(path_obj_for_parent.parent)

#             current_traversable = package_root_traversable
#             is_valid_target_dir = True

#             # Переходим к целевой директории, если это не корень пакета ('.')
#             if parent_dir_str != '.':
#                 path_segments = parent_dir_str.split('/')
#                 for segment in path_segments:
#                     if not segment: # Пропускаем пустые сегменты (маловероятно при корректных путях)
#                         continue
#                     try:
#                         current_traversable = current_traversable.joinpath(segment)
#                         # Важно проверять is_dir() после каждого шага, если это промежуточный сегмент
#                         if not current_traversable.is_dir():
#                             is_valid_target_dir = False
#                             break
#                     except (FileNotFoundError, NotADirectoryError):
#                         is_valid_target_dir = False
#                         break

#             if not is_valid_target_dir or not current_traversable.is_dir():
#                 # Целевая директория не найдена или не является директорией
#                 print(f"Предупреждение: Директория '{parent_dir_str}' не найдена или не является директорией в пакете '{package_name}'.")
#                 continue

#             # Теперь ищем .md файлы в этой директории (current_traversable)
#             try:
#                 for item in current_traversable.iterdir():
#                     # item.name содержит имя файла (например, "page.html")
#                     if item.is_file() and item.name.lower().endswith('.md'):
#                         all_md_file_names.add(item.name)
#             except Exception:
#                 # Обработка возможных ошибок при итерации по директории
#                 print(f"Предупреждение: Ошибка при итерации по директории в пакете '{package_name}', путь '{parent_dir_str}'.")
#                 pass

#     return sorted(list(all_md_file_names))
####################################################################################################
####################################################################################################
# def get_traversable_for_packaged_mds(
#     package_name: str,
#     relative_md_paths: List[str],
# ) -> List[Traversable]:
#     """
#     Находит указанные md файлы внутри пакета и возвращает для них Traversable объекты.

#     Args:
#         package_name: Имя пакета (например, 'my_package').
#         relative_md_paths: Список относительных путей к md файлам внутри пакета.
#                              Пути должны быть от корня пакета.
#                              Пример: ['images/logo.md', 'assets/icon.md']
#     Returns:
#         Список Traversable объектов для найденных md файлов.
#         Если файл не найден, путь некорректен, или ресурс не является файлом,
#         он будет пропущен, и будет выведено соответствующее сообщение.
#     """
#     found_traversables: List[Traversable] = []
#     try:
#         package_root_traversable = importlib.resources.files(package_name)
#     except (ModuleNotFoundError, TypeError):
#         print(f"Ошибка: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
#         return found_traversables

#     for rel_path_str in relative_md_paths:
#         if not rel_path_str.lower().endswith('.md'):
#             print(f"Пропуск (не md): '{rel_path_str}' не является md файлом (ожидается расширение .md).")
#             continue

#         current_traversable_candidate = package_root_traversable
#         # Используем pathlib.Path для корректного разбора пути на сегменты
#         try:
#             path_segments = Path(rel_path_str).parts
#         except TypeError: # Обработка случая, если rel_path_str не может быть преобразован в Path
#             print(f"Пропуск (некорректный формат пути): '{rel_path_str}' не является корректной строкой пути.")
#             continue
            
#         path_is_valid = True

#         if not path_segments or (len(path_segments) == 1 and path_segments[0] == '.'): # Пустой путь или "."
#             print(f"Пропуск (некорректный путь): Относительный путь '{rel_path_str}' некорректен.")
#             continue

#         # Итерация по всем сегментам пути.
#         # current_traversable_candidate в итоге будет указывать на целевой ресурс.
#         for i, segment in enumerate(path_segments):
#             if not segment: # Редкий случай с Path.parts, но для надежности
#                 path_is_valid = False 
#                 print(f"Пропуск (пустой сегмент): Обнаружен пустой сегмент в пути '{rel_path_str}'.")
#                 break
            
#             current_traversable_candidate = current_traversable_candidate.joinpath(segment)
            
#             # Если это промежуточный сегмент, он должен быть директорией.
#             if i < len(path_segments) - 1:
#                 if not current_traversable_candidate.is_dir():
#                     print(f"Ошибка (не директория): Промежуточный путь '{'/'.join(path_segments[:i+1])}' (часть '{rel_path_str}') не является директорией в пакете '{package_name}'.")
#                     path_is_valid = False
#                     break
        
#         if not path_is_valid:
#             continue

#         # После цикла, current_traversable_candidate указывает на целевой ресурс.
#         # Проверяем, является ли он файлом.
#         if current_traversable_candidate.is_file():
#             found_traversables.append(current_traversable_candidate)
#         else:
#             print(f"Предупреждение (не файл): Ресурс по пути '{rel_path_str}' в пакете '{package_name}' не является файлом (или не существует).")

#     if not found_traversables and relative_md_paths:
#         print(f"Ни один из указанных md файлов не был успешно найден как Traversable объект в пакете '{package_name}'.")

#     return found_traversables 
####################################################################################################
# path for mds = 'matplobblib/nm/theory/ipynbs/' 
# e.g. url = "https://raw.githubusercontent.com/Ackrome/matplobblib/master/matplobblib/nm/theory/ipynbs/Числаки.md"
# list_subdirectories("https://raw.githubusercontent.com/Ackrome/matplobblib/master/matplobblib/nm/theory/ipynbs")



# print(get_exact_format_files_from_subdir("https://raw.githubusercontent.com/Ackrome/matplobblib/master/matplobblib/nm/theory/ipynbs",'md'))

# mds = get_all_packaged_md_files(package_data)
# to_open_dct_md = {}
# to_open_dct_md_nums = {}


# for i in mds:
#     parts = i.split('.')
#     try:
#         to_open_dct_md_nums[int(parts[0])] = get_traversable_for_packaged_mds('matplobblib',['nm/theory/ipynbs/'+i])[0]
#     except:
#         to_open_dct_md[i] = get_traversable_for_packaged_mds('matplobblib',['nm/theory/ipynbs/'+i])[0]

    
# to_open_dct_md = dict(sorted(to_open_dct_md.items()))
# to_open_dct_md_nums = dict(sorted(to_open_dct_md_nums.items()))

# with io.open(to_open_dct_md['h1_names.md'], encoding='utf-8', errors='ignore') as f:
#     h1_names = f.readlines()[0].split('|||||')

# names = []
# for i in range(len(h1_names)):
#     names.append(f'{i} = {h1_names[i]}')

# ####################################################################################################
# def open_md(md_num = None):
#     """Открывает некоторые преобразованные ipynb

#     Args:
#         md_num (str, optional): название файла
#     """
#     if md_num:
#         try:
#             md_num = int(md_num)
#             with io.open(to_open_dct_md_nums[md_num], encoding='utf-8', errors='ignore') as f:
#                 display.display(display.Markdown(f.read()))
            
#         except:       
#             with io.open(to_open_dct_md[md_num], encoding='utf-8', errors='ignore') as f:
#                 display.display(display.Markdown(f.read()))
#     else:
#         print(*(list(to_open_dct_md.keys()) + names), sep='\n')
# ####################################################################################################
# THEORY.append(open_md)
####################################################################################################









####################################################################################################
# Depreciated 0.3.9
####################################################################################################
# def get_traversable_for_packaged_pngs(
#     package_name: str,
#     relative_png_paths: List[str],
# ) -> List[Traversable]:
#     """
#     Находит указанные PNG файлы внутри пакета и возвращает для них Traversable объекты.

#     Args:
#         package_name: Имя пакета (например, 'my_package').
#         relative_png_paths: Список относительных путей к PNG файлам внутри пакета.
#                              Пути должны быть от корня пакета.
#                              Пример: ['images/logo.png', 'assets/icon.png']
#     Returns:
#         Список Traversable объектов для найденных PNG файлов.
#         Если файл не найден, путь некорректен, или ресурс не является файлом,
#         он будет пропущен, и будет выведено соответствующее сообщение.
#     """
#     found_traversables: List[Traversable] = []
#     try:
#         package_root_traversable = importlib.resources.files(package_name)
#     except (ModuleNotFoundError, TypeError):
#         print(f"Ошибка: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
#         return found_traversables

#     for rel_path_str in relative_png_paths:
#         if not rel_path_str.lower().endswith('.png'):
#             print(f"Пропуск (не PNG): '{rel_path_str}' не является PNG файлом (ожидается расширение .png).")
#             continue

#         current_traversable_candidate = package_root_traversable
#         # Используем pathlib.Path для корректного разбора пути на сегменты
#         try:
#             path_segments = Path(rel_path_str).parts
#         except TypeError: # Обработка случая, если rel_path_str не может быть преобразован в Path
#             print(f"Пропуск (некорректный формат пути): '{rel_path_str}' не является корректной строкой пути.")
#             continue
            
#         path_is_valid = True

#         if not path_segments or (len(path_segments) == 1 and path_segments[0] == '.'): # Пустой путь или "."
#             print(f"Пропуск (некорректный путь): Относительный путь '{rel_path_str}' некорректен.")
#             continue

#         # Итерация по всем сегментам пути.
#         # current_traversable_candidate в итоге будет указывать на целевой ресурс.
#         for i, segment in enumerate(path_segments):
#             if not segment: # Редкий случай с Path.parts, но для надежности
#                 path_is_valid = False 
#                 print(f"Пропуск (пустой сегмент): Обнаружен пустой сегмент в пути '{rel_path_str}'.")
#                 break
            
#             current_traversable_candidate = current_traversable_candidate.joinpath(segment)
            
#             # Если это промежуточный сегмент, он должен быть директорией.
#             if i < len(path_segments) - 1:
#                 if not current_traversable_candidate.is_dir():
#                     print(f"Ошибка (не директория): Промежуточный путь '{'/'.join(path_segments[:i+1])}' (часть '{rel_path_str}') не является директорией в пакете '{package_name}'.")
#                     path_is_valid = False
#                     break
        
#         if not path_is_valid:
#             continue

#         # После цикла, current_traversable_candidate указывает на целевой ресурс.
#         # Проверяем, является ли он файлом.
#         if current_traversable_candidate.is_file():
#             found_traversables.append(current_traversable_candidate)
#         else:
#             print(f"Предупреждение (не файл): Ресурс по пути '{rel_path_str}' в пакете '{package_name}' не является файлом (или не существует).")

#     if not found_traversables and relative_png_paths:
#         print(f"Ни один из указанных PNG файлов не был успешно найден как Traversable объект в пакете '{package_name}'.")

#     return found_traversables
####################################################################################################
# def get_all_packaged_png_files(package_data_config: Dict[str, List[str]]) -> List[str]:
#     """
#     Составляет список имен всех уникальных PNG-файлов, найденных во всех директориях,
#     указанных в конфигурации типа package_data, доступных изнутри установленного пакета.
#     Возвращаются только имена файлов, а не полные пути.

#     Args:
#         package_data_config: Словарь, аналогичный параметру `package_data` в setup.py.
#                              Ключи - это имена пакетов верхнего уровня (например, 'matplobblib').
#                              Значения - это списки строк с путями относительно корня пакета,
#                              обычно заканчивающиеся маской, такой как '*.png'.
#                              Пример: {'my_package': ['my_package/images/*.png', 'other_assets/*.png']}

#     Returns:
#         Отсортированный список уникальных имен PNG-файлов (например, ['image1.png', 'logo.png']).
#     """
#     all_png_file_names: Set[str] = set()

#     for package_name, path_patterns in package_data_config.items():
#         try:
#             # Получаем Traversable для корня пакета
#             package_root_traversable = importlib.resources.files(package_name)
#         except (ModuleNotFoundError, TypeError):
#             # Пакет не найден или не является валидным контейнером ресурсов
#             # Можно добавить логирование предупреждения, если необходимо
#             print(f"Предупреждение: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
#             continue

#         for pattern_str in path_patterns:
#             # Нормализуем разделители пути для pathlib
#             normalized_pattern = pattern_str.replace("\\", r'/')

#             # Получаем директорию из шаблона пути
#             # Например, для 'sub_pkg/data/htmls/*.html', parent_dir_str будет 'sub_pkg/data/htmls'
#             # Для '*.html', parent_dir_str будет '.'
#             path_obj_for_parent = pathlib.Path(normalized_pattern)
#             parent_dir_str = str(path_obj_for_parent.parent)

#             current_traversable = package_root_traversable
#             is_valid_target_dir = True

#             # Переходим к целевой директории, если это не корень пакета ('.')
#             if parent_dir_str != '.':
#                 path_segments = parent_dir_str.split('/')
#                 for segment in path_segments:
#                     if not segment: # Пропускаем пустые сегменты (маловероятно при корректных путях)
#                         continue
#                     try:
#                         current_traversable = current_traversable.joinpath(segment)
#                         # Важно проверять is_dir() после каждого шага, если это промежуточный сегмент
#                         if not current_traversable.is_dir():
#                             is_valid_target_dir = False
#                             break
#                     except (FileNotFoundError, NotADirectoryError):
#                         is_valid_target_dir = False
#                         break

#             if not is_valid_target_dir or not current_traversable.is_dir():
#                 # Целевая директория не найдена или не является директорией
#                 print(f"Предупреждение: Директория '{parent_dir_str}' не найдена или не является директорией в пакете '{package_name}'.")
#                 continue

#             # Теперь ищем .png файлы в этой директории (current_traversable)
#             try:
#                 for item in current_traversable.iterdir():
#                     # item.name содержит имя файла (например, "page.html")
#                     if item.is_file() and item.name.lower().endswith('.png'):
#                         all_png_file_names.add(item.name)
#             except Exception:
#                 # Обработка возможных ошибок при итерации по директории
#                 print(f"Предупреждение: Ошибка при итерации по директории в пакете '{package_name}', путь '{parent_dir_str}'.")
#                 pass

#     return sorted(list(all_png_file_names))
####################################################################################################
# pngs = get_all_packaged_png_files(package_data)
# to_open_dct_png = {}

# for i in pngs:
#     parts = i.split('_')
#     num = int(parts[1].split('.')[0])
#     to_open_dct_png[num] = get_traversable_for_packaged_pngs('matplobblib',['nm/theory/lec/'+i])[0]

    
# to_open_dct_png = dict(sorted(to_open_dct_png.items()))    
# ####################################################################################################
# def open_prez(pages: Union[int, List[int]]):
#     """
#     Функция для просмотра презентации
#     Отображает изображения PNG, соответствующие указанным номерам страниц.

#     Функция может принимать один номер страницы, список номеров страниц
#     или диапазон страниц (в виде списка из двух чисел).

#     Args:
#         pages: Может быть одним из следующих:
#             - int: Номер одной страницы для отображения.
#             - List[int] с одним элементом: Список, содержащий номер одной страницы.
#             - List[int] с двумя элементами: Список, указывающий начальный и конечный
#               номера страниц (включительно) для отображения диапазона.
#             - List[int] с более чем двумя элементами: Список номеров страниц,
#               каждая из которых будет отображена.

#     Raises:
#         KeyError: Если номер страницы, указанный в `pages`, отсутствует
#                   в словаре `to_open_dct_png`.
#         TypeError: Если аргумент `pages` имеет неподдерживаемый тип или
#                    содержит элементы неподходящего типа (не int).

#     Notes:
#         Предполагается, что существует глобальный или доступный в области видимости
#         словарь `to_open_dct_png`, где ключи - это номера страниц (int),
#         а значения - это пути к файлам PNG или данные изображения,
#         которые могут быть обработаны `display.Image()`.
#         Также предполагается, что используется `IPython.display.display` и
#         `IPython.display.Image`.
#     """
#     if isinstance(pages, int):
#         display.display(display.Image(to_open_dct_png[pages]))
#     elif isinstance(pages, list):
#         if not all(isinstance(j, int) for j in pages):
#             print('Неправильно предоставленный аргумент: все элементы в списке должны быть целыми числами.')
#             return

#         if len(pages) == 1:
#             display.display(display.Image(to_open_dct_png[pages[0]]))
#         elif len(pages) == 2:
#             start_page, end_page = pages[0], pages[1]
#             if start_page > end_page:
#                 print('Неправильно предоставленный аргумент: начальная страница диапазона не может быть больше конечной.')
#                 return
#             for i in range(start_page, end_page + 1):
#                 display.display(display.Image(to_open_dct_png[i]))
#         elif len(pages) > 2:
#             for i in pages:
#                 display.display(display.Image(to_open_dct_png[i]))
#         else: # len(pages) == 0
#              print('Неправильно предоставленный аргумент: список страниц не может быть пустым.')
#     else:
#         print('Неправильно предоставленный аргумент: ожидается int или list[int].')
# ####################################################################################################




####################################################################################################
# Depreciated 0.3.8
####################################################################################################
# def open_packaged_html_files_in_browser(
#     package_name: str,
#     relative_html_paths: List[str],
#     give_path_back: Optional[bool] = False,
# ) -> None:
#     """
#     Открывает указанные HTML файлы из пакета в новых вкладках браузера.

#     Args:
#         package_name: Имя пакета (например, 'matplobblib').
#         relative_html_paths: Список относительных путей к HTML файлам внутри пакета.
#                              Пути должны быть от корня пакета.
#                              Пример: ['nm/theory/htmls/page1.html', 'assets/main.html']
#     """
#     opened_any = False
#     paths = []
#     try:
#         package_root_traversable = importlib.resources.files(package_name)
#     except (ModuleNotFoundError, TypeError):
#         print(f"Ошибка: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
#         return

#     for rel_path_str in relative_html_paths:
#         if not rel_path_str.lower().endswith('.html'):
#             print(f"Пропуск: '{rel_path_str}' не является HTML файлом (ожидается расширение .html).")
#             continue

#         current_resource = package_root_traversable
#         # Используем pathlib.Path для корректного разбора пути на сегменты
#         path_segments = Path(rel_path_str).parts
        
#         resource_found_and_valid_type = True

#         if not path_segments or path_segments == ('.',): # Пустой путь или "."
#             print(f"Пропуск: Некорректный относительный путь '{rel_path_str}'.")
#             continue

#         for i, segment in enumerate(path_segments):
#             if not segment: # Пропускаем пустые сегменты, если они как-то образовались
#                 continue
#             try:
#                 next_resource = current_resource.joinpath(segment)
#                 # Проверяем, является ли ресурс директорией, если это не последний сегмент пути
#                 if i < len(path_segments) - 1:
#                     if not next_resource.is_dir():
#                         print(f"Ошибка: Промежуточный путь '{'/'.join(path_segments[:i+1])}' в '{rel_path_str}' не является директорией в пакете '{package_name}'.")
#                         resource_found_and_valid_type = False
#                         break
#                 current_resource = next_resource
#             except (FileNotFoundError, NotADirectoryError):
#                 print(f"Ошибка: Сегмент пути '{segment}' в '{rel_path_str}' не найден в пакете '{package_name}'.")
#                 resource_found_and_valid_type = False
#                 break
        
#         if not resource_found_and_valid_type:
#             continue

#         # Теперь current_resource указывает на предполагаемый файл
#         if current_resource.is_file():
#             try:
#                 # importlib.resources.as_file гарантирует, что ресурс доступен как файл в файловой системе
#                 # (может быть извлечен во временное место, если пакет - это zip-архив)
#                 with importlib.resources.as_file(current_resource) as actual_file_path:
#                     if give_path_back:
#                         paths.append(current_resource)
#                     else:
                        
#                         uri = actual_file_path.as_uri() # Преобразуем путь в file URI
#                         # print(current_resource)
#                         # print(f"Открывается: {uri}")
#                         print(webbrowser.open_new_tab(uri))
#                     opened_any = True
                    
#             except FileNotFoundError: 
#                  print(f"Ошибка (as_file): Файл для '{rel_path_str}' не найден в пакете '{package_name}'.")
#             except Exception as e:
#                 print(f"Не удалось открыть '{rel_path_str}' из пакета '{package_name}': {e}")
#         else:
#             print(f"Ошибка: Ресурс '{rel_path_str}' не является файлом в пакете '{package_name}'.")

#     if not opened_any and relative_html_paths:
#         print(f"Ни один из указанных HTML файлов не был открыт из пакета '{package_name}'.")

#     if give_path_back:
#         return paths
####################################################################################################
# def get_all_packaged_html_files(package_data_config: Dict[str, List[str]]) -> List[str]:
#     """
#     Составляет список имен всех уникальных HTML-файлов, найденных во всех директориях,
#     указанных в конфигурации типа package_data, доступных изнутри установленного пакета.
#     Возвращаются только имена файлов, а не полные пути.

#     Args:
#         package_data_config: Словарь, аналогичный параметру `package_data` в setup.py.
#                              Ключи - это имена пакетов верхнего уровня (например, 'matplobblib').
#                              Значения - это списки строк с путями относительно корня пакета,
#                              обычно заканчивающиеся маской, такой как '*.html'.
#                              Пример: {'matplobblib': ['matplobblib/nm/theory/htmls/*.html', 'other_data/*.html']}

#     Returns:
#         Отсортированный список уникальных имен HTML-файлов (например, ['page1.html', 'index.html']).
#     """
#     all_html_file_names: Set[str] = set()

#     for package_name, path_patterns in package_data_config.items():
#         try:
#             # Получаем Traversable для корня пакета
#             package_root_traversable = importlib.resources.files(package_name)
#         except (ModuleNotFoundError, TypeError):
#             # Пакет не найден или не является валидным контейнером ресурсов
#             # Можно добавить логирование предупреждения, если необходимо
#             print(f"Предупреждение: Пакет '{package_name}' не найден или не является корректным контейнером ресурсов.")
#             continue

#         for pattern_str in path_patterns:
#             # Нормализуем разделители пути для pathlib
#             normalized_pattern = pattern_str.replace("\\", r'/')
            
#             # Получаем директорию из шаблона пути
#             # Например, для 'sub_pkg/data/htmls/*.html', parent_dir_str будет 'sub_pkg/data/htmls'
#             # Для '*.html', parent_dir_str будет '.'
#             path_obj_for_parent = pathlib.Path(normalized_pattern)
#             parent_dir_str = str(path_obj_for_parent.parent)

#             current_traversable = package_root_traversable
#             is_valid_target_dir = True

#             # Переходим к целевой директории, если это не корень пакета ('.')
#             if parent_dir_str != '.':
#                 path_segments = parent_dir_str.split('/')
#                 for segment in path_segments:
#                     if not segment: # Пропускаем пустые сегменты (маловероятно при корректных путях)
#                         continue
#                     try:
#                         current_traversable = current_traversable.joinpath(segment)
#                         # Важно проверять is_dir() после каждого шага, если это промежуточный сегмент
#                         if not current_traversable.is_dir():
#                             is_valid_target_dir = False
#                             break
#                     except (FileNotFoundError, NotADirectoryError):
#                         is_valid_target_dir = False
#                         break
            
#             if not is_valid_target_dir or not current_traversable.is_dir():
#                 # Целевая директория не найдена или не является директорией
#                 print(f"Предупреждение: Директория '{parent_dir_str}' не найдена или не является директорией в пакете '{package_name}'.")
#                 continue

#             # Теперь ищем .html файлы в этой директории (current_traversable)
#             try:
#                 for item in current_traversable.iterdir():
#                     # item.name содержит имя файла (например, "page.html")
#                     if item.is_file() and item.name.lower().endswith('.html'):
#                         all_html_file_names.add(item.name)
#             except Exception:
#                 # Обработка возможных ошибок при итерации по директории
#                 print(f"Предупреждение: Ошибка при итерации по директории в пакете '{package_name}', путь '{parent_dir_str}'.")
#                 pass
                
#     return sorted(list(all_html_file_names))


# htmls = get_all_packaged_html_files(package_data)
# to_open_dct = {}

# for i in htmls:
#     parts = i.split('_')
#     try:
#         to_open_dct[int(parts[0])] = 'nm/theory/htmls/'+i
#     except:
#         continue

# with open(open_packaged_html_files_in_browser('matplobblib',['nm/theory/htmls/index.html'],True)[0]  , "r", encoding="utf-8") as actual_file_path:
    
#     html_content = actual_file_path.read()

# # Парсинг HTML
# soup = BeautifulSoup(html_content, "html.parser")

# # Извлечение всех заголовков h1
# h1_tags = soup.find_all("h1")
# tags = [h1.get_text(strip=True) for h1 in h1_tags] + ['Tanya.html', 'index.html']

# to_open_dct = dict(sorted(to_open_dct.items()))    

# to_open_dct['Tanya.html'] = 'nm/theory/htmls/'+'Tanya.html'
# to_open_dct['index.html'] = 'nm/theory/htmls/'+'index.html'

  
# def open_ticket(num = None, to_print = True):
#     """
#     Открывает HTML-файл, связанный с номером билета, в браузере и/или отображает его содержимое.

#     Если номер билета не указан, функция выводит список доступных билетов.

#     Args:
#         num (str, int, optional): Номер билета для открытия. Если None,
#                                   будет выведен список билетов. По умолчанию None.
#         to_print (bool, optional): Если True и указан `num`, содержимое HTML-файла
#                                    будет отображено в текущей среде вывода
#                                    (например, в Jupyter Notebook).
#                                    Если False, файл будет только открыт в браузере.
#                                    По умолчанию True.
#     """
#     if num:
#         if to_print:
#             # Предполагается, что open_packaged_html_files_in_browser возвращает список путей,
#             # и мы берем первый элемент.
#             now_path = open_packaged_html_files_in_browser('matplobblib',[to_open_dct[num]],True)[0]
#             with open(now_path  , "r", encoding="utf-8") as actual_file_path:
    
#                 html_content = actual_file_path.read()
#                 # Предполагается, что display импортирован, например, из IPython.display
#                 display.display(display.HTML(html_content))
#         else:
#             open_packaged_html_files_in_browser('matplobblib',[to_open_dct[num]])
#     else:
#         # Предполагается, что 'tags' - это глобальная переменная (список/кортеж)
#         print(*tags,sep='\n')
####################################################################################################
####################################################################################################
####################################################################################################