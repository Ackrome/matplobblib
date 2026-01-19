import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######################################################################################################################
# Модификации линейной регрессионной модели
#######################################################################################################################
class LinearRegression:
    """
    Реализация линейной регрессии с пакетным градиентным спуском.
    """
    def __init__(self):
        """Инициализация модели."""
        self.w = None
        
    def predict(self, X):
        """
        Предсказывает целевые значения для входных данных.

        Args:
            X (pd.DataFrame): Матрица признаков.

        Returns:
            pd.DataFrame: Вектор предсказанных значений.
        """
        return X @ self.w
    
    def error(self, X, y):
        """
        Вычисляет ошибку MSE (не используется напрямую в `fit`, но может быть полезна).

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.

        Returns:
            np.ndarray: Значение MSE.
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2
    
    def fit(self, X, y, a=0.1, n=1000):
        """
        Обучает модель линейной регрессии с помощью пакетного градиентного спуска.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
            a (float, optional): Скорость обучения (learning rate). Defaults to 0.1.
            n (int, optional): Количество итераций. Defaults to 1000.
            
        Returns:
            np.ndarray: Массив ошибок на каждой итерации.
        """
        errors = []
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))        # Вектор-столбец весов
        N = X.shape[0]                                         # Количество объектов
        for i in range(n):
            errors.append([*self.error(X, y).values.tolist()]) # Подсчет ошибки для итерации
            f = self.predict(X)                                # Вычисляет предсказанные значения для итерации
            grad = 2/N * (X.T @ (f - y))                       # Вычисляет градиент функции ошибки для итерации
            self.w -= a * grad                                 # Обновление весов
        
        self.errors = np.array(errors)
        return self.errors
        
    def score(self, y, y_):
        """
        Вычисляет коэффициент детерминации (R^2).

        Args:
            y (pd.DataFrame): Вектор истинных значений.
            y_ (pd.DataFrame): Вектор предсказанных значений.

        Returns:
            float: Значение R^2.
        """
        return (1 - ((y - y_)**2).sum()/((y - y.mean())**2).sum())[0]
    
    def plot(self, X, y):
        """
        Строит график рассеяния "предсказание vs истинное значение".

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
        """
        yy = self.predict(X)
        plt.scatter(yy,y)
        plt.plot(yy, yy, c='r')
        plt.ylabel('$Y$')
        plt.xlabel('$Y$')
        plt.show()
    
    def study_plot(self,errors = None):
        """
        Строит график изменения ошибки в процессе обучения.

        Args:
            errors (array-like, optional): Массив ошибок. Если None, используются
                ошибки, сохраненные после `fit`. Defaults to None.
        """
        if errors == None:
            errors = self.errors[:,0,0]
            
        plt.plot([i+1 for i in range(len(errors))], errors)
        plt.xlabel('$Steps$')
        plt.ylabel('$Errors$')
        plt.show()
#######################################################################################################################
class LinearRegressionStoh:
    """
    Реализация линейной регрессии с стохастическим (батч) градиентным спуском.
    """
    def __init__(self):
        """Инициализация модели."""
        self.w = None
        
    def predict(self, X):
        """
        Предсказывает целевые значения для входных данных.

        Args:
            X (pd.DataFrame): Матрица признаков.

        Returns:
            pd.DataFrame: Вектор предсказанных значений.
        """
        return X @ self.w
    
    def error(self, X, y):
        """
        Вычисляет ошибку MSE.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.

        Returns:
            np.ndarray: Значение MSE.
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2
    
    def fit(self, X, y, B, E, a=0.1, n=1000):
        """
        Обучает модель с помощью стохастического градиентного спуска.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
            B (int): Размер батча (подвыборки).
            E (int): Количество эпох.
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Не используется в этой реализации.
        """
        errors = []
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))     # Вектор-столбец весов
        N = X.shape[0]                                      # Количество объектов
        for i in range(E):
            l = 0
            while l < N:
                batch_x = X.iloc[l:l+B]                     # Выбираем подвыборку
                batch_y = y.iloc[l:l+B]                         
                errors.append([*self.error(batch_x, batch_y).values.tolist()]) # Подсчет ошибки для итерации подвыборки
                f = self.predict(batch_x)                   # Вычисляет предсказанные значения для итерации подвыборки
                grad = 2/N * (batch_x.T @ (f - batch_y))    # Вычисляет градиент функции ошибки для итерации
                self.w -= a * grad                          # Обновление весов
                l += B                                      # Переход к следующей подвыборке

        self.errors = np.array(errors)
        return self.errors
    
    def score(self, y, y_):
        """
        Вычисляет коэффициент детерминации (R^2).

        Args:
            y (pd.DataFrame): Вектор истинных значений.
            y_ (pd.DataFrame): Вектор предсказанных значений.

        Returns:
            float: Значение R^2.
        """
        return (1 - ((y - y_)**2).sum()/((y - y.mean())**2).sum())[0]
    
    def plot(self, X, y):
        """
        Строит график рассеяния "предсказание vs истинное значение".

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
        """
        yy = self.predict(X)
        plt.scatter(yy,y)
        plt.plot(yy, yy, c='r')
        plt.ylabel('$Y$')
        plt.xlabel('$Y$')
        plt.show()
    
    def study_plot(self,errors = None):
        """
        Строит график изменения ошибки в процессе обучения.

        Args:
            errors (array-like, optional): Массив ошибок. Если None, используются
                ошибки, сохраненные после `fit`. Defaults to None.
        """
        if errors == None:
            errors = self.errors[:,0,0]
            
        plt.plot([i+1 for i in range(len(errors))], errors)
        plt.xlabel('$Steps$')
        plt.ylabel('$Errors$')
        plt.show()
#######################################################################################################################
class LinearRegressionL2:
    """
    Реализация линейной регрессии с L2-регуляризацией (Ridge регрессия).
    """
    def __init__(self):
        """Инициализация модели."""
        self.w = None # веса
        
    def predict(self, X):
        """
        Предсказывает целевые значения для входных данных.

        Args:
            X (pd.DataFrame): Матрица признаков.

        Returns:
            pd.DataFrame: Вектор предсказанных значений.
        """        
        return X @ self.w
    
    def error(self, X, y, lambd):
        """
        Вычисляет ошибку MSE с L2-штрафом.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
            lambd (float): Коэффициент L2-регуляризации (λ).

        Returns:
            np.ndarray: Значение функции потерь.
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2 + lambd*((self.w**2).sum())
    
    def fit(self, X, y, lambd, a=0.1, n=1000):
        """
        Обучает модель с помощью градиентного спуска.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
            lambd (float): Коэффициент L2-регуляризации (λ).
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций. Defaults to 1000.

        Returns:
            pd.DataFrame: DataFrame с историей изменения весов на каждой итерации.
        """
        self.b = [] ##
        errors = []
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))            # Вектор-столбец весов
        N = X.shape[0]                                             # Количество объектов
        for i in range(n):
            self.b.append(self.w.T) ##
            errors.append([*self.error(X, y, lambd).values.tolist()]) # Подсчет ошибки для итерации
            f = self.predict(X)                                # Вычисляет предсказанные значения для итерации
            grad = 2/N * (X.T @ (f - y)) + 2*lambd*self.w        # Вычисляет градиент функции ошибки для итерации
            self.w -= a * grad                                  # Обновление весов
            
        self.b = pd.DataFrame([self.b[i].values[0] for i in range(len(self.b))])
        return self.b
    
    def score(self, y, y_):
        """
        Вычисляет коэффициент детерминации (R^2).

        Args:
            y (pd.DataFrame): Вектор истинных значений.
            y_ (pd.DataFrame): Вектор предсказанных значений.

        Returns:
            float: Значение R^2.
        """
        return (1 - ((y - y_)**2).sum()/((y - y.mean())**2).sum())[0]
    
    def plot(self, X, y):
        """
        Строит график рассеяния "предсказание vs истинное значение".

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
        """
        yy = self.predict(X)
        plt.scatter(yy,y)
        plt.plot(yy, yy, c='r')
        plt.ylabel('$Y$')
        plt.xlabel('$Y$')
        plt.show()
#######################################################################################################################
class LinearRegressionMAE:
    """
    Реализация линейной регрессии с функцией потерь MAE (Mean Absolute Error).
    """
    def __init__(self):
        """Инициализация модели."""
        self.w = None   #Веса
        
    def predict(self, X):
        """
        Предсказывает целевые значения для входных данных.

        Args:
            X (pd.DataFrame): Матрица признаков.

        Returns:
            pd.DataFrame: Вектор предсказанных значений.
        """
        return X @ self.w
    
    def error(self, X, y):
        """
        Вычисляет ошибку MAE.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.

        Returns:
            np.ndarray: Значение MAE.
        """
        N = X.shape[0]
        return 1/N * abs(self.predict(X) - y)
    
    def fit(self, X, y, a=0.1, n=1000):
        """
        Обучает модель с помощью градиентного спуска.

        Args:
            X (pd.DataFrame): Матрица признаков.
            y (pd.DataFrame): Вектор истинных значений.
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций. Defaults to 1000.
            
        Returns:
            np.ndarray: Массив ошибок на каждой итерации.
        """
        errors = []
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))         # Вектор-столбец весов
        N = X.shape[0]                                          # Количество объектов
        for i in range(n):
            errors.append([*self.error(X, y).values.tolist()])  # Подсчет ошибки для итерации
            f = self.predict(X)                                 # Вычисляет предсказанные значения для итерации
            grad = -1/N * np.sign(f - y)                        # Вычисляет градиент функции ошибки для итерации
            self.w -= a * grad                                  # Обновление весов
            
        self.errors = np.array(errors)
        return self.errors
    
    def score(self, y, y_):
        """Interpretation
        - R^2 = 1: The model perfectly predicts the values of y.
        - R^2 = 0: The model performs no better than simply predicting the mean of y  for all observations.
        - R^2 < 0: The model performs worse than predicting the mean, indicating a poor fit.

        Args:
            y (pandas.DataFrame): Истинные значения эндогенной переменной (Y-True)
            y_ (pandas.DataFrame): Предсказанные значения эндогенной переменной (Y-Pred)

        Returns:
            numerical: Коэффициент детерминации (R^2 score)
        """
        return (1 - ((y - y_)**2).sum()/((y - y.mean())**2).sum())[0]
    
    def plot(self, X, y):
        """Строит график

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
        """
        yy = self.predict(X)
        plt.scatter(yy,y)
        plt.plot(yy, yy, c='r')
        plt.ylabel('$Y$')
        plt.xlabel('$Y$')
        plt.show()
#######################################################################################################################
class LinearRegressionL1:
    """Линейная регрессия с L1-регуляризацией"""
    def __init__(self):
        """Линейная регрессия с L1-регуляризацией"""
        self.w = None #Веса
        
    def predict(self, X):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
        Returns:
            pandas.DataFrame: Предсказанные значения эндогенной переменной(Y)
        """
        return X @ self.w
    
    def error(self, X, y, lambd):
        """Считает значение ошибки MSE с добавлением `penalty` члена выражения

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            lambd (numerical): Параметр Регуляризации (λ)

        Returns:
            numpy.array: MSE + λ* sum(|w_i|)
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2 + lambd*((abs(self.w)).sum())
    
    def fit(self, X, y, lambd, a=0.1, n=1000):
        """Функция обучения модели.

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            lambd (numerical): Параметр Регуляризации (λ)
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций(Шагов). Defaults to 1000.

        Returns:
            pandas.DataFrame: Таблица изменения весов на каждой итерации градиаентного спуска
        """
        self.b = [] ##
        errors = []
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))                 # Вектор-столбец весов
        N = X.shape[0]                                                  # Количество объектов
        for i in range(n):
            self.b.append(self.w.T) ##
            errors.append([*self.error(X, y, lambd).values.tolist()])   # Подсчет ошибки для итерации
            f = self.predict(X)                                         # Вычисляет предсказанные значения для итерации
            grad = 2/N * (X.T @ (f - y)) + lambd*np.sign(self.w.sum())  # Вычисляет градиент функции ошибки для итерации
            self.w -= a * grad                                          # Обновление весов
            
        self.b = pd.DataFrame([self.b[i].values[0] for i in range(len(self.b))])
        return self.b
    
    def score(self, y, y_):
        """Interpretation
        - R^2 = 1: The model perfectly predicts the values of y.
        - R^2 = 0: The model performs no better than simply predicting the mean of y  for all observations.
        - R^2 < 0: The model performs worse than predicting the mean, indicating a poor fit.

        Args:
            y (pandas.DataFrame): Истинные значения эндогенной переменной (Y-True)
            y_ (pandas.DataFrame): Предсказанные значения эндогенной переменной (Y-Pred)

        Returns:
            numerical: Коэффициент детерминации (R^2 score)
        """
        return (1 - ((y - y_)**2).sum()/((y - y.mean())**2).sum())[0]
    
    def plot(self, X, y):
        """Строит график

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
        """
        yy = self.predict(X)
        plt.scatter(yy,y)
        plt.plot(yy, yy, c='r')
        plt.ylabel('$Y$')
        plt.xlabel('$Y$')
        plt.show()
#######################################################################################################################

#######################################################################################################################
RM = [LinearRegression,LinearRegressionStoh,LinearRegressionMAE,LinearRegressionL1,LinearRegressionL2]