# Условные характеристики относительно группы событий

Этот модуль содержит функции для работы с дискретными случайными величинами, связанными с бросками несбалансированных игральных костей. Каждая функция предоставляет расчет математического ожидания и дисперсии случайной величины, описывающей число бросков до выполнения определенного условия.

## Описание функций

### `CCE_1(a, b)`

Подбрасывается несбалансированная игральная кость до тех пор, пока не выпадут цифры `V1` и `V2`.

#### Аргументы:

- `a` (число): Вероятность выпадения цифры `V1` в одном броске.
- `b` (число): Вероятность выпадения цифры `V2` в одном броске.

#### Результаты:

- Математическое ожидание E(X).
- Дисперсия Var(X), если известно, что из `V1` и `V2` сначала выпала цифра `V2`.

#### Пример использования:

```python
result = CCE_1(0.3, 0.2)
# Вывод:
# E(X)   = 5,8333
# Var(X) = 8,333
```

---

### `CCE_2(a, b, c)`

Подбрасывается несбалансированная игральная кость до тех пор, пока не выпадут цифры `V1`, `V2` и `V3`.

#### Аргументы:

- `a` (число): Вероятность выпадения цифры `V1` в одном броске.
- `b` (число): Вероятность выпадения цифры `V2` в одном броске.
- `c` (число): Вероятность выпадения цифры `V3` в одном броске.

#### Результаты:

- Математическое ожидание E(X).
- Дисперсия Var(X), если известно, что из `V1`, `V2` и `V3` сначала выпала цифра `V1`, затем — `V2`.

#### Пример использования:

```python
result = CCE_2(0.2, 0.3, 0.5)
# Вывод:
# E(X)   = 8,1234
# Var(X) = 12,345
```

---

### Особенности:

- Все результаты округляются и выводятся с запятой вместо точки.
- Расчеты выполняются с использованием пользовательской функции `rrstr()` для форматирования.

Этот модуль упрощает работу с дискретными случайными величинами, связанными с многократными бросками игральных костей, предоставляя точные и эффективные вычисления.
