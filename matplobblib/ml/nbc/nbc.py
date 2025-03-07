import pandas as pd
import numpy as np
import scipy.stats as st
from collections import defaultdict

class NormalNaiveBayes:
    """
    Классификатор наивного байеса с предположением о нормальном (гауссовском) распределении признаков.
    
    Данный классификатор оценивает среднее и стандартное отклонение каждого признака для каждого класса
    на основе обучающей выборки, а затем использует эти параметры для вычисления правдоподобий при предсказании.
    """
    
    def fit(self, X, y):
        """
        Обучает классификатор на основе входных данных.
        
        Параметры:
        -----------
        X : array-like, shape (n_samples, n_features)
            Матрица признаков обучающей выборки.
        y : array-like, shape (n_samples,)
            Вектор меток классов.
            
        Возвращает:
        -----------
        self : object
            Обученный классификатор.
        """
        # Объединяем признаки и метки в один набор для удобства группировки
        dataset = np.column_stack((X, y))
        
        # Группируем строки по метке класса с помощью defaultdict
        data_per_class = defaultdict(list)
        for row in dataset:
            class_label = row[-1]
            features = row[:-1]
            data_per_class[class_label].append(features)

        
        # Вычисляем априорные вероятности каждого класса
        self.p_classes = {
            class_label: len(features_list) / len(X)
            for class_label, features_list in data_per_class.items()
        }
        
        # Для каждого класса вычисляем оценку параметров нормального распределения (среднее и стандартное отклонение)
        self.features_distribs = {}
        for class_label, rows in data_per_class.items():
            # Преобразуем список строк в DataFrame для удобных вычислений
            data = pd.DataFrame(rows)
            means = data.mean()
            stds = data.std(ddof=1)
            # Если стандартное отклонение равно 0, заменяем его на маленькое число, чтобы избежать деления на ноль
            self.features_distribs[class_label] = {
                col: st.norm(loc=means[col], scale=stds[col] if stds[col] > 0 else 1e-6)
                for col in data.columns
            }
        
        return self
    
    def predict_prob(self, X):
        """
        Вычисляет вероятности принадлежности каждого образца к классам.
        
        Параметры:
        -----------
        X : array-like, shape (n_samples, n_features)
            Матрица признаков тестовой выборки.
            
        Возвращает:
        -----------
        prob_per_class_for_x : list of numpy arrays
            Список, в котором каждый элемент – массив вероятностей по классам для соответствующего образца.
            Порядок классов соответствует порядку ключей self.p_classes.
        """
        prob_per_class_for_x = []
        class_order = list(self.p_classes.keys())
        
        # Обходим каждый образец из выборки
        for x in X:
            total_prob = 0.0  # Сумма по классам (нормировочная константа)
            class_probs = {}
            
            # Для каждого класса вычисляем неотнормированную вероятность (априорная вероятность * произведение плотностей)
            for class_label, distributions in self.features_distribs.items():
                # Вычисляем произведение плотностей для всех признаков
                likelihood = np.prod([
                    distribution.pdf(x[int(feature_idx)]) 
                    for feature_idx, distribution in distributions.items()
                ])
                prob = self.p_classes[class_label] * likelihood
                class_probs[class_label] = prob
                total_prob += prob
            
            # Нормируем вероятности, чтобы их сумма равнялась 1
            if total_prob > 0:
                normalized_probs = {label: prob / total_prob for label, prob in class_probs.items()}
            else:
                # Если суммарное правдоподобие оказалось 0, назначаем равномерное распределение
                normalized_probs = {label: 1.0 / len(class_probs) for label in class_probs}
            
            # Собираем вероятности в массив в порядке, определённом в class_order
            prob_array = np.array([normalized_probs[label] for label in class_order])
            prob_per_class_for_x.append(prob_array)
        
        return prob_per_class_for_x
    
    def predict(self, X):
        """
        Предсказывает метки классов для заданных образцов.
        
        Параметры:
        -----------
        X : array-like, shape (n_samples, n_features)
            Матрица признаков тестовой выборки.
            
        Возвращает:
        -----------
        predictions : numpy array, shape (n_samples,)
            Массив предсказанных меток классов.
        """
        # Получаем вероятностное распределение по классам для каждого образца
        probs = self.predict_prob(X)
        class_order = list(self.p_classes.keys())
        # Для каждого образца выбираем класс с максимальной вероятностью
        predictions = np.array([class_order[np.argmax(prob)] for prob in probs])
        return predictions
#
NBC = [NormalNaiveBayes]