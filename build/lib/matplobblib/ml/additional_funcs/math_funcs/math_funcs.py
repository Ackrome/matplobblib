import numpy as np
def sigm(x):
    """Векторизованная функция сигмоиды"""
    with np.errstate(over='ignore'):
        return 1.0 / (1.0 + np.exp(-1*x))