# Нормальные случайные векторы: Дополнительный пакет функций

Этот пакет предоставляет функции для анализа нормальных случайных векторов с использованием аналитических методов и символьных вычислений.

---

## Список функций

### 1. `ANRV_1(a, b, n)`

**Описание**: Генерация случайного вектора (X, Y), равномерно распределённого в треугольнике $ x \geq 0, y \geq 0, a \cdot x + y \leq b $. Вычисляет математическое ожидание $ E(X^n \cdot Y) $.**Аргументы**:

- `a` (число): Коэффициент при $ x $.
- `b` (число): Верхняя граница.
- `n` (число): Степень $ X $.
  **Возвращает**: Математическое ожидание $ E(X^n \cdot Y) $.

---

### 2. `ANRV_2(a, x_1, x_2, y_1, y_2, p)`

**Описание**: Генерация случайного вектора с плотностью распределения $ f(x, y) = a \cdot x + C \cdot y $ на прямоугольной области $ x_1 < x < x_2, y_1 < y < y_2 $.Функция находит:

- Константу $ C $, обеспечивающую нормировку.
- Вероятность $ P(X + Y > p) $.**Аргументы**:
- `a` (число): Коэффициент при $ x $.
- `x_1, x_2` (числа): Границы по $ x $.
- `y_1, y_2` (числа): Границы по $ y $.
- `p` (число): Условие для вероятности.
  **Возвращает**: Кортеж $ (C, P(X + Y > p)) $.

---

### 3. `ANRV_3(C, a, b, p)`

**Описание**: Генерация случайного вектора с плотностью распределения $ f(x, y) = C \cdot e^{a \cdot x + b \cdot y} $ в области $ x, y \geq 0 $.Функция вычисляет вероятность $ P(X < p) $.**Аргументы**:

- `C` (число): Коэффициент при экспоненте (должен быть равен $ a \cdot b $).
- `a, b` (числа): Коэффициенты в экспоненциальной функции.
- `p` (число): Условие для вероятности.
  **Возвращает**: Вероятность $ P(X < p) $.

---

### 4. `ANRV_4(c_x2=0, c_x=0, c_xy=0, c_y=0, c_y2=0)`

**Описание**: Генерация случайного вектора с плотностью распределения:

$$
f_{X, Y}(x, y) = \frac{1}{\pi} e^{-\frac{1}{2}(c_{x^2} x^2 + c_x x + c_{xy} xy + c_y y + c_{y^2} y^2)}
$$

Функция вычисляет:

- Математические ожидания $ E(X) $, $ E(Y) $.
- Дисперсии $ \text{Var}(X) $, $ \text{Var}(Y) $.
- Ковариацию $ \text{Cov}(X, Y) $.
- Коэффициент корреляции $ \rho(X, Y) $.
- Условные математические ожидания $ E(X|Y) $, $ E(Y|X) $.
- Условные дисперсии $ \text{Var}(X|Y) $, $ \text{Var}(Y|X) $.**Аргументы**:
- `c_x2, c_x, c_xy, c_y, c_y2` (числа): Коэффициенты в плотности распределения.
  **Возвращает**: Кортеж значений $ (E(X), E(Y), \text{Var}(X), \text{Var}(Y), \text{Cov}(X, Y), \rho(X, Y), E(X|Y), E(Y|X), \text{Var}(X|Y), \text{Var}(Y|X)) $.
