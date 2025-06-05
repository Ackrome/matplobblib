import numpy as np
import pandas as pd
import re
from inspect import getsource, getdoc
import matplotlib.pyplot as plt
import sys
from numba import njit, prange
import warnings
warnings.filterwarnings('ignore')
####################################################################################
pattern = r'\s*(.*?)\s*(?=def __init__|Args|Параметры|Parameters)' #     pattern = r'\s*[\s\S]*?([\s\S]+?)\s+[Parameters|Args]'
####################################################################################
def get_task_from_func(func, to_search=False):
    """
    Извлекает описание параметров или полный docstring из функции.

    Parameters
    ----------
    func : callable
        Функция, из которой извлекается документация.
    to_search : bool, optional
        Если True, ищет только секцию 'Args' или 'Parameters' и удаляет пробелы/переносы.
        Если False, возвращает полный docstring с сохранением форматирования.

    Returns
    -------
    str or None
        Обработанная часть docstring или None, если документация отсутствует.

    Notes
    -----
    1. Использует регулярные выражения для поиска секции 'Args'/'Parameters'.
    2. При отсутствии docstring возвращает None, чтобы избежать ошибок.
    3. Рекомендуется использовать `inspect.getdoc()` вместо регулярного выражения для полного текста.

    Examples
    --------
    >>> def example(x: int):
    ...     '''Example function.
    ...     Parameters
    ...     ----------
    ...     x : int
    ...         Value to process.
    ...     '''
    ...     return x
    ...
    >>> get_task_from_func(example, to_search=True)
    'Parameters----------x:intValueToprocess.'

    >>> get_task_from_func(example, to_search=False)  # doctest: +ELLIPSIS
    'Example function.\\n    Parameters\\n    ----------\\n    x : int\\n        Value to process.'
    """
    doc = getdoc(func)
    if not doc:
        return None
    
    try:
        return re.search(pattern,doc,re.DOTALL).group(1).replace('\n','').replace(' ','') if to_search else re.search(pattern,doc,re.DOTALL).group(1)
    except:
        try:
            return doc.replace('\n','').replace(' ','') if to_search else doc
        except:
            return doc
####################################################################################
#from .nm.additional_funcs import *
####################################################################################
# rrstr (Округление до n знаков)
####################################################################################
def one_rrstr(x, n=0): # округление до n знаков после запятой
    if n == 0:
        return str(x)
    fmt = '{:.' + str(n) + 'f}'
    return fmt.format(x).replace('.', ',')

def un_one_rrstr(x):
    return float(x.replace(',', '.'))

def un_rrstr(x):
    return np.vectorize(un_one_rrstr)(x)


def rrstr(x, n):
    """
    Форматирует числа или массивы чисел с округлением до заданного количества знаков после запятой.

    Parameters
    ----------
    x : float or array_like
        Число или массив чисел для форматирования.
    n : int
        Количество знаков после десятичного разделителя (запятой).

    Returns
    -------
    str or ndarray
        Строка (для скалярных входов) или массив строк (для последовательностей).
        Десятичный разделитель представлен запятой.

    Notes
    -----
    1. Поддерживает векторизацию через numpy.vectorize.
    2. Для n=0 выполняет только замену точки на запятую (если есть).
    3. Требует установленной библиотеки numpy.
    4. Не предназначен для работы с отрицательными значениями n.

    Examples
    --------
    >>> rrstr(3.1415, 2)
    '3,14'

    >>> rrstr([1.2345, 2.789], 1)
    array(['1,2', '2,8'], dtype='<U3')

    >>> rrstr(42, 0)
    '42'

    References
    ----------
    .. [1] NumPy Documentation: https://numpy.org/doc/
    .. [2] Python Software Foundation. "Python Language Reference", version 3.11.
    """
    rrstr1 = np.vectorize(one_rrstr)
    res = rrstr1(x, n)
    if res.size == 1:
        return str(res)
    return res
####################################################################################
# show_img показывает фотографию в ячейке вывода
####################################################################################
def show_img(filename):
    """
    Отображает изображение в интерфейсе Jupyter Notebook/IPython.

    Parameters
    ----------
    filename : str
        Путь к файлу изображения, который необходимо отобразить.
        Поддерживаются стандартные графические форматы (PNG, JPEG и др.).

    Returns
    -------
    str
        Возвращает переданный путь к файлу без изменений, 
        независимо от успешности отображения изображения.

    Notes
    -----
    1. Требует наличия библиотеки IPython в окружении.
    2. Функция работает только в интерактивных средах (Jupyter Notebook, IPython).
    3. При отсутствии файла/ошибке загрузки:
       - Выводит сообщение 'Неправильное имя файла'
       - Не прерывает выполнение программы
    4. Поддерживает все форматы, поддерживаемые классом IPython.display.Image

    Examples
    --------
    >>> show_img("example.png")
    # Отображает изображение example.png если оно существует

    >>> show_img("nonexistent.jpg")
    Неправильное имя файла
    'nonexistent.jpg'

    References
    ----------
    .. [1] IPython Documentation: https://ipython.readthedocs.io/en/stable/
    .. [2] Jupyter Notebook documentation: https://jupyter-notebook.readthedocs.io/en/latest/
    """
    from IPython.display import display, Image
    try:
        img = Image(filename=filename)
        display(img)
    except:
        print('Неправильное имя файла')
    return filename
####################################################################################
# show_images показывает несколько фотографий 
# в ячейке вывода по названиям в итерируемом аргументе  
####################################################################################
def show_images(filenames):
    """
    Отображает изображения из указанных файлов в интерфейсе Jupyter Notebook/IPython.

    Параметры
    ---------
    filenames : str or array_like
        Путь к одному файлу изображения (строка) или последовательность путей (список, массив).
        Поддерживаются стандартные графические форматы (PNG, JPEG и др.).

    Возвращает
    ----------
    str or ndarray
        Если входной аргумент - скаляр: возвращает строку с именем файла.
        Если входной аргумент - последовательность: возвращает numpy.ndarray со списком имен файлов.

    Примечания
    ---------
    1. Функция основана на `np.vectorize` для поддержки массивов/списков файлов.
    2. Требует наличия библиотеки IPython и работы в интерактивной среде (Jupyter Notebook, IPython).
    3. При отсутствии файла/ошибке загрузки:
       - Выводит сообщение 'Неправильное имя файла'
       - Не прерывает выполнение программы
       - Возвращает имя файла как есть
    4. Каждое изображение отображается немедленно при обработке.

    Примеры
    --------
    >>> show_images("example.png")
    'example.png'  # Изображение будет отображено в ячейке вывода

    >>> show_images(["img1.jpg", "img2.png"])
    array(['img1.jpg', 'img2.png'], dtype='<U8')  # Оба изображения отобразятся последовательно

    >>> show_images(np.array([["a.png", "b.png"], ["c.png", "d.png"]]))
    array([['a.png', 'b.png'], ['c.png', 'd.png']], dtype='<U5')  # Поддержка многомерных массивов

    Ссылки
    ------
    .. [1] Документация show_img: https://github.com/example/docs/show_img
    .. [2] IPython Documentation: https://ipython.readthedocs.io/en/stable/
    .. [3] Jupyter Notebook documentation: https://jupyter-notebook.readthedocs.io/en/latest/
    """
    return np.vectorize(show_img)(filenames)
####################################################################################
# save_pdf_as_images (Сохраняет каждую страничку pdf как png файл)
####################################################################################    
def save_pdf_as_images(pdf_path, output_folder=None, dpi=100):
    """
    Конвертирует PDF-документ в изображения и сохраняет их в указанной папке.

    Parameters
    ----------
    pdf_path : str
        Путь к исходному PDF-файлу, который необходимо конвертировать.
    output_folder : str, optional
        Путь к папке, куда будут сохранены изображения. Если None, создается папка
        с тем же именем, что и у PDF-файла, но без расширения.
    dpi : int, optional
        Разрешение вывода изображений в точках на дюйм (dots per inch).
        Более высокое значение увеличивает качество, но замедляет обработку.

    Returns
    -------
    list of str
        Список абсолютных путей к сохраненным PNG-файлам.

    Notes
    -----
    1. Требует установленной библиотеки `pdf2image` и Poppler (для Windows).
    2. Автоматически создает выходную папку, если она отсутствует.
    3. Имена файлов генерируются по шаблону "page_номер.png".
    4. При работе с большими PDF файлами потребуется больше оперативной памяти.
    5. Для Linux-систем Poppler можно установить через пакетный менеджер.

    Examples
    --------
    >>> save_pdf_as_images("document.pdf")
    # Сохранит страницы в папке "document" с разрешением 100 DPI
    
    >>> save_pdf_as_images("report.pdf", "output_images", dpi=200)
    # Сохранит страницы в папке "output_images" с разрешением 200 DPI

    References
    ----------
    .. [1] "pdf2image documentation" https://pdf2image.readthedocs.io/en/latest/
    .. [2] Python Software Foundation. "Python Language Reference", version 3.11.
    """
    from pdf2image import convert_from_path
    import os
    
    if output_folder is None:
        output_folder = pdf_path[:-4]
        
    outpaths = []
    # Создаем папку для сохранения, если её нет
    os.makedirs(output_folder, exist_ok=True)

    # Конвертируем PDF в список изображений
    try:
        pages = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        raise RuntimeError(f"Ошибка при конвертации PDF: {str(e)}")

    # Сохраняем каждую страницу как изображение
    for page_number, page in enumerate(pages, start=1):
        output_path = os.path.join(output_folder, f"page_{page_number}.png")
        try:
            page.save(output_path, "PNG")
            outpaths.append(os.path.abspath(output_path))
            print(f"Страница {page_number} сохранена как {output_path}")
        except Exception as e:
            print(f"Ошибка при сохранении страницы {page_number}: {str(e)}")
            
    return outpaths
####################################################################################
import pyperclip

#Делаем функцию которая принимает переменную text
def write(name):
    """
    Копирует указанную информацию в системный буфер обмена.

    Parameters
    ----------
    name : str
        Строка, которую необходимо скопировать в буфер обмена.

    Returns
    -------
    None
        Функция не возвращает значение, но выполняет побочный эффект (копирование в буфер).

    Notes
    -----
    1. Функция использует библиотеку `pyperclip`, которая должна быть установлена.
    2. Второй вызов `pyperclip.paste()` не влияет на результат выполнения функции.
    3. Для работы на Linux-системах может потребоваться установка дополнительных зависимостей (например, `xclip`).

    Examples
    --------
    >>> write("Hello, World!")
    # Строка "Hello, World!" будет скопирована в буфер обмена

    >>> write("12345")
    # Числовая строка "12345" будет доступна для вставки из буфера

    References
    ----------
    .. [1] Pyperclip documentation: https://pyperclip.readthedocs.io/en/latest/
    .. [2] Sweigart, A. "Automate the Boring Stuff with Python", 2nd edition.
    """
    pyperclip.copy(name)  # Копирование в буфер обмена
    pyperclip.paste()     # Дублирующий вызов для проверки буфера
####################################################################################
def invert_dict(d):
    """
    Возвращает новый словарь с поменяными местами ключами и значениями исходного словаря.

    Parameters
    ----------
    d : dict
        Исходный словарь, значения которого должны быть хэшируемыми (например, не списки).

    Returns
    -------
    dict
        Словарь, где ключи и значения исходного словаря поменяны местами.

    Notes
    -----
    1. Если в исходном словаре есть дублирующиеся значения, последние ключи будут перезаписаны.
    2. Функция не поддерживает словари с нехэшируемыми значениями (например, списками или множествами).
    3. Используется для упрощения двустороннего поиска в словарях с уникальными значениями.

    Examples
    --------
    >>> invert_dict({'a': 1, 'b': 2})
    {1: 'a', 2: 'b'}

    >>> invert_dict({'x': 'val', 'y': 'val'})
    {'val': 'y'}  # Второй ключ перезаписывает первый

    References
    ----------
    .. [1] Python Software Foundation. "Python Language Reference", version 3.11.
    .. [2] Beazley, D.M. "Python Essential Reference", 4th edition.
    """
    return {value: key for key, value in d.items()}
####################################################################################
from .ml.additional_funcs import *