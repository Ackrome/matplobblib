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

names = ['Формулы полной вероятности и Байеса',
 'Специальные дискретные случайные величины',
 'Непрерывные случайные величины',
 'Нормальные случайные векторы',
 'Нормальные случайные векторы ДОПОЛНИТЕЛЬНЫЙ ПАКЕТ ФУНКЦИЙ',
 'Условные характеристики относительно группы событий',
 'Приближенное вычисление вероятности методом Монте-Карло',
 'Портфельный анализ с невырожденной ковариационной матрицей',
 'Описательная статистика'
 ]

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

FPB_dict_ts = dict([(get_task_from_func(i,True), i) for i in FPB])
SDRV_dict_ts =dict([(get_task_from_func(i,True), i)  for i in SDRV])
CRV_dict_ts =dict([(get_task_from_func(i,True), i)  for i in CRV])
NRV_dict_ts =dict([(get_task_from_func(i,True), i)  for i in NRV])
ANRV_dict_ts =dict([(get_task_from_func(i,True), i)  for i in ANRV])
CCE_dict_ts =dict([(get_task_from_func(i,True), i)  for i in CCE])
ACMK_dict_ts = dict([(get_task_from_func(i,True), i)for i in ACMK])
PAN_dict_ts = dict([(get_task_from_func(i,True), i)  for i in PAN])
DT_dict_ts = dict([(get_task_from_func(i,True), i)  for i in DT])

FPB_dict = dict([(get_task_from_func(i), i) for i in FPB] )
SDRV_dict = dict([(get_task_from_func(i), i)  for i in SDRV]) 
CRV_dict = dict([(get_task_from_func(i), i)  for i in CRV] )
NRV_dict = dict([(get_task_from_func(i), i) for i in NRV]) 
ANRV_dict = dict([(get_task_from_func(i), i)  for i in ANRV] )
CCE_dict = dict([(get_task_from_func(i), i) for i in CCE] )
ACMK_dict = dict([(get_task_from_func(i), i) for i in ACMK] )
PAN_dict = dict( [(get_task_from_func(i), i) for i in PAN] )
DT_dict = dict([(get_task_from_func(i), i)  for i in DT] )

funcs_ts_dicts = [FPB_dict_ts,SDRV_dict_ts,CRV_dict_ts,NRV_dict_ts,ANRV_dict_ts,CCE_dict_ts,ACMK_dict_ts,PAN_dict_ts,DT_dict_ts]
funcs_dicts    = [FPB_dict,SDRV_dict,CRV_dict,NRV_dict,ANRV_dict,CCE_dict,ACMK_dict,PAN_dict,DT_dict]

themes_list_funcs = dict([(names[i],list(funcs_ts_dicts[i].values()) ) for i in range(len(names))]) # Название темы : список функций по теме
themes_list_dicts = dict([(names[i],funcs_dicts[i]) for i in range(len(names))])                    # Название темы : словарь по теме, где ЗАДАНИЕ: ФУНКЦИИ


# Тема -> Функция -> Задание
def description(dict_to_show = themes_list_funcs, key=None, show_only_keys:bool = True):
    if dict_to_show=='Вывести функцию буфера обмена':
            return print(enable_ppc)
    
    else:
        if type(dict_to_show) == str and key==None:
                dict_to_show = themes_list_dicts[dict_to_show] # Теперь это словарь ЗАДАНИЕ : ФУНКЦИЯ
                dict_to_show = invert_dict(dict_to_show)       # Теперь это словарь ФУНКЦИЯ : ЗАДАНИЕ
                text = ""
                length1=1+max([len(x.__name__) for x in list(dict_to_show.keys())])
                
                for key in dict_to_show.keys():
                    text += f'{key.__name__:<{length1}}\n'
                    
                return print(text)
            
        elif type(dict_to_show) == str and key in [i.__name__ for i in list(invert_dict(themes_list_dicts[dict_to_show]).keys())]:
            cdict = dict(list(zip([i.__name__ for i in list(invert_dict(themes_list_dicts[dict_to_show]).keys())], [list(invert_dict(themes_list_dicts[dict_to_show]).values())])))
            return print(cdict[key])
        
        else:
            show_only_keys=False
        text = ""
        length1=1+max([len(x) for x in list(dict_to_show.keys())])
        for key in dict_to_show.keys():
            text += f'{key:^{length1}}'
            if not show_only_keys:
                text +=': '
                for f in dict_to_show[key]:
                    text += f'{f};\n'+' '*(length1+2)
            text += '\n'
        print(text)