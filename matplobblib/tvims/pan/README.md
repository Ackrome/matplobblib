# Портфельный анализ с невырожденной ковариационной матрицей

## Описание

Модуль предоставляет функции для анализа доходностей и рисков инвестиционного портфеля. Он ориентирован на работу с акциями и их стандартными отклонениями, коэффициентами корреляции и ожидаемыми доходностями.

### Основные функции:

1. **PAN\_1**: Рассчитывает стандартное отклонение доходности портфеля, состоящего из акций двух компаний (А и В), при известной корреляции их доходностей.
2. **PAN\_2**: Определяет ожидаемую доходность портфеля, составленного из акций трёх компаний (А, В и С), при минимальной дисперсии доходности.
3. **PAN\_3**: Находит доли акций в портфеле с минимальной дисперсией доходности для двух компаний (А и В), а также рассчитывает ожидаемую доходность и стандартное отклонение доходности портфеля.

---

### PAN\_1: Стандартное отклонение портфеля (две акции)

**Описание**:
Инвестор сформировал портфель из акций компаний А и В, вложив в акции А в `n` раз больше средств, чем в акции В. Известны стандартные отклонения доходностей акций и коэффициент корреляции между ними. Функция вычисляет стандартное отклонение доходности портфеля.

**Аргументы:**

- `n` (int): Соотношение вложений в акции А и В.
- `s_a` (число): Стандартное отклонение доходности акций А (в %).
- `s_b` (число): Стандартное отклонение доходности акций В (в %).
- `r_ab` (число): Коэффициент корреляции доходностей акций А и В.

**Вывод:**

- Стандартное отклонение доходности портфеля (в %).

---

### PAN\_2: Ожидаемая доходность портфеля (три акции)

**Описание**:
Функция определяет ожидаемую доходность портфеля, составленного из акций трёх компаний (А, В и С), при минимальной дисперсии доходности. Предполагается, что доходности акций независимы.

**Аргументы:**

- `e_a`, `e_b`, `e_c` (числа): Ожидаемые доходности акций А, В и С (в %).
- `s_a`, `s_b`, `s_c` (числа): Стандартные отклонения доходностей акций А, В и С (в %).

**Вывод:**

- Ожидаемая доходность портфеля (в %).

---

### PAN\_3: Портфель с минимальной дисперсией доходности (две акции)

**Описание**:
Функция вычисляет доли акций компаний А и В в портфеле с минимальной дисперсией доходности. Также рассчитываются ожидаемая доходность и стандартное отклонение доходности такого портфеля.

**Аргументы:**

- `e_a`, `e_b` (числа): Ожидаемые доходности акций А и В (в %).
- `s_a`, `s_b` (числа): Стандартные отклонения доходностей акций А и В (в %).
- `r_ab` (число): Коэффициент корреляции доходностей акций А и В.

**Вывод:**

- Доли акций А и В в портфеле.
- Ожидаемая доходность портфеля (в %).
- Стандартное отклонение доходности портфеля (в %).

---

## Общие инструкции

### Формат вывода

Результаты округляются до двух или трёх знаков после запятой, при этом используется запятая в качестве десятичного разделителя. Пример:

```
Стандартное отклонение доходности портфеля = 12,34 %
```

### Требования

- Python версии 3.6 или выше.
- Необходимые библиотеки: `numpy`, `sympy`.
