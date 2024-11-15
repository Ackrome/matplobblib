from  inspect import getsource
import re
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

files_dict ={
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
    'Выборки из конечной совокупности':SFFP
}

names = list(files_dict.keys())
modules = list(files_dict.values())

def imports():
    """
    Returns a string containing Python import statements for various scientific libraries. 
    These libraries are commonly used for mathematical computations, symbolic mathematics, 
    and combinatorial operations, with SymPy initialized for pretty printing using Unicode 
    and LaTeX formatting.
    """
    return '''
    
from scipy.integrate import quad
import math
import numpy as np
import sympy
import itertools
sympy.init_printing(use_unicode=True,use_latex=True)
    '''
    
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

def get_task_from_func(func,to_search=False):
    """
    Returns the task associated with the given function.
    
    Parameters:
        func : callable
            The function whose task we want to find.
        to_search : bool, optional
            If True, returns a string that can be used to search for the task by name.
            If False, returns the task itself. Defaults to False.
    
    Returns:
        str or callable
            The task associated with the function, or a string that can be used to search for it.
    """
    return re.search(r'""".*?Args',getsource(func),re.DOTALL).group(0)[3:-4].replace('\n','').replace(' ','') if to_search else re.search(r'""".*?Args',getsource(func),re.DOTALL).group(0)[3:-4]


funcs_dicts = [dict([(get_task_from_func(i), i) for i in module]) for module in modules]
funcs_dicts_ts = [dict([(get_task_from_func(i,True), i) for i in module]) for module in modules]
funcs_dicts_full = [dict([(i.__name__, getsource(i)) for i in module]) for module in modules]


themes_list_funcs = dict([(names[i],list(funcs_dicts[i].values()) ) for i in range(len(names))]) # Название темы : список функций по теме
themes_list_dicts = dict([(names[i],funcs_dicts[i]) for i in range(len(names))])                 # Название темы : словарь по теме, где ЗАДАНИЕ: ФУНКЦИИ
themes_list_dicts_full = dict([(names[i],funcs_dicts_full[i]) for i in range(len(names))])       # Название темы : словарь по теме, где НАЗВАНИЕ ФУНКЦИИ: ТЕКСТ ФУНКЦИИ


# Тема -> Функция -> Задание
def description(dict_to_show = themes_list_funcs, key=None, show_only_keys:bool = False, show_keys_second_level:bool = True, n_symbols:int = 32):
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
                    
                return print(text)
        
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
        return print(text)