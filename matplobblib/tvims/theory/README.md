# Теоретические материалы

## Описание

Этот код предназначен для динамического отображения изображений PNG из подкаталогов внутри пакета Python. Основная цель — упрощение работы с теоретическими материалами, хранящимися в виде изображений (например, страниц из PDF-файлов, преобразованных в PNG). Код автоматически создает функции для каждого подкаталога, чтобы пользователи могли легко выводить изображения теории, организованные по темам.

---

## Основные возможности

1. **Динамическое создание функций** :

   * Код автоматически создает функции для вывода всех PNG-изображений из конкретного подкаталога.
   * Каждая функция получает имя формата `display_<имя_подкаталога>` и генерируется для всех подкаталогов в библиотеке `matplobblib.tvims.theory.pdfs`.
2. **Удобный доступ к теории** :

   * Пользователи могут вызывать созданные функции для просмотра всех страниц теоретических материалов.
3. **Поддержка каталогов** :

   * Код автоматически находит подкаталоги в заданном каталоге пакета.
4. **Совместимость с Jupyter Notebook** :

   * Изображения отображаются с помощью библиотеки `IPython.display`, что идеально подходит для использования в интерактивных средах.

---

## Структура функций

### 1. `get_png_files_from_subdir(subdir)`

 **Описание** : Возвращает список путей к файлам PNG в указанном подкаталоге.

 **Параметры** :

* `subdir` (str): Имя подкаталога.

 **Возвращает** : Список путей к файлам PNG.

---

### 2. `display_png_files_from_subdir(subdir)`

 **Описание** : Выводит изображения PNG из указанного подкаталога.

 **Параметры** :

* `subdir` (str): Имя подкаталога.

 **Результат** : Отображает изображения PNG в Jupyter Notebook.

---

### 3. `create_subdir_function(subdir)`

 **Описание** : Динамически создает функцию для отображения PNG-файлов из заданного подкаталога. Созданные функции добавляются в глобальную область видимости и список `THEORY`.

 **Параметры** :

* `subdir` (str): Имя подкаталога.

---

### 4. `list_subdirectories()`

 **Описание** : Возвращает список подкаталогов в пакете `matplobblib.tvims.theory.pdfs`.

 **Возвращает** : Список имен подкаталогов.

---

### 5. Созданные функции

После выполнения скрипта для каждого подкаталога будет создана функция формата `display_<имя_подкаталога>`. Эти функции:

* Отображают все PNG-изображения из соответствующего подкаталога.
* Автоматически добавляются в список `THEORY`.

---

## Зависимости

* **Python 3.6+**
* **Библиотеки** :
* `importlib.resources`: Для работы с пакетами и файлами.
* `Pillow (PIL)`: Для работы с изображениями.
* `IPython.display`: Для отображения изображений в Jupyter Notebook.

---

## Использование

1. **Запуск основного скрипта** :

* Убедитесь, что в каталоге `matplobblib.tvims.theory.pdfs` находятся подкаталоги с PNG-изображениями.

1. **Вызов функции** :

* После выполнения кода вызовите автоматически созданную функцию для нужного подкаталога:
  ```python
  display_<имя_подкаталога>()
  ```

1. **Просмотр доступных функций** :

* Список всех созданных функций доступен в переменной `THEORY`:
  ```python
  print(THEORY)
  ```

---

## Пример

### Шаги:

1. Пусть существует подкаталог `chapter_1`, содержащий файлы `page1.png`, `page2.png`.
2. После выполнения скрипта будет создана функция `display_chapter_1`.
3. Чтобы вывести изображения:
   ```python
   display_chapter_1()
   ```

Результат: Все страницы из подкаталога `chapter_1` будут выведены в Jupyter Notebook.

---

## Отладка

Если возникает ошибка, убедитесь, что:

* Пакет `matplobblib.tvims.theory.pdfs` доступен.
* Подкаталоги содержат файлы с расширением `.png`.
* Все зависимости установлены.