import numpy as np
#########################################################################
# MAE
#########################################################################
def mean_absolute_error(y_true, y_pred):
    """
    Вычисляет среднюю абсолютную ошибку (MAE) между предсказанными и фактическими значениями.

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.

    Returns:
        float: Средняя абсолютная ошибка.
    """
    assert len(y_true) == len(y_pred) != 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    mae = 1/len(y_true) * np.sum(np.abs(np.subtract(y_true, y_pred)))
    
    return mae
#########################################################################
# MSE
#########################################################################
def mean_squared_error(y_true, y_pred):
    """
    Вычисляет среднеквадратичную ошибку (MSE) между предсказанными и фактическими значениями.

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.

    Returns:
        float: Среднеквадратичная ошибка.
    """
    assert len(y_true) == len(y_pred) != 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    mse = 1/len(y_true) * np.sum((np.subtract(y_true, y_pred))**2)
    
    return mse
#########################################################################
# MAPE
#########################################################################
def mean_absolute_percentage_error(y_true, y_pred):
    """
    Вычисляет среднюю абсолютную процентную ошибку (MAPE) между предсказанными и фактическими значениями.

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.

    Returns:
        float: Средняя абсолютная процентная ошибка.
    """
    assert len(y_true) == len(y_pred) != 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    mape = 1/len(y_true) * np.sum(np.abs(np.subtract(y_true, y_pred))/np.abs(y_true))
    
    return mape
#########################################################################
# SMAPE
#########################################################################
def symmetric_mean_absolute_percentage_error(y_true, y_pred):
    """
    Вычисляет симметричную среднюю абсолютную процентную ошибку (SMAPE).

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.

    Returns:
        float: Симметричная средняя абсолютная процентная ошибка.
    """
    assert len(y_true) == len(y_pred) != 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    smape = 1/len(y_true) * np.sum(2* np.abs(np.subtract(y_true, y_pred))/(y_true + y_pred))
    
    return smape
#########################################################################
# WAPE
#########################################################################
def weighted_average_percentage_error(y_true, y_pred):
    """
    Вычисляет взвешенную среднюю процентную ошибку (WAPE).

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.

    Returns:
        float: Взвешенная средняя процентная ошибка.
    """
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    wape = np.sum(np.abs(np.subtract(y_true, y_pred)))/np.sum(np.abs(y_true))
    
    return wape
#########################################################################
# MSLE
#########################################################################
def mean_squared_logarithmic_error(y_true, y_pred, c=1):
    """
    Вычисляет среднеквадратичную логарифмическую ошибку (MSLE).

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.
        c (float, optional): Смещение, добавляемое к значениям для избежания логарифма отрицательных чисел. По умолчанию 1.

    Returns:
        float: среднеквадратичная логарифмическая ошибка.

    Raises:
        ValueError: Если y_true или y_pred (с учетом c) имеют недопустимые значения.
    """
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
        
    if np.any(y_true + c <= 0) or np.any(y_pred + c <= 0):
        raise ValueError("Значения y_true и y_pred с учетом смещения c должны быть строго положительными")

    
    rmsle = (1/len(y_true) * np.sum(np.subtract(np.log(y_true+c),np.log(y_pred+c))))
    
    return rmsle
#########################################################################
# RMSLE
#########################################################################
def root_mean_squared_logarithmic_error(y_true, y_pred, c=1):
    """
    Вычисляет корень среднеквадратичной логарифмической ошибки (RMSLE).

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.
        c (float, optional): Смещение, добавляемое к значениям для избежания логарифма отрицательных чисел. По умолчанию 1.

    Returns:
        float: Корень среднеквадратичной логарифмической ошибки.

    Raises:
        ValueError: Если y_true или y_pred (с учетом c) имеют недопустимые значения.
    """
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
        
    if np.any(y_true + c <= 0) or np.any(y_pred + c <= 0):
        raise ValueError("Значения y_true и y_pred с учетом смещения c должны быть строго положительными")

    
    rmsle = np.sqrt(1/len(y_true) * np.sum(np.subtract(np.log(y_true+c),np.log(y_pred+c))**2))
    
    return rmsle
#########################################################################
# MedAE
#########################################################################
def median_absolute_error(y_true, y_pred, multioutput = "uniform_average"):
    """
    Вычисляет медианную абсолютную ошибку (MedAE).

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.
        multioutput (str, optional): {'raw_values', 'uniform_average'}\
            Defines aggregating of multiple output values.

    Returns:
        float: медианная абсолютная ошибка.
    """
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    output_errors  = np.median(np.abs(y_pred - y_true), axis=0)
    
    if isinstance(multioutput, str):
        if multioutput == "raw_values":
            return output_errors
        elif multioutput == "uniform_average":
            # pass None as weights to np.average: uniform mean
            multioutput = None

    return np.average(output_errors, weights=multioutput)
#########################################################################
# ME
#########################################################################
def max_error(y_true, y_pred):
    """
    Вычисляет максимальную ошибку (ME).

    Args:
        y_true (iterable): Реальные значения.
        y_pred (iterable): Предсказанные значения.


    Returns:
        float: максимальная ошибка.
    """
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)

    return np.max(np.abs(y_pred - y_true))