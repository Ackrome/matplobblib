# интерполяция по Лагранжу
def lagrange_interpolation(x_values, y_values, x):
    """
    Вычисляет значение интерполяционного многочлена Лагранжа в точке x
    x_values: массив узлов интерполяции
    y_values: массив значений функции в узлах
    x: точка для вычисления
    """
    n = len(x_values)
    result = 0.0

    # Проверка на совпадение размеров массивов
    if len(y_values) != n:
        raise ValueError("Количество x и y значений должно совпадать")

    # Вычисление суммы по формуле Лагранжа
    for i in range(n):
        term = y_values[i]
        for j in range(n):
            if j != i:
                # Вычисление базисного полинома
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term

    return result

def lagrange_interpolation_func_get(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    n = len(x_values)
    # Проверка уникальности x_values
    for i in range(n):
        for j in range(i + 1, n):
            if x_values[i] == x_values[j]:
                raise ValueError("x_values must be distinct")
    
    def _basis(i, x):
        term = 1.0
        xi = x_values[i]
        for j in range(n):
            if j != i:
                xj = x_values[j]
                term *= (x - xj) / (xi - xj)
        return term
    
    def _lagrange(x):
        total = 0.0
        for i in range(n):
            total += y_values[i] * _basis(i, x)
        return total
    
    return _lagrange

INTER = [lagrange_interpolation,lagrange_interpolation_func_get]