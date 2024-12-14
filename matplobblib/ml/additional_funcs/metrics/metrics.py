import numpy as np
#########################################################################
# MAE
#########################################################################
def mean_absolute_error(y_true, y_pred):
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
def mean_absolute_error(y_true, y_pred):
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
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
    
    wape = np.sum(np.abs(np.subtract(y_true, y_pred)))/np.sum(np.abs(y_true))
    
    return wape
#########################################################################
# RMSLE
#########################################################################
def root_mean_squared_logarithmic_error(y_true, y_pred, c=1):
    assert len(y_true) == len(y_pred) > 1, 'Предсказанные и реальные значения должны быть представлены одномерными итерируемыми объектами, содержащими более 1 элемента'
    
    if not isinstance(y_true,np.ndarray):
        y_true = np.array(y_true)
        
    if not isinstance(y_pred,np.ndarray):
        y_pred = np.array(y_pred)
        
    if np.any(y_true + c <= 0) or np.any(y_pred + c <= 0):
        raise ValueError("Значения y_true и y_pred с учетом смещения c должны быть строго положительными")

    
    rmsle = np.sqrt(1/len(y_true) * np.sum(np.subtract(np.log(y_true+c),np.log(y_pred+c))**2))
    
    return rmsle
