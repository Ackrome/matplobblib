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

# nlp.call_model

Вызывает OpenAI-совместимую языковую модель через ProxyAPI Responses API.

Сначала задайте ключ ProxyAPI в переменной окружения:

```python
import os
os.environ["PROXYAPI_API_KEY"] = "your_proxyapi_key"
```

Пример вызова:

```python
from matplobblib.nlp import *

answer = call_model(
    "Объясни, что такое бинарное дерево, в одном абзаце.",
    model="gpt-5-mini"
)
print(answer)
```

Ключ можно передать напрямую:

```python
answer = call_model("Привет!", api_key="your_proxyapi_key")
```

Дополнительные параметры: `system`, `temperature`, `max_output_tokens`,
`timeout`, `base_url`, `return_json` и любые другие параметры Responses API.
Если нужно посмотреть исходный JSON-ответ ProxyAPI, укажите `return_json=True`.

# nlp.description

Показывает доступные темы и функции в модуле `nlp`. Интерфейс такой же,
как у `description()` в `matplobblib.nm`.

```python
from matplobblib.nlp import *

description()
```

Показать только названия тем:

```python
description(show_only_keys=True)
```

Показать исходный код функции `call_model`:

```python
description("Вызовы языковых моделей", key="call_model", show_doc=True)
```
