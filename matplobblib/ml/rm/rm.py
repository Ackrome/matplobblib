import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######################################################################################################################
# Модификации линейной регрессионной модели
#######################################################################################################################
class LinearRegression:
    """Линейная регрессия с градиентным спуском
    """
    def __init__(self):
        """Линейная регрессия с градиентным спуском
        """
        self.w = None
        
    def predict(self, X):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
        Returns:
            pandas.DataFrame: Предсказанные значения эндогенной переменной(Y)
        """
        return X @ self.w
    
    def error(self, X, y):
        """Считает значение ошибки MSE

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)

        Returns:
            numpy.array: MSE
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2
    
    def fit(self, X, y, a=0.1, n=1000):
        """Функция обучения модели.

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций(Шагов). Defaults to 1000.
            
        Returns:
            errors(list): Ошибки на каждую итерацию
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
    
    def study_plot(self,errors = None):
        """Строит график обучения для одной фичи

        Args:
            errors (array-like, optional): список ошибок. Defaults to None.
        """
        if errors == None:
            errors = self.errors[:,0,0]
            
        plt.plot([i+1 for i in range(len(errors))], errors)
        plt.xlabel('$Steps$')
        plt.ylabel('$Errors$')
        plt.show()
#######################################################################################################################
class LinearRegressionStoh:
    """Линейная регрессия с стохастическим градиентным спуском
    """
    def __init__(self):
        """Линейная регрессия с стохастическим градиентным спуском
        """
        self.w = None
        
    def predict(self, X):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
        Returns:
            pandas.DataFrame: Предсказанные значения эндогенной переменной(Y)
        """
        return X @ self.w
    
    def error(self, X, y):
        """Считает значение ошибки MSE

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)

        Returns:
            numpy.array: MSE
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2
    
    def fit(self, X, y, B, E, a=0.1, n=1000):
        """_summary_

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            B (numerical): Размер подвыборки
            E (numerical): Эпохи
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций(Шагов). Defaults to 1000.
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
    
    def study_plot(self,errors = None):
        """Строит график обучения для одной фичи

        Args:
            errors (array-like, optional): список ошибок. Defaults to None.
        """
        if errors == None:
            errors = self.errors[:,0,0]
            
        plt.plot([i+1 for i in range(len(errors))], errors)
        plt.xlabel('$Steps$')
        plt.ylabel('$Errors$')
        plt.show()
#######################################################################################################################
class LinearRegressionL2:
    """Линейная регрессия с L2-регуляризацией
    """
    def __init__(self):
        """Линейная регрессия с L2-регуляризацией
        """
        self.w = None # веса
        
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
            numpy.array: MSE + λ* sum(w_i^2)
        """
        N = X.shape[0]
        return 1/N * (X.T @ (self.predict(X) - y))**2 + lambd*((self.w**2).sum())
    
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
class LinearRegressionMAE:
    """Линейная регрессия с MAE
    """
    def __init__(self):
        """Линейная регрессия с MAE
        """
        self.w = None   #Веса
        
    def predict(self, X):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
        Returns:
            pandas.DataFrame: Предсказанные значения эндогенной переменной(Y)
        """
        return X @ self.w
    
    def error(self, X, y):
        """Считает значение ошибки MAE

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)

        Returns:
            numpy.array: MAE
        """
        N = X.shape[0]
        return 1/N * abs(self.predict(X) - y)
    
    def fit(self, X, y, a=0.1, n=1000):
        """Функция обучения модели.

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций(Шагов). Defaults to 1000.
            
        Returns:
            errors(list): Ошибки на каждую итерацию
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