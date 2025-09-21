from ...forall import *

FLS = []

def fls1():
    '''Загрузите названия рецептов из файла
preprocessed_descriptions.csv
(первая колонка). Получите набор уникальных слов в названиях. Получите набор из 5 ближайших слов к слову "black'. (Близость слов измеряется с помощью расстояния Левенштейна).'''
    print("""import pandas as pd
    import re
    from collections import Counter
    from Levenshtein import distance as levenshtein_distance

    df = pd.read_csv('preprocessed_descriptions.csv', usecols = [0], header = None, names = ['title'])
    titles = df['title'].tolist()
    test = ' '.join(titles)
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words = set(words)
    print(len(unique_words))

    targer_word = 'black'
    word_distances = {}
    for word in unique_words:
        distance_value = distance(target_word, word)
        word_distances[word] = distance_value
        sorted_words = sorted(word_distance.items(), key = lambda item: item[1])
        closest_words = sorted_words[:6]

    print(target_word)
    for word, dist in closest_words:
        print(word, dist)""")
    

def fls2():
    '''В файле 'average_ratings.npy содержится информация о среднем рейтинге 3 рецептов за период с 01.01.2019 по 30.12.2021. При помощи пакета 'matplotlib в одной системе координат (на одной картинке) изобразите три временных ряда, соответствующих средним рейтингам этих рецептов'''
    print("""import numpy as np
import matplotlib.pyplot as plt
import datetime

average_rating = np.load('average_ratinds.npy')
start_date = datetime.date(2019, 1, 1)
dates = [start_date + datetime.timedelta(days = i) for i in range(average_ratinds.shape[1])]
plt.figure(figsize = (12, 6))
for i in range(average_ratings.shape[0]):
    plt.plot(dates, average_ratings[i], label = f'Рецепт {i + 1}')
plt.xlabels('Дата')
plt.ylabel('Средний рейтинг')
plt.title('Средний рейтинг рецептов по времени')
plt.grid(True)
plt.legend()
plt.tught_layout()
plt.show()
    """)


def fls3():
    '''Напишите регулярное выражение, которое ищет в приведенном ниже тексте нумерацию, затем точку, затем первое слово после точки.'''
    print("""import re

text = (тут должны быть тройные кавычки)
Bavarian apple cheesecake tart
1. mix butter , flour , 1 / 3 c
2. sugar and 1-1 / 4 t
3. vanilla
4. press into greased 9" springform pan
5. mix cream cheese , 1 / 4 c
6. sugar , eggs and 1 / 2 t
7. vanilla beating until fluffy
8. pour over dough
9. combine apples , 1 / 3 c
10. sugar and cinnamon
11. arrange on top of cream cheese mixture and sprinkle with almonds
12. bake at 350 for 45-55 minutes , or until tester comes out clean
(тут должны быть тройные кавычки)

pattern = r"(\d+\.\s*\w+)"
matches = re.findall(pattern, text)
print(matches)""")
    
def fls4():
    '''НВ файле 'average ratings.npy содержится информация о среднем рейтинге 3 рецептов за период с 01.01.2019 по 30.12.2021. При помощи пакета 'matplotlib в одной системе координат (на одной картинке) изобразите три временных ряда, соответствующих средним рейтингам этих рецептов.'''
    print("""import numpy as np
import matplotlib.pyplot as plt
import datetime

average_ratings = np.load('average_ratings.npy')
start_date = datetime.date(2019, 1, 1)
dates = [start_date + datetime.timedelta(days = i) for i in range(average_ratings.shape[1])]
plt.fiaure(figsize = (12, 6))
for i in range(average_ratings.shape[0]):
    plt.plot(dates, average_ratings[i], label = f"Рецепт {i + 1}")
plt.xlabel('Дата')
plt.ylabel('Средний рейтинг')
plt.title('Средний рейтинг рецептов во времени')
plt.grid(True)
plt.legend() 
plt.tight_layout()  
plt.show()""")    

def fls5():
    '''При помощи объединения таблиц, создайте DataFrame, состоящий из четырех столбцов: id, name, date, review. Рецепты без отзывов должны отсутствовать в данной таблице. Создайте новый DataFrame, состоящий их записей не старше 2015 года и состоящий из двух столбцов, где первый это id рецепта, а второй - столбец, хранящий количество отзывов на рецепт.'''
    print("""data = {
    'id': [1, 1, 2, 3, 3, 3, 4, 5],  # У рецептов 1 и 3 по несколько отзывов
    'name': ['Яблочный пирог', 'Яблочный пирог', 'Кремовый пирог', 'Чизкейк', 'Чизкейк', 'Чизкейк', 'Панна-котта', 'Медовой'],
    'date': ['2014-03-15', '2014-03-15', '2016-07-20', '2013-11-10', '2013-11-10', '2013-11-10', '2015-05-30', '2017-02-14'],
    'review': ['Вкусно!', 'Пальчики оближешь!', 'Без комментариев', 'Отлично', 'Супер', 'Нежный', 'Превосходно', 'Збс']
}

df = pd.DataFrame(data).dropna(subset=['review'])
print("Исходный DataFrame (без рецептов без отзывов):")
print(df)""")   
    
def fls6():
    '''Загрузите названия рецептов из файла
ргеprocessed_descriptions.csv
(первая колонка). Получите набор уникальных слов в названиях. Получите набор из 5 ближайших слов к слову "black'. (Близость слов измеряется с помощью расстояния Левенштейна).'''
    print("""import pandas as pd
import re
from collections import Counter
from Levenshtein import distance as levenshtein_distance

df = pd.read_csv('preprocessed_descriptions.csv', usecols = [0], header = None, names = ['title'])
titles = df['title'].tolist()
test = ' '.join(titles)
words = re.findall(r'\b\w+\b', text.lower())
unique_words = set(words)
print(len(unique_words))

targer_word = 'black'
word_distance = {}
for word in unique_words:
    distance_value = distance(target_word, word)
    word_distances[word] = distance_value
    sorted_words = sorted(word_distance.items(), key = lambda item: item[1])
    closest_words = sorted_words[:6]
print(targer_word)
for word, dist in closest_words:
    print(word, dist)""")   

def fls7():
    '''Постройте кривые синуса, косинуса, тангенса, функции х в квадрате их в кубе на четырех графиках в два ряда и два столбца, задайте им разные цвета и стили линий. Задайте решетку и общий заголовок.'''
    print("""import matplotlib.pyplot as plt

x = np.linspace(-2*np.pi, 2*np.pi, 200)


y_sin = np.sin(x)
y_cos = np.cos(x)
y_tan = np.tan(x)
y_square = x**2
y_cube = x**3


styles = {
    'sin': {'color': 'blue', 'linestyle': '-', 'label': 'sin(x)'},
    'cos': {'color': 'red', 'linestyle': '--', 'label': 'cos(x)'},
    'tan': {'color': 'green', 'linestyle': ':', 'label': 'tan(x)'},
    'square': {'color': 'purple', 'linestyle': '-.', 'label': 'x²'},
    'cube': {'color': 'orange', 'linestyle': (0, (3, 1, 1, 1)), 'label': 'x³'}
}


fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Графики функций: sin(x), cos(x), tan(x), x², x³', fontsize=14)


axs[0, 0].plot(x, y_sin, **styles['sin'])
axs[0, 0].plot(x, y_cos, **styles['cos'])
axs[0, 0].set_title('Синус и Косинус')
axs[0, 0].grid(True)
axs[0, 0].legend()

y_tan_filtered = np.where(np.abs(y_tan) > 20, np.nan, y_tan)
axs[0, 1].plot(x, y_tan_filtered, **styles['tan'])
axs[0, 1].set_title('Тангенс')
axs[0, 1].grid(True)
axs[0, 1].legend()
axs[0, 1].set_ylim(-5, 5)


axs[1, 0].plot(x, y_square, **styles['square'])
axs[1, 0].set_title('Квадратичная функция')
axs[1, 0].grid(True)
axs[1, 0].legend()


axs[1, 1].plot(x, y_cube, **styles['cube'])
axs[1, 1].set_title('Кубическая функция')
axs[1, 1].grid(True)
axs[1, 1].legend()


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()""")   
    
def fls8():
    '''По данным файл steps_sample.xml сформируйте словарь с шагами по каждому рецепту вида {id рецепта: ["шаг\", \"шаг2\"]}'. Сохраните этот словарь в файл
steps_sample.json'''
    print("""import xml.etree.ElementTree as ET
import json

def process_xml(xml_file, json_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    recipes_dict = {}

    for recipe in root.findall('recipe'):
        recipe_id = recipe.get('id')
        steps = [step.text for step in recipe.findall('step')]
        recipes_dict[recipe_id] = steps

    with open(json_file, 'w', encoding = 'utf-8') as f:
        json.dump(recipes_dict, f, indent = 4, ensure_ascii = False)
        print(json_file)

xml_file = 'steps_sample.xml'
json_file = 'steps_sample.json'
process_xml(xml_file, json_file)""")   
    
def fls9():
    '''В файле 'average_ratings.ру содержится информация о среднем рейтинге 3 рецептов за период с 01.01.2019 по 30.12.2021. При помощи пакета 'matplotlib в одной системе координат (на одной картинке) изобразите три временных ряда, соответствующих средним рейтингам этих рецептов.'''
    print("""import numpy as np
import matplotlib.pyplot as plt
import datetime

data = np.load('average_ratings.npy')
start_date = datetime.data(2019, 1, 1)
end_date = datetime.data(2021, 12, 30)
num_days = (end_date - start_date).days + 1
time_scale = [start_date + datetime.timedelta(days = i) for i in range(num_days)]

plt.figure(figsixe = (12, 6))
plt.title('abiba', fontsize = 14)
plt.xlabel('Дата', fontsize = 12)
plt.ylabel('Средний рейтинг', fontsize = 12)
for i in range(data.shape[0]):
    plt.plot(time_scale, data[i, :], label = f"Рецепт {i + 1}")

plt.legend()
plt.grid(True)
plt.xticks(rotation = 45)
plt.tight_layout()
plt.show()""")   
    
def fls10():
    '''Файл 'minutes_n_ingredients.csv содержит информацию об идентификаторе рецепта, времени его выполнения в минутах и количестве необходимых ингредиентов. Считайте данные из этого файла в виде массива 'numpy типа 'int32, используя np.loadtxt'.
Выведите на экран первые 5 строк массива.'''
    print("""import numpy as np

data = np.loadtxt('minutes_n_ingredients.csv', delimiter = ',', dtype = np.int32)
print(data[:5])""")      
    
def fls11():
    '''В файле average_ratings.npy содержится информация о среднем рейтинге 3 рецептов за период с 01.01.2019 по 30.12.2021. При помощи пакета 'matplotlib в одной системе координат (на одной картинке) изобразите три временных ряда, соответствующих средним рейтингам этих рецептов.'''
    print("""import xml.etree.ElementTree as ET
import json

def process_xml(xnl_file, json_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    recipes_dict = {}

    for recipe in root.findall('recipe'):
        recipe_id = recipe.get('id')
        steps = [step.text for step in recipe.findall('step')]
        recipes_dict[recipe_id] = steps

    with open(json_file, 'w', encoding = 'utf-8') as f:
        json.dump(recipes_dict, f, indent = 4, ensure_ascii = False)
        print(json_file)

xml_file = 'steps_sample.xml'
json_file = 'steps_sample.json'
process_xml(xml_file, json_file)""") 
    
def fls12():
    '''По данным из файла 'addres-book-q.xml сформировать список словарей с телефонами
каждого из людей.'''
    print("""import xml.etree.ElementTree as ET

def process_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    adress_book = []
    for person in root.findall('person'):
        name = person.find('name').text
        phones = [phone.text for phone in person.findall('phone')]
        person_dict = {'name': name, 'phones': phones}
        adress_book.append(person_dict)
        print(adress_book)

xml_file = 'addres-book-q.xml'
process_xml(xml_file)""") 
    
FLS = [fls1,fls2,fls3,fls4,fls5,fls6,fls7,fls8,fls9,fls10,fls11,fls12]