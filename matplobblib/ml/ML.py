from  inspect import getsource
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######################################################################################################################
from .rm import *                       # Модификации линейной регрессионной модели
from .cm import *                       # Модификации модели классификации
from .additional_funcs import *         # Дополнительные функции
from .trees import *                    # Деревья


files_dict ={
    'Модификации линейной регрессионной модели': RM,
    'Модификации модели классификации': CM,
    'Дополнительные функции' : AF,
    'Реализация дерева решений' : TREES,
    
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
    
def invert_dict(d):
    return {value: key for key, value in d.items()}

def get_task_from_func(func,to_search=False):
    return re.search(r'"""\s*(.*?)\s*(?=def __init__|Args)',getsource(func),re.DOTALL).group(0)[3:-4].replace('\n','').replace(' ','') if to_search else re.search(r'"""\s*(.*?)\s*(?=def __init__|Args)',getsource(func),re.DOTALL).group(0)[3:-4]


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