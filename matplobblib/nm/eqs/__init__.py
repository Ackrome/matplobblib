# метод дихотомии <=>  метод половинного деления
def bisection_method(f, a, b, eps=1e-6, max_iter=1000):
    """
    f: функция f(x)
    a, b: начальный интервал [a, b]
    eps: точность
    max_iter: максимальное число итераций
    """
    if f(a) * f(b) >= 0:
        raise ValueError("Функция не меняет знак на интервале [a, b]")

    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < eps or (b - a) < eps:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return None





# Метод Ньютона
def newton_method(f, df, x0, eps=1e-6, max_iter=1000):
    """
    f: функция f(x)
    df: производная f'(x)
    x0: начальное приближение
    """
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < eps:
            return x
        dfx = df(x)
        if dfx == 0:
            raise ValueError("Производная равна нулю")
        x = x - fx / dfx
    raise RuntimeError("Метод не сошёлся за указанное число итераций")







# Метод секущих
def secant_method(f, x0, x1, eps=1e-6, max_iter=1000):
    """
    x0, x1: два начальных приближения
    """
    for _ in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        if abs(fx1) < eps:
            return x1
        if fx1 - fx0 == 0:
            raise ValueError("Деление на ноль")
        x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        x0, x1 = x1, x_next
    raise RuntimeError("Метод не сошёлся за указанное число итераций")





# Метод Вегстейна
def wegstein_method(g, x0, max_iter=100, tol=1e-6):
    x_prev = x0
    x_current = g(x_prev)
    history = [x_prev, x_current]

    for _ in range(max_iter):
        if abs(x_current - x_prev) < tol:
            return x_current, history

        # Вычисление параметра q
        delta_g = g(x_current) - g(x_prev)
        delta_x = x_current - x_prev
        q = delta_g / (delta_x - delta_g)

        # Итерация Вегстейна
        x_next = (1 - q) * x_current + q * g(x_current)

        x_prev, x_current = x_current, x_next
        history.append(x_current)

    raise RuntimeError("Метод не сошёлся за указанное число итераций")







# Метод простых итераций
def simple_iteration_method(g, x0, eps=1e-6, max_iter=1000):
    """
    g: функция, к которой приводится уравнение x = g(x)
    x0: начальное приближение
    """
    x = x0
    for _ in range(max_iter):
        x_next = g(x)
        if abs(x_next - x) < eps:
            return x_next
        x = x_next
    raise RuntimeError("Метод не сошёлся за указанное число итераций")

def dichotomy_method(f, a, b, eps=1e-6, max_iter=1000):
    """
    f: функция f(x)
    a, b: начальный интервал [a, b]
    eps: точность
    max_iter: максимальное число итераций
    """
    if f(a) * f(b) >= 0:
        raise ValueError("Функция не меняет знак на интервале [a, b]")

    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < eps or (b - a) < eps:
            return c
        if f(c - eps/2) < f(c + eps/2) :
            b = c
        else:
            a = c
    return None

EQS = [bisection_method,dichotomy_method, newton_method,secant_method,wegstein_method,simple_iteration_method]