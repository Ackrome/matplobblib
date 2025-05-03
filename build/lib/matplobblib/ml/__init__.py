#######################################################################################################################
import re
import pandas as pd
import matplotlib.pyplot as plt
from ..forall import *
#######################################################################################################################
from .rm import *                       # Модификации линейной регрессионной модели
from .logreg import *                       # Модификации модели классификации
from .additional_funcs import *         # Дополнительные функции
from .tree import *                     # Деревья
from .svc import *                      # Классификатор методом опорных векторов
from .knn import *                       # K-nn
from .randomforrest import *            # Случайный лес
from .nbc import *                      # Наивный байесовский классификатор

pattern = r'"""\s*(.*?)\s*(?=def __init__|Args|Параметры)'

files_dict ={
    'Дополнительные функции' : AF,
    'Модификации линейной регрессионной модели': RM,
    'Модель Логистической регрессии': CM,
    'Реализация дерева решений' : TREES,
    'Классификатор методом опорных векторов' : SVCS,
    'К-ближайших соседей': KNNS,
    'Случайный лес': RF,
    'Наивный байесовский классификатор': NBC
}

names = list(files_dict.keys())
modules = list(files_dict.values())

def imports():
    return '''
    
    from scipy.integrate import quad
    import math
    import numpy a np
    import sympy
    import itertools
    sympy.init_printing(use_unicode=True,use_latex=True)
    '''
    
def enable_ppc():
    return'''
import pyperclip

#Делаем функцию которая принимает переменную text
def write(name):
    pyperclip.copy(name) #Копирует в буфер обмена информацию
    pyperclip.paste()'''
    


funcs_dicts = [
    dict([
        (task, func) for func in module
        if (task := get_task_from_func(func)) is not None
    ])
    for module in modules
]
funcs_dicts_ts = [
    dict([
        (task, func) for func in module
        if (task := get_task_from_func(func, True)) is not None
    ])
    for module in modules
]
funcs_dicts_full = [dict([(i.__name__, getsource(i)) for i in module]) for module in modules]


themes_list_funcs = dict([(names[i],list(funcs_dicts[i].values()) ) for i in range(len(names))]) # Название темы : список функций по теме
themes_list_dicts = dict([(names[i],funcs_dicts[i]) for i in range(len(names))])                 # Название темы : словарь по теме, где ЗАДАНИЕ: ФУНКЦИИ
themes_list_dicts_full = dict([(names[i],funcs_dicts_full[i]) for i in range(len(names))])       # Название темы : словарь по теме, где НАЗВАНИЕ ФУНКЦИИ: ТЕКСТ ФУНКЦИИ


# Тема -> Функция -> Задание
def description(dict_to_show = themes_list_funcs, key=None, show_only_keys:bool = False, show_keys_second_level:bool = True, n_symbols:int = 32, to_print=True):
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
        позволяет вывести строковое значение описания
    
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
                    
                return print(text) if to_print else text
        
        elif type(dict_to_show) == str and key in themes_list_dicts_full[dict_to_show].keys():
            return print(themes_list_dicts_full[dict_to_show][key]) if to_print else themes_list_dicts_full[dict_to_show][key]
        
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
        return print(text) if to_print else text