import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
KNNS = [KNN]