import numpy as np
def sigm(x):
    """
    Вычисляет сигмоидную (логистическую) функцию.

    Функция обрабатывает входные данные векторизованно и защищена от
    переполнения при вычислении экспоненты.

    Args:
        x (np.ndarray or float): Входное значение или массив значений.

    Returns:
        np.ndarray or float: Результат применения сигмоидной функции.
    """
    with np.errstate(over='ignore'):
        return 1.0 / (1.0 + np.exp(-1*x))
    
MATH_FUNCS = [sigm]