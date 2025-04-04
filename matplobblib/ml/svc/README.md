# SVC (Support Vector Classifier)

Этот проект реализует модель классификации с использованием метода опорных векторов (SVC). Код написан на Python и включает методы для обучения модели, предсказания классов, вычисления точности (accuracy), а также визуализации границы принятия решения.

---

## Описание

Модель SVC — это алгоритм машинного обучения, используемый для задач бинарной классификации. Модель строит гиперплоскость в пространстве признаков, которая разделяет объекты двух классов с максимальным отступом. В данном случае реализованы различные ядра (`linear`, `polynomial`, `rbf`), а также автоматический подбор параметра регуляризации `C`.

---

## Использование

Для использования класса `SVC` выполните следующие шаги:

1. Импортируйте необходимые библиотеки:

   ```python
   import numpy as np
   import matplotlib.pyplot as plt
   from cvxopt import matrix, solvers
   ```
2. Создайте экземпляр класса `SVC`.
3. Обучите модель, передав матрицу признаков `X` и вектор меток `y` в метод `fit`.
4. Используйте методы `predict`, `score` и `visualize` для оценки качества модели и визуализации данных.

---

## Методы класса

### 1. `__init__(kernel='linear', C=None, kernel_params=None)`

Инициализация модели SVC.

- **Параметры:**
  - `kernel`: Тип ядра (`'linear'`, `'polynomial'`, `'rbf'`).
  - `C`: Параметр регуляризации; если `None`, то будет подобран автоматически.
  - `kernel_params`: Словарь с параметрами ядра (например, `degree` для полиномиального или `sigma` для RBF).

---

### 2. `_kernel_function(x1, x2)`

Вычисляет значение ядра между двумя векторами.

- **Поддерживаемые ядра:**
  - `'linear'`: Линейное ядро.
  - `'polynomial'`: Полиномиальное ядро (параметры: `degree`, `coef0`).
  - `'rbf'`: Радиальная базисная функция (RBF) (параметр: `sigma`).

---

### 3. `_tune_C(X, y, folds=5, candidates=None)`

Автоматический подбор параметра регуляризации `C` с помощью кросс-валидации.

- **Параметры:**
  - `X`: Массив признаков размером `(n_samples, n_features)`.
  - `y`: Вектор меток (-1 или 1) размером `(n_samples,)`.
  - `folds`: Число фолдов для кросс-валидации (по умолчанию 5).
  - `candidates`: Список кандидатов для `C`; если `None`, используются значения `[0.01, 0.1, 1, 10, 100]`.
- **Возвращает:**
  - Оптимальное значение `C`.

---

### 4. `fit(X, y)`

Обучение модели SVC по обучающей выборке.

- **Параметры:**
  - `X`: Массив признаков размером `(n_samples, n_features)`.
  - `y`: Вектор меток (-1 или 1) размером `(n_samples,)`.

---

### 5. `project(X)`

Вычисление значений функции принятия решения для объектов `X`.

- **Параметры:**
  - `X`: Массив объектов размером `(n_samples, n_features)`.
- **Возвращает:**
  - Массив значений функции принятия решения.

---

### 6. `predict(X)`

Предсказывает метки классов (-1 или 1) для объектов `X`.

- **Параметры:**
  - `X`: Массив объектов размером `(n_samples, n_features)`.
- **Возвращает:**
  - Вектор предсказанных меток.

---

### 7. `score(X, y)`

Вычисляет точность модели на заданных данных.

- **Параметры:**
  - `X`: Массив объектов размером `(n_samples, n_features)`.
  - `y`: Истинные метки классов размером `(n_samples,)`.
- **Возвращает:**
  - Точность (доля правильно предсказанных объектов).

---

### 8. `visualize(X, y)`

Визуализация границы принятия решения, отступов и опорных векторов.

- **Параметры:**
  - `X`: Массив объектов размером `(n_samples, 2)`.
  - `y`: Истинные метки классов размером `(n_samples,)`.
- **Примечание:** Метод поддерживает только двумерные данные.

---

## Пример использования

```python
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

# Генерация данных
X, y = make_moons(n_samples=200, noise=0.2)
y = np.where(y == 0, -1, 1)  # Преобразуем метки в {-1, 1}

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Создание и обучение модели с RBF ядром
model = SVC(kernel='rbf')
model.fit(X_train, y_train)

# Предсказание и оценка
print("Accuracy:", model.score(X_test, y_test))

# Визуализация
model.visualize(X, y)
```

---

## Требования

Для работы с кодом необходимо установить следующие библиотеки:

- `numpy`
- `matplotlib`
- `cvxopt`

Установите их с помощью pip:

```bash
pip install numpy matplotlib cvxopt
```
