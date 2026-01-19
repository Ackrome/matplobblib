import re
from ..forall import *
from .fpb import *                      # Формулы полной вероятности и Байеса
from .sdrv import *                     # Специальные дискретные случайные величины
from .crv import *                      # Непрерывные случайные величины
from .nrv import *                      # Нормальные случайные векторы
from .anrv import *                     # Нормальные случайные векторы ДОПОЛНИТЕЛЬНЫЙ ПАКЕТ ФУНКЦИЙ
from .cce import *                      # Условные характеристики относительно группы событий
from .acmk import *                     # Приближенное вычисление вероятности методом Монте-Карло
from .pan import *                      # Портфельный анализ с невырожденной ковариационной матрицей
from .dt import *                       # Описательная статистика
from .ec import *                       # Эмперические характеристики
from .sffp import *                     # Выборки из конечной совокупности
from .mlm import *                      # Метод максимального правдоподобия
from .tmh import *                      # Проверка гипотез о значении среднего
from .tvh import *                      # Проверка гипотез о значении дисперсии
from .tsm import *                      # Проверка гипотезы о состоянии двух и трёх средних
from .cicc import *                     # Доверительный интервал для коэффициента корреляции
from .theory import *                   # Теоретические материалы

def printcolab():
    """Выводит ссылку на знакомый гугл колаб(google colab)"""
    print(r'https://colab.research.google.com/drive/1QjC3HnOivbi-38CvI7c9wq0mAYuXNQei?usp=sharing')
    return r'https://colab.research.google.com/drive/1QjC3HnOivbi-38CvI7c9wq0mAYuXNQei?usp=sharing'

def imports():
    """
    Возвращает строку, содержащую инструкции импорта Python для различных научных библиотек. 
    Эти библиотеки обычно используются для математических вычислений, символьной математики, 
    и комбинаторные операции с инициализацией SymPy для красивой печати с использованием Unicode. 
    и форматирование LaTeX.
    """
    print('''
    
from scipy.integrate import quad
import math
import numpy as np
import sympy
import itertools
sympy.init_printing(use_unicode=True,use_latex=True)
    ''')
    return '''
    
from scipy.integrate import quad
import math
import numpy as np
import sympy
import itertools
sympy.init_printing(use_unicode=True,use_latex=True)
    '''

UF = [printcolab,imports]

files_dict ={
    'Полезные функции': UF,
    'Теоретические материалы':THEORY,
    'Формулы полной вероятности и Байеса':FPB,
    'Специальные дискретные случайные величины':SDRV,
    'Непрерывные случайные величины':CRV,
    'Нормальные случайные векторы':NRV,
    'Нормальные случайные векторы ДОПОЛНИТЕЛЬНЫЙ ПАКЕТ ФУНКЦИЙ':ANRV,
    'Условные характеристики относительно группы событий':CCE,
    'Приближенное вычисление вероятности методом Монте-Карло':ACMK,
    'Портфельный анализ с невырожденной ковариационной матрицей':PAN,
    'Описательная статистика':DT,
    'Эмперические характеристики':EC,
    'Выборки из конечной совокупности':SFFP,
    'Метод максимального правдоподобия':MLM,
    'Проверка гипотез о значении среднего':TMH,
    'Проверка гипотез о значении дисперсии': TVH,
    'Проверка гипотезы о состоянии двух и трёх средних': TSM,
    'Доверительный интервал для коэффициента корреляции':CICC
}

names = list(files_dict.keys())
modules = list(files_dict.values())


    
def enable_ppc():
    """
    Returns a string containing a Python script that uses the pyperclip module to
    define a function named `write`. The `write` function takes a single argument `name`,
    copies it to the system clipboard, and pastes it using pyperclip.
    """
    return'''
import pyperclip

#Делаем функцию которая принимает переменную text
def write(name):
    pyperclip.copy(name) #Копирует в буфер обмена информацию
    pyperclip.paste()'''
    
def invert_dict(d):
    """
    Returns a new dictionary with the keys and values of the input dictionary swapped.
    
    Example:
        >>> invert_dict({1: 'a', 2: 'b'})
        {'a': 1, 'b': 2}
    """
    return {value: key for key, value in d.items()}

# Создание словарей функций для каждой темы
# funcs_dicts: {описание_задачи: функция}
funcs_dicts = [dict([(get_task_from_func(i), i) for i in module]) for module in modules]
# funcs_dicts_ts: {описание_задачи_без_пробелов_и_переносов: функция} (ts - to_search)
funcs_dicts_ts = [dict([(get_task_from_func(i,True), i) for i in module]) for module in modules]
# funcs_dicts_full: {имя_функции: исходный_код_функции}
funcs_dicts_full = [dict([(i.__name__, getsource(i)) for i in module]) for module in modules]
# funcs_dicts_full_nd: {имя_функции: исходный_код_функции_без_документации}
funcs_dicts_full_nd = [dict([(i.__name__, getsource_no_docstring(i)) for i in module]) for module in modules]

# Создание словарей, группирующих функции по темам
themes_list_funcs = dict([(names[i],list(funcs_dicts[i].values()) ) for i in range(len(names))])        # Название темы : список функций по теме
themes_list_dicts = dict([(names[i],funcs_dicts[i]) for i in range(len(names))])                        # Название темы : словарь по теме, где ЗАДАНИЕ: ФУНКЦИИ
themes_list_dicts_full = dict([(names[i],funcs_dicts_full[i]) for i in range(len(names))])              # Название темы : словарь по теме, где НАЗВАНИЕ ФУНКЦИИ: ТЕКСТ ФУНКЦИИ
themes_list_dicts_full_nd = dict([(names[i],funcs_dicts_full_nd[i]) for i in range(len(names))])        # Название темы : словарь по теме, где НАЗВАНИЕ ФУНКЦИИ: ТЕКСТ ФУНКЦИИ БЕЗ ДОКУМЕНТАЦИИ


# Тема -> Функция -> Задание
def description(
    dict_to_show=themes_list_funcs,
    key=None,
    show_only_keys: bool = False,
    show_keys_second_level: bool = True,
    n_symbols: int = 32,
    to_print: bool = True,
    show_doc = False):
    """
    Отображает информацию о доступных функциях и темах в модуле TViMS.

    Функция предоставляет несколько режимов для просмотра содержимого модуля:
    - Показать все темы и функции в них.
    - Показать функции в рамках одной темы.
    - Показать исходный код конкретной функции.

    Args:
        dict_to_show (str or dict, optional): Словарь для отображения или название темы.
            По умолчанию `themes_list_funcs`.
        key (hashable, optional): Ключ для фильтрации (например, имя функции).
        show_only_keys (bool, optional): Если True, показывать только ключи (названия тем).
            По умолчанию False.
        show_keys_second_level (bool, optional): Если True, показывать ключи второго уровня (названия функций).
            По умолчанию True.
        n_symbols (int, optional): Максимальное количество символов для описания.
            По умолчанию 32.
        to_print (bool, optional): Если True, выводит результат в консоль. Иначе возвращает строку.
            По умолчанию True.
        show_doc (bool, optional): Если True, показывает полный исходный код функции с документацией.
            По умолчанию False.

    Returns:
        str or None: Форматированная строка с информацией, если `to_print` равно False.
            В противном случае None.

    Examples:
        >>> # Показать только названия тем в модуле TViMS
        >>> description(show_only_keys=True)

        >>> # Показать функции и их краткое описание для темы 'Описательная статистика'
        >>> description('Описательная статистика')

        >>> # Показать исходный код функции 'describe_text'
        >>> description('Описательная статистика', key='describe_text', show_doc=True)

    Notes:
        - Функция использует предопределенные словари `themes_list_funcs`, `themes_list_dicts` и др.
          для доступа к метаданным функций.
        - Для корректного отображения длинных описаний используется автоматический перенос строк.
    """
    
    # Если dict_to_show - строка (название темы) и не указан конкретный ключ (key)
    if type(dict_to_show) == str and key == None:
        dict_to_show = themes_list_dicts[dict_to_show]
        dict_to_show = invert_dict(dict_to_show)
        text = ""
        length1 = 1 + max([len(x.__name__) for x in list(dict_to_show.keys())])
        
        for key in dict_to_show.keys():
            text += f'{key.__name__:<{length1}}' # Имя функции, выровненное по левому краю
            
            if not show_only_keys:
                text += ': '
                text += f'{dict_to_show[key]};\n' + ' '*(length1+2) # Описание задачи
            text += '\n'
            
        if to_print == True:
            return print(text)
        return text
    
    # Если dict_to_show - строка (название темы) и указан конкретный ключ (имя функции)
    elif type(dict_to_show) == str and key in themes_list_dicts_full[dict_to_show].keys():
        if show_doc:
            return print(themes_list_dicts_full[dict_to_show][key]) # Вывод исходного кода функции
        else:
            return print(themes_list_dicts_full_nd[dict_to_show][key]) # Вывод исходного кода функции
    
    else:
        show_only_keys = False
    text = ""
    length1 = 1 + max([len(x) for x in list(dict_to_show.keys())]) # Максимальная длина ключа первого уровня (названия темы)
    
    for key in dict_to_show.keys():
        text += f'{key:^{length1}}' # Название темы, выровненное по центру
        if not show_only_keys:
            text += ': '
            for f in dict_to_show[key]:
                text += f'{f.__name__}'
                if show_keys_second_level:
                    text += ': '
                    try:
                        # Получение описания функции из инвертированного словаря
                        func_text_len = len(invert_dict(themes_list_dicts[key])[f])
                        
                        # Форматирование описания с переносами строк и ограничением по длине
                        func_text = invert_dict(themes_list_dicts[key])[f]
                        text += func_text.replace('\n','\n'+' '*(length1 + len(f.__name__))) if func_text_len < n_symbols else func_text[:n_symbols].replace('\n','\n'+' '*(length1 + len(f.__name__)))+'...'
                    except:
                        pass # Пропуск, если описание не найдено
                text += ';\n' + ' '*(length1+2) # + '\n' + ' '*(length1+2)
        text += '\n'
        
    if to_print == True:
        return print(text)
    return text



def search(query: str, to_print: bool = True, data: str = description(n_symbols=10000, to_print=False)):
    """
    Ищет функции в модуле TViMS по ключевым словам в их описаниях.

    Функция выполняет регистронезависимый поиск по описаниям всех доступных
    элементов и выводит найденные совпадения.

    Args:
        query (str): Строка для поиска. Может быть частью слова или фразой.
        to_print (bool, optional): Если True, результат выводится в консоль.
            Иначе возвращается в виде списка строк. По умолчанию True.
        data (str, optional): Строка с данными для поиска, обычно результат
            вызова `description(to_print=False)`. По умолчанию генерируется
            автоматически.

    Returns:
        list or None: Список найденных строк в формате "Тема : Описание",
            если `to_print` равно False. В противном случае None.

    Examples:
        >>> # Найти все, что связано с гипотезами
        >>> search("гипотез")

        >>> # Найти функции для работы с распределениями и вернуть результат в виде списка
        >>> results = search("распределен", to_print=False)
        >>> print(results)

    Notes:
        - Поиск чувствителен к структуре данных, предоставляемых функцией `description`.
        - Для полного поиска по всем описаниям `description` вызывается с `n_symbols=10000`.
    """
    # Разделение входных данных на отдельные темы
    topics = re.split(r'\n\s*\n', data)
    matches = []

    for topic_data in topics:
        # Пропуск пустых блоков тем
        if not topic_data.strip():
            continue

        topic_match = re.match(r'^\s*(.*?):', topic_data)
        if not topic_match:
            continue
        
        # Извлечение названия темы
        topic = topic_match.group(1).strip()
        # Поиск всех функций и их описаний в текущей теме
        functions = re.findall(r'(\w+)\s*:\s*([\s\S]*?)(?=\n\s*\w+\s*:|\Z)', topic_data)

        for func, description in functions:
            # Проверка наличия запроса (без учета регистра) в описании функции
            if query.lower() in description.lower():
                matches.append(f"{topic} : {description.strip()}")
    
    # Вывод результатов или их возврат списком
    if to_print:
        return print("\n".join(matches))
    return matches