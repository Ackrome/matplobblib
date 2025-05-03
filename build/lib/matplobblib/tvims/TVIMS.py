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

funcs_dicts = [dict([(get_task_from_func(i), i) for i in module]) for module in modules]
funcs_dicts_ts = [dict([(get_task_from_func(i,True), i) for i in module]) for module in modules]
funcs_dicts_full = [dict([(i.__name__, getsource(i)) for i in module]) for module in modules]


themes_list_funcs = dict([(names[i],list(funcs_dicts[i].values()) ) for i in range(len(names))]) # Название темы : список функций по теме
themes_list_dicts = dict([(names[i],funcs_dicts[i]) for i in range(len(names))])                 # Название темы : словарь по теме, где ЗАДАНИЕ: ФУНКЦИИ
themes_list_dicts_full = dict([(names[i],funcs_dicts_full[i]) for i in range(len(names))])       # Название темы : словарь по теме, где НАЗВАНИЕ ФУНКЦИИ: ТЕКСТ ФУНКЦИИ


# Тема -> Функция -> Задание
def description(dict_to_show = themes_list_funcs, key=None, show_only_keys:bool = False, show_keys_second_level:bool = True, n_symbols:int = 32,to_print:bool = True):
    """
    Печатает информацию о заданиях и функциях 
    
    Parameters
    ----------
    dict_to_show : dict, optional
        словарь, который будет использоваться для поиска заданий, 
        по умолчанию themes_list_funcs
    key : str, optional
        если dict_to_show - строка, то key - это ключ, 
        по которому будет найден словарь в themes_list_dicts_full, 
        если key=None, то будет найден словарь по строке dict_to_show
    show_only_keys : bool, optional
        если True, то будет печататься только список keys, 
        если False, то будет печататься словарь с функциями, 
        по умолчанию False
    show_keys_second_level : bool, optional
        если True, то будет печататься информация о функциях, 
        если False, то будет печататься только список функций, 
        по умолчанию False
    n_symbols : int, optional
        количество символов, которое будет выведено, если show_keys_second_level=True, 
        по умолчанию 20
    to_print : bool, optional
        вывести текст через `print` или нет
        
    
    Returns
    -------
    None
    """
    if dict_to_show=='Вывести функцию буфера обмена':
            return print(enable_ppc)
    
    else:
        if type(dict_to_show) == str and key==None:
                dict_to_show = themes_list_dicts[dict_to_show] # Теперь это словарь ЗАДАНИЕ : ФУНКЦИЯ
                dict_to_show = invert_dict(dict_to_show)       # Теперь это словарь ФУНКЦИЯ : ЗАДАНИЕ
                text = ""
                length1=1+max([len(x.__name__) for x in list(dict_to_show.keys())])
                
                for key in dict_to_show.keys():
                    text += f'{key.__name__:<{length1}}'
                    
                    if not show_only_keys:
                        text +=': '
                        text += f'{dict_to_show[key]};\n'+' '*(length1+2)
                    text += '\n'
                    
                if to_print == True:
                    return print(text)
                return text
        
        elif type(dict_to_show) == str and key in themes_list_dicts_full[dict_to_show].keys():
            return print(themes_list_dicts_full[dict_to_show][key])
        
        else:
            show_only_keys=False
        text = ""
        length1=1+max([len(x) for x in list(dict_to_show.keys())])
        
        for key in dict_to_show.keys():
            text += f'{key:^{length1}}'
            if not show_only_keys:
                text +=': '
                for f in dict_to_show[key]:
                    text += f'{f.__name__}'
                    if show_keys_second_level:
                        text += ': '
                        func_text_len = len(invert_dict(themes_list_dicts[key])[f])
                        func_text = invert_dict(themes_list_dicts[key])[f]
                        text += func_text.replace('\n','\n'+' '*(length1 + len(f.__name__))) if func_text_len<n_symbols else func_text[:n_symbols].replace('\n','\n'+' '*(length1 + len(f.__name__)))+'...'
                    text += ';\n'+' '*(length1+2)
            text += '\n'
            
        if to_print == True:
            return print(text)
        return text

def search(query: str, to_print: bool = True, data: str = description(n_symbols=10000, to_print=False)):
        """
        Осуществляет поиск совпадений в описании функций среди строк формата:
        "Тема : функция : описание; функция : описание;"

        Args:
                data (str): Исходная строка с данными.
                query (str): Строка для поиска.
                to_print (bool): вывести ответы через print.

        Returns:
                list: Список совпадений в формате "Тема : функция : описание".
        """
        # Разделение данных на темы
        topics = re.split(r'\n\s*\n', data)
        matches = []

        for topic_data in topics:
                if not topic_data.strip():
                        continue

                # Извлечение темы
                topic_match = re.match(r'^\s*(.*?):', topic_data)
                if not topic_match:
                        continue

                topic = topic_match.group(1).strip()

                # Поиск функций и описаний в теме
                functions = re.findall(r'(\w+)\s*:\s*([\s\S]*?)(?=\n\s*\w+\s*:|\Z)', topic_data)

                for func, description in functions:
                        if query.lower() in description.lower():
                                matches.append(f"{topic} : {description.strip()}")

        
        if to_print:
                return print("\n".join(matches))
        return matches