from .data_structures import *
from  .search_algorythms import *
from .additional_funcs import *

data1 = text1.split('abracadabrabibidi')
data_structures_dict = dict([(x.split('\n')[1].replace("# ",''),x) for x in data1])
data2 = text2.split('abracadabrabibidi')
search_algorythms_dict = dict([(x.split('\n')[1].replace("# ",''),x) for x in data2])
data3 = text3.split('abracadabrabibidi')
additional_funcs_dict = dict([(x.split('\n')[1].replace("# ",''),x) for x in data3])

themes = {
        'Структуры данных': list(data_structures_dict.keys()),
        'Алгоритмы сортировки': list(search_algorythms_dict.keys()),
        'Дополнительные функции' : list(additional_funcs_dict.keys()),
        'Вывести функцию буфера обмена': ['enable_ppc'],
              }
# Тема -> Выбор структуры -> структура
def description(dict_to_show = themes, key=None, show_only_keys:bool = True):
    if dict_to_show=='Вывести функцию буфера обмена':
            return print(enable_ppc)
        
    elif type(dict_to_show) == str and dict_to_show!='Вывести функцию буфера обмена' and key==None:
            dict_to_show = {
            'Структуры данных': data_structures_dict,
            'Алгоритмы сортировки': search_algorythms_dict,
            'Дополнительные функции' : additional_funcs_dict,
                }[dict_to_show]
            
            text = ""
            length1=1+max([len(x) for x in list(dict_to_show.keys())])
            for key in dict_to_show.keys():
                text += f'{key:<{length1}}\n'
                
            return print(text)
        
    elif type(dict_to_show) == str and dict_to_show!='Вывести функцию буфера обмена' and key in list({
            'Структуры данных': data_structures_dict,
            'Алгоритмы сортировки': search_algorythms_dict,
            'Дополнительные функции' : additional_funcs_dict,
                }[dict_to_show].keys()):
        
        return print({
            'Структуры данных': data_structures_dict,
            'Алгоритмы сортировки': search_algorythms_dict,
            'Дополнительные функции' : additional_funcs_dict,
                }[dict_to_show][key])
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

def enable_ppc():
    return '''import pyperclip

#Делаем функцию которая принимает переменную text
def write(name):
    pyperclip.copy(name) #Копирует в буфер обмена информацию
    pyperclip.paste()'''
