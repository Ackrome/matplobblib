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

# cv: офлайн-билеты по компьютерному зрению

`matplobblib.cv` читает экспортированные билеты из package data и не обращается
к Google Drive во время работы. В `manifest.json` и `tickets/` находятся только
48 теоретических билетов с номерами `1..48`; служебные вкладки Google Docs
`Вопросы`, `Практика` и вкладки без номера в начале заголовка не упаковываются.

```python
from matplobblib import cv
```

`description()` возвращает сведения об установленном наборе билетов и примеры
вызовов:

```python
print(cv.description())
```

`show_tickets(mode="auto")` заменяет служебную вкладку `Вопросы`: функция
собирает актуальный нумерованный список тем непосредственно из 48 записей
`manifest.json`. В Jupyter список показывается как Markdown, в терминале
печатается, а режим `text` только возвращает строку:

```python
cv.show_tickets()
questions_markdown = cv.show_tickets(mode="text")
```

`ticket(ref)` ищет билет по номеру, строковому номеру, заголовку, фрагменту
заголовка или slug. Метод `markdown()` возвращает исходный Markdown:

```python
item = cv.ticket(1)
print(item.title)
print(item.markdown())
```

`all_tickets()` возвращает список всех билетов в порядке из `manifest.json`:

```python
for item in cv.all_tickets():
    print(item.number, item.title)
```

`search(query, limit=10)` ищет по заголовкам, ключевым словам, кратким
описаниям и полному тексту. Поиск не различает регистр и `е`/`ё`:

```python
matches = cv.search("свертка", limit=5)
```

`random_ticket(seed=None)` выбирает случайный билет. Передайте `seed`, если
нужен воспроизводимый выбор:

```python
item = cv.random_ticket(seed=42)
```

`short(ref, max_chars=280)` возвращает краткое описание заданной длины:

```python
summary = cv.short(1, max_chars=120)
```

`flashcards(ref, limit=12)` строит простые карточки из разделов, определений и
таблиц билета:

```python
for card in cv.flashcards(1, limit=6):
    print(card["q"], card["a"])
```

`render(ref, mode="auto", sanitize_math=True)` показывает Markdown с
изображениями. Перед показом функция по умолчанию обезвреживает повреждённые
формулы старых Google Docs exports: блоки с `\subscript`, `\superscript`,
`\Equation*`, `\sbracelr` и склеенными командами вроде `\DeltaI` превращаются
в обычный текст без KaTeX delimiters. Корректный простой LaTeX не меняется.
В Jupyter изображения встраиваются как data URLs; вне IPython Markdown
печатается с временными абсолютными путями к assets. Режим `text` только
возвращает подготовленный Markdown, ничего не выводя:

```python
cv.render(1)                    # auto: Jupyter или CLI
cv.render(1, mode="jupyter")   # принудительный notebook-режим
markdown = cv.render(1, mode="text")
raw = cv.render(1, mode="text", sanitize_math=False)  # диагностика старого export
```

Для отдельной строки доступна публичная функция
`sanitize_markdown_math(markdown)`. Она сохраняет обычный текст, корректные
формулы, code spans и Markdown images без изменений, исправляя только известные
повреждённые math fragments.

## Ручной экспорт Google Docs tabs

Экспортёр находится в `scripts/export_google_doc_tabs_to_cv_markdown.gs`.

1. Создайте Apps Script project, вставьте содержимое файла и проверьте
   `CFG.DOCUMENT_ID`.
2. Задайте `CFG.EXPORT_PARENT_FOLDER_ID` — ID папки Google Drive, куда можно
   записать результат. Настройте `CFG.BATCH_SIZE` (по умолчанию `3`) и при
   необходимости `CFG.MAX_BATCH_RUNTIME_MS`. Оставьте
   `CFG.EQUATION_MODE = 'plain'`, чтобы формулы экспортировались как безопасный
   читаемый текст без `$...$`.
3. Для самопроверки запустите `testEquationStringifier()`,
   `testTheoryTicketTabFilter()` и `testCvExportCheckpoint()`.
4. Один раз запустите `startCvExport()`. Функция создаст новую папку
   `cv-export-*`, сбросит старый checkpoint и выгрузит только первый batch.
5. Проверяйте прогресс через `showCvExportStatus()`. Повторно запускайте
   `continueCvExport()`, пока журнал не покажет `Export is complete.`.
   После ошибки снова запускайте `continueCvExport()` — уже сохранённые tabs
   не экспортируются заново.
6. Скачайте созданную папку. Скопируйте `manifest.json`, `tickets/` и `assets/`
   в `matplobblib/cv/data/`, заменив предыдущие данные. Экспортёр включает
   только вкладки, заголовки которых начинаются с уникального номера `1..48`;
   `Вопросы`, `Практика`, ненумерованные вкладки и номера вне диапазона
   пропускаются.
7. Из корня репозитория запустите `pytest` и `python -m build`. В собранных
   wheel и sdist должны присутствовать все файлы `matplobblib/cv/data/**`.

`resetCvExport()` удаляет только checkpoint из Script Properties и не удаляет
уже созданную папку Drive. Старое имя `exportDocTabsToMarkdown()` оставлено для
совместимости, но теперь оно эквивалентно `startCvExport()` и начинает новый
экспорт. Для продолжения всегда используйте `continueCvExport()`. Не меняйте
порядок или состав tabs исходного документа до завершения экспорта.
После обновления старой версии экспортёра сбросьте checkpoint через
`resetCvExport()` и запустите новый экспорт: версия `1.3.x` использует
отфильтрованную последовательность tabs и новый безопасный режим формул.

### Ручная проверка пакетного возобновления

1. Создайте тестовый документ с tabs `1`, `2`, `3` и задайте
   `CFG.BATCH_SIZE = 1`. Ненумерованные тестовые tabs будут отфильтрованы.
2. Запустите `startCvExport()` и проверьте статус `Exported 1 / 3`.
3. Закройте редактор Apps Script или дождитесь следующего запуска, затем
   вызовите `continueCvExport()`. Статус должен стать `Exported 2 / 3`, без
   повторного файла первого билета.
4. Ещё раз вызовите `continueCvExport()`. Итоговый статус должен быть
   `Exported 3 / 3` и `Export is complete.`.
5. Проверьте, что итоговый `manifest.json` содержит три ticket entry, а папки
   `tickets/` и `assets/` не содержат дубликатов после повторных запусков.

### Ручная проверка фильтра вкладок

1. Запустите `testTheoryTicketTabFilter()` и проверьте сообщение
   `Theory ticket tab filter regression test passed.`.
2. В тестовом документе создайте tabs `Вопросы`, `Практика`, `Черновик`, `1`,
   `48` и `49`.
3. Выполните новый экспорт. В `manifest.json` и `tickets/` должны попасть только
   билеты `1` и `48`; служебные tabs и номер вне диапазона должны отсутствовать.
4. Повторяющиеся номера считаются ошибкой экспорта, поскольку иначе
   `cv.ticket(number)` был бы неоднозначным.

### Ручная проверка экспорта формул

`CFG.EQUATION_MODE` поддерживает три режима:

- `plain` — режим по умолчанию: распознанные структуры преобразуются в обычный
  текст, неподдерживаемые — в `[formula]`; math delimiters не добавляются;
- `placeholder` — каждая формула становится `[formula]`;
- `latex` — `$...$` создаётся только для консервативного набора проверенных
  символов и структур, всё остальное становится `[formula]`.

1. В Apps Script сначала запустите `testEquationStringifier()`. Функция
   проверяет все три режима, `EquationSymbol` без `getText()`, неизвестный тип
   элемента и методы, выбрасывающие исключения. Ожидаемый результат — запись
   `Equation stringifier regression test passed` в журнале без ошибки.
2. Создайте тестовую вкладку Google Docs с обычным текстом и несколькими
   формулами: дробью, корнем, суммой, греческой буквой и знаком неравенства.
3. Запустите `startCvExport()`, а затем `continueCvExport()` до завершения.
   Убедитесь, что созданы `manifest.json`, Markdown-файл вкладки и каталог
   `assets/`.
4. Откройте Markdown-файл. В режиме `plain` там не должно быть команд
   `\subscript`, `\superscript` или `\Equation*`, а fallback formulas не должны
   находиться внутри `$...$`, `\(...\)` или `$$...$$`. Наличие `[formula]`
   допустимо, падение всего экспорта — нет.

Формулы экспортируются best effort и требуют проверки. Ссылки Google Docs на
изображения не используются во время выполнения: exporter сохраняет сами
байты изображений в `assets/`.
