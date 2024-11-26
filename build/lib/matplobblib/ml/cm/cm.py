import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#######################################################################################################################
# Модификации модели классификации
#######################################################################################################################
class SVC1:
    """Классификация методом опорных векторов"""
    def __init__(self) -> None:
        """Классификация методом опорных векторов"""
        pass
    
    def predict(self, X):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            
        Returns:
            pandas.DataFrame: Предсказанные значения эндогенной переменной(Y)
        """
        return np.sign(X @ self.w)
    
    def error(self, X, y):
        """Считает значение ошибки

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)

        Returns:
            numerical: error
        """
        return (1 - self.predict(X) * y).sum()
    
    def fit(self, X, y, a=0.1, n=1000):
        """Функция обучения модели.

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций(Шагов). Defaults to 1000.
            
        Returns:
            
        """
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))                 # Вектор-столбец весов
        
        for i in range(n):
            pred = self.predict(X)                                      # Предсказывает класс объектов в итерации
            M_ = 1 - pred * y                                           # Отступ от разделяющей линии
            wrong_preds = (M_[M_ > 0].dropna()).index                   # Индексы неправильных предсказаний
            grad = -1 * (y.iloc[wrong_preds].T @ X.iloc[wrong_preds])   # Вычисляет градиент функции ошибки для итерации
            self.w -= (a * grad).T                                      # Обновление весов
            
            
    def accuracy_score(self, y, y_):
        """Вычисляет accuracy-score

        Args:
            y (pandas.DataFrame): Истинные значения эндогенной переменной (Y-True)
            y_ (pandas.DataFrame): Предсказанные значения эндогенной переменной (Y-Pred)

        Returns:
            numerical: Accuracy-score
        """
        return ((y_ == y).sum()/y.shape[0])[0]
    
    
    def plot(self, X, y):
        """Строит график

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
        """
        h = 0.02
        x_min, x_max = X[0].min() - 1, X[0].max() + 1
        y_min, y_max = X[1].min() - 1, X[1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))

        Z_linear = self.predict(np.c_[xx.ravel(), yy.ravel()])
        Z_linear = Z_linear.values.reshape(xx.shape)
        plt.contourf(xx, yy, Z_linear, alpha=0.1)
        plt.scatter(X[0], X[1], c=y)
        plt.title('SVC')
        plt.xlabel('Sepal Length')
        plt.ylabel('Sepal Width')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.show()
#######################################################################################################################
class LogReg1:
    """Логистическая регрессия Вариант 1
    """
    def __init__(self) -> None:
        """Логистическая регрессия"""
        pass
    
    def predict_prob(self, X):
        """Предсказывает вероятности значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            
        Returns:
            pandas.DataFrame: Предсказанные вероятности значения эндогенной переменной(Y)
        """
        with np.errstate(over='ignore'):
            result = 1/(1 + np.exp(-(X @ self.w)))
        return result
    
    def predict(self, X, wall):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            
        Returns:
            pandas.DataFrame: Предсказанные значения эндогенной переменной(Y)
        """
        prob = self.predict_prob(X)
        prob[prob > wall] = 1
        prob[prob < wall] = -1
        return prob
    
    def error(self, X, y):
        """Функция ошибки

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)

        Returns:
            numerical: значение функции ошибки
        """
        return -(y * np.log(self.predict_prob(X)) + (1 - y) * np.log(self.predict_prob(-X))).sum()
    
    def fit(self, X, y, a=0.1, n=1000):
        """Функция обучения модели.

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
            a (float, optional): Скорость обучения. Defaults to 0.1.
            n (int, optional): Количество итераций(Шагов). Defaults to 1000.
        """
        self.w = pd.DataFrame(np.ones((X.shape[1], 1)))     # Вектор-столбец весов
        for i in range(n):
            grad = -(X.T @ (y - self.predict_prob(X)))      # Вычисляет градиент функции ошибки для итерации
            self.w -= a * grad                              # Обновление весов
            
    def accuracy_score(self, y, y_):
        """Вычисляет accuracy-score

        Args:
            y (pandas.DataFrame): Истинные значения эндогенной переменной (Y-True)
            y_ (pandas.DataFrame): Предсказанные значения эндогенной переменной (Y-Pred)

        Returns:
            numerical: Accuracy-score
        """
        return ((y == y_).sum()/y.shape[0])[0]
    
    def plot(self, X, y):
        """Строит график

        Args:
            X (pandas.DataFrame): Экзогенная переменная (X)
            y (pandas.DataFrame): Эндогенная переменная (Y)
        """
        h = 0.02
        x_min, x_max = X[0].min() - 1, X[0].max() + 1
        y_min, y_max = X[1].min() - 1, X[1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))

        Z_linear = self.predict(np.c_[xx.ravel(), yy.ravel()], wall=0.5)
        Z_linear = Z_linear.values.reshape(xx.shape)
        plt.contourf(xx, yy, Z_linear, alpha=0.1)
        plt.scatter(X[0], X[1], c=y)
        plt.title('Logistic Regression')
        plt.xlabel('Sepal Length')
        plt.ylabel('Sepal Width')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.show()
#######################################################################################################################
def sigm(x):
    """Векторизованная функция сигмоиды"""
    with np.errstate(over='ignore'):
        return 1 / (1 + np.exp(-1*x))

class LogReg2():
    """Логистическая регрессия Вариант 2"""
    def __init__(self,X,Y):
        """Логистическая регрессия Вариант 2

        Args:
            X (array-like): Экзогенная переменная (X)
            Y (array-like): Эндогенная переменная (Y)
        """
        self.X = np.matrix(X)
        self.Y = np.matrix(Y).T
        self.b = np.matrix(np.ones(X.shape[1])).T

    def grad(self):
        """Вычисление градиента в данный момент"""
        s = sigm(self.X*self.b)
        return self.X.T * (self.Y - s)

    def fit(self,alpha=0.5, iters=1000):
        """Функция обучения

        Args:
            alpha (float, optional): Скорость обучения. Defaults to 0.5.
            iters (int, optional): Количество итераций(Шагов). Defaults to 1000.
        """
        for i in range(iters):
            self.b+=alpha*self.grad()
            alpha/=2

    def predict(self,X):
        """Предсказание классов объектов (X)"""
        return np.where(np.sign(np.matrix(X)*self.b)>0,1,0).T

    def predict_proba(self,X):
        """Предсказание вероятности принадлежности к классам объектов (X)"""
        return (np.matrix(X)*self.b).T
#######################################################################################################################
class SVC2():
    """Классификация методом опорных векторов с определением ядра"""
    def K(self,X, func = lambda X : X * X.T):
        """Преобразование экзогенной переменной с помощью ядерной функции

        Args:
            X (array-like): Экзогенная переменная (X)
            func (func, optional): Функция преобразования. Defaults to lambda X : X*X.T
            
        Returns:
            (array-like): Экзогенная переменная (X)
        """
        return func(X)

    def __init__(self,X,Y,lamb = 0):
        """Классификация методом опорных векторов с определением ядра

        Args:
            X (array-like): Экзогенная переменная (X)
            Y (array-like): Эндогенная переменная (Y)
            lamb (int, optional): Параметр регуляризации. Defaults to 0.
        """
        self.X = self.K(np.matrix(X))
        self.Y = np.matrix(Y).T
        self.b = np.matrix(np.ones(self.X.shape[1])).T
        self.lamb = lamb

    def predict(self,X):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (array-like): Экзогенная переменная (X)

        Returns:
            array-like: Предсказанные значения эндогенной переменной(Y)
        """
        xs = np.sign(self.K(np.matrix(X)) * self.b)
        return np.where(xs>0,1,0)
    
    def M_crit(self):
        """Вычисление Margin - значения

        Returns:
            array-like: Margin
        """
        nz = np.zeros(1)
        crit =  1 - (self.X*self.b).T * self.Y
        real = (-1)* self.X.T*self.Y
        return np.where(crit>0,real,nz)
    
    def L2_grad(self):
        """Градиент члена функции потерь с регуляризацией"""
        return 2*self.lamb*self.b
    
    def grad(self):
        """Общий градиент функции"""
        self.M_crit()
        return self.M_crit() + self.L2_grad()

    def fit(self,alpha=0.5,iters=1000):
        """Функция обучения"""
        for i in range(iters):
            self.b-=alpha*self.grad()
            alpha/=2
#######################################################################################################################
class KNN:
    def p(self, u, x):
        """Вычисление Евклидова расстояния"""
        return np.sqrt(((u - x)**2).sum())
    def kernel(self, x):
        """Вычисление ядерной функции

        Args:
            x (numerical, array-like): аргумент функции ядра

        Returns:
            (numerical, array-like): Значение ядерной функции
        """
        I = ['Rectangular','Triangular','Epanechnikov','Quartic','Triweight','Tricube','Cosine']
        if (self.kernel_type in I):
            assert np.abs(x)<=1, 'Ядро не подходит для данных' 
            
        kernel = {
            'Rectangular': 1/2,         # Оно же Юниформ или Нормальнок распределение
            'Triangular': (1-np.abs(x)),
            'Epanechnikov' :  3/4 * (1- x**2),
            'Quartic' : 15/16 * (1-x**2)**2,            #Оно же биквадратное
            'Triweight' : 35/32 * (1-x**2)**3,
            'Tricube':  70/81 * (1 - np.abs(x)**3)**3,
            'Gaussian': 1/np.sqrt(2*np.pi) * np.e**(-2*x**2),
            'Cosine': np.pi/4 * np.cos(np.pi/2 * x),
            'Logistic' : 1/(np.e**x + 2 + np.e**(-x)),
            'Sigmoid' : 2/np.pi * 1/(np.e**x + np.e**(-x)),
            'Silverman' : 1/2 * np.e**(-np.abs(x)/np.sqrt(2))*np.sin(np.abs(x)/np.sqrt(2) + np.pi/4),
            None: x     
        }
        return kernel[self.kernel_type]
    
    def predict(self, X, k=3, h=0.1):
        """Предсказывает значения эндогенной переменной(Y)

        Args:
            X (array-like): Экзогенная переменная (X)
            k (int,optional): Количество рассматриваемых соседей
            h (float, optional): Гиперпараметр для ядерной функции

        Returns:
            array-like: Предсказанные значения эндогенной переменной(Y)
        """
        p = {}  # Матрица расстояний
        index = 0
        for obj in X.values:    # Для каждого объекта из тех, которые мы хотим определить, создаем список расстояний до всех точек обучающей выборки
            p_obj = []
            for edu_obj in self.X.values:
                p_obj.append(self.p(obj, edu_obj))
            p[f'{index}'] = p_obj
            index += 1
        p = pd.DataFrame(p)
        ans = []
        for name_col in p.columns:      # По матрица находим класс точек наиболее близких к целевым
            idx = np.argpartition(p[name_col], k)[:k]           # Индексы k точек с минимальным расстояним
            class_y = [self.y.iloc[obj].values[0] for obj in idx]       # Каждой ближайшей точке находим соответствующий класс
            if self.kernel_type:
                kernel_k_near = [self.kernel(obj/h) for obj in p[name_col][idx].values] # Значение ядерной функции для каждой точки
                y_w = pd.DataFrame({'Y':class_y, 'w':kernel_k_near}) # Группирую по классу, нахожу сумму весов для каждого и выбираю больший
                ans.append(y_w.groupby('Y').sum('w').idxmax().values[0])
            else:
                vals, count = np.unique(class_y, return_counts=True)
                ans.append(vals[np.argmax(count)]) # Находим наиболее встречающийся класс                
                
        return pd.DataFrame(ans)
    
    def fit(self, X, y, kernel_type = 'Gaussian'):
        """Добавим тренировочную выборку в модель и определим тип ядра из
        `[
            'Rectangular',
            'Triangular',
            'Epanechnikov',
            'Quartic',
            'Triweight',
            'Tricube',
            'Gaussian',
            'Cosine',
            'Logistic',
            'Sigmoid',
            'Silverman',
            None
        ]`. При значении `None` будет применен невзвешенный k-NN
        
        Args:
            X (array-like): Экзогенная переменная (X)
            Y (array-like): Эндогенная переменная (Y)
        """
        self.X = X
        self.y = y
        self.kernel_type = kernel_type
        self.data = pd.concat([X, y], axis=1)
        return self
    
    def accuracy_score(self, y, y_):
        """Вычисление accuracy-значения модели

        Args:
            y (array-like): Истинные значения
            y_ (array-like): Предсказанные значения

        Returns:
            float: accuracy-score
        """
        return ((y_ == y).sum()/y.shape[0])[0]
    
    def plot(self, X, y):
        """Диаграмма рассеяния точек, где 'o' - обучающая выборка, а 'x' - целевая выборка

        Args:
            X (array-like): Экзогенная переменная целевой выборки (X)
            y (array-like): Эндогенная переменная целевой выборки (Y)
        """
        plt.scatter(self.X[0], self.X[1], c=self.y, marker='o') # Скаттер обучающей выборки
        plt.scatter(X[0], X[1], c=y, marker='x') # Скаттер целевых точек
        plt.show()
#######################################################################################################################        
CM = [LogReg1,LogReg2,SVC1,SVC2,KNN]