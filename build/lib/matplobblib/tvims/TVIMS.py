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

names = ['Формулы полной вероятности и Байеса',
 'Специальные дискретные случайные величины',
 'Непрерывные случайные величины',
 'Нормальные случайные векторы',
 'Нормальные случайные векторы ДОПОЛНИТЕЛЬНЫЙ ПАКЕТ ФУНКЦИЙ',
 'Условные характеристики относительно группы событий',
 'Приближенное вычисление вероятности методом Монте-Карло',
 'Портфельный анализ с невырожденной ковариационной матрицей',
 'Описательная статистика',
 'Эмперические характеристики'
 ]

modules = [FPB,SDRV,CRV,NRV,ANRV,CCE,ACMK,PAN,DT, EC]

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
    return re.search(r'""".*?Args',getsource(func),re.DOTALL).group(0)[3:-4].replace('\n','').replace(' ','') if to_search else re.search(r'""".*?Args',getsource(func),re.DOTALL).group(0)[3:-4]


funcs_dicts = [dict([(get_task_from_func(i), i) for i in module]) for module in modules]
funcs_dicts_ts = [dict([(get_task_from_func(i,True), i) for i in module]) for module in modules]
funcs_dicts_full = [dict([(i.__name__, getsource(i)) for i in module]) for module in modules]


themes_list_funcs = dict([(names[i],list(funcs_dicts[i].values()) ) for i in range(len(names))]) # Название темы : список функций по теме
themes_list_dicts = dict([(names[i],funcs_dicts[i]) for i in range(len(names))])                 # Название темы : словарь по теме, где ЗАДАНИЕ: ФУНКЦИИ
themes_list_dicts_full = dict([(names[i],funcs_dicts_full[i]) for i in range(len(names))])       # Название темы : словарь по теме, где НАЗВАНИЕ ФУНКЦИИ: ТЕКСТ ФУНКЦИИ


# Тема -> Функция -> Задание
def description(dict_to_show = themes_list_funcs, key=None, show_only_keys:bool = False):
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
                    text += f'{f.__name__};\n'+' '*(length1+2)
            text += '\n'
        return print(text)