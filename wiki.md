# description

```python
from matplobblib.nm import *
description()
```

Выведет список всех user-функций модуля в виде

Тема1: функция1: описание[:n_symbols];
            функция2: описание[:n_symbols];

Допустим, нас интересует тема 'Матричные операции' , тогда мы первым аргументом даем название темы в эту функцию:

```python
from matplobblib.nm import *
description('Матричные операции')
```

Нам выдадут полный список функций с их полным описанием, но без кода. Вида
функция1: описание;
функция2: описание;

Допустим, нам понравилась функция norm. Тогда мы СТРОКОВЫМ ТИПОМ  задаем следующий аргумент функции description():

```python
from matplobblib.nm import *
description('Матричные операции','norm')
```

В таком случае нам выдадут код функции norm, который мы как раз и хотели узнать.
Если мы хотим, чтобы нам дали код функции вместе с докстрингом этой функции, тогда пишем show_doc=True:

```python
from matplobblib.nm import *
description('Матричные операции','norm', show_doc=True)
```

# getsource

Если мы знаем как называется функция, которая нам нужна, то есть путь быстрее, чем `description()`:

```python
from matplobblib.nm import *
print(getsource(norm)) # Ровно то же самое, что description('Матричные операции','norm', show_doc=True)
```

Или без докстринга

```python
from matplobblib.nm import *
print(getsource_no_docstring(norm)) # Ровно то же самое, что description('Матричные операции','norm')
```
