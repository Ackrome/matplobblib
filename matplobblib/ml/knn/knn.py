import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#######################################################################################################################
class KNN:
    def __init__(self, kernel_type='Gaussian', distance_metric='euclidean', k=3, h=0.1, task="classification"):
        """
        Реализация алгоритма k-ближайших соседей (k-NN) для классификации и регрессии.
        
        Args:
            kernel_type (str or None, optional): Тип ядерной функции для взвешивания соседей.
                Возможные значения:
                'Rectangular', 'Triangular', 'Epanechnikov', 'Quartic', 
                'Triweight', 'Tricube', 'Gaussian', 'Cosine', 'Logistic', 
                'Sigmoid', 'Silverman'. Если None, используется невзвешенный k-NN.
                Defaults to 'Gaussian'.
            distance_metric (str, optional): Метрика расстояния. 'euclidean' или 'manhattan'.
                Defaults to 'euclidean'.
            k (int, optional): Количество соседей. Defaults to 3.
            h (float, optional): Ширина окна (bandwidth) для ядерной функции. Defaults to 0.1.
            task (str, optional): Тип задачи: 'classification' или 'regression'.
                Defaults to "classification".
        """
        self.kernel_type = kernel_type
        self.distance_metric = distance_metric
        self.k = k
        self.h = h
        self.task = task
        self.X_train = None
        self.y_train = None
        self._init_kernels()
        
    def _init_kernels(self):
        self.kernels = {
            'Rectangular': lambda u: 0.5 if np.abs(u) <= 1 else 0,
            'Triangular': lambda u: (1 - np.abs(u)) if np.abs(u) <= 1 else 0,
            'Epanechnikov': lambda u: 0.75 * (1 - u**2) if np.abs(u) <= 1 else 0,
            'Quartic': lambda u: (15/16) * (1 - u**2)**2 if np.abs(u) <= 1 else 0,
            'Triweight': lambda u: (35/32) * (1 - u**2)**3 if np.abs(u) <= 1 else 0,
            'Tricube': lambda u: (70/81) * (1 - np.abs(u)**3)**3 if np.abs(u) <= 1 else 0,
            'Gaussian': lambda u: 1/np.sqrt(2*np.pi) * np.exp(-0.5 * u**2),
            'Cosine': lambda u: (np.pi/4) * np.cos(np.pi*u/2) if np.abs(u) <= 1 else 0,
            'Logistic': lambda u: 1/(np.exp(u) + 2 + np.exp(-u)),
            'Sigmoid': lambda u: 2/np.pi * 1/(np.exp(u) + np.exp(-u)),
            'Silverman': lambda u: 0.5 * np.exp(-np.abs(u)/np.sqrt(2)) * np.sin(np.abs(u)/np.sqrt(2) + np.pi/4)
        }
        
    def _distance(self, u, x):
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((u - x)**2))
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(u - x))
        else:
            raise ValueError("Unsupported distance metric")
    
    def _compute_distances(self, X):
        X = np.array(X)
        X_train = np.array(self.X_train)
        if self.distance_metric == 'euclidean':
            X_norm = np.sum(X**2, axis=1).reshape(-1, 1)
            X_train_norm = np.sum(X_train**2, axis=1).reshape(1, -1)
            distances = np.sqrt(X_norm + X_train_norm - 2 * np.dot(X, X_train.T))
        elif self.distance_metric == 'manhattan':
            distances = np.sum(np.abs(X[:, np.newaxis, :] - X_train[np.newaxis, :, :]), axis=2)
        return distances
    
    def fit(self, X, y):
        """
        Обучает модель, сохраняя обучающую выборку.
        
        Args:
            X (array-like): Матрица признаков обучающей выборки.
            y (array-like): Вектор целевых значений.
        """
        if isinstance(X, pd.DataFrame):
            self.X_train = X.values
        else:
            self.X_train = np.array(X)
            
        if isinstance(y, (pd.Series, pd.DataFrame)):
            self.y_train = np.array(y).flatten()
        else:
            self.y_train = np.array(y).flatten()
        return self
    
    def predict_proba(self, X):
        """
        Вычисляет вероятности принадлежности к каждому классу для задачи классификации.

        Args:
            X (array-like): Матрица признаков для предсказания.
        
        Returns:
            pd.DataFrame: DataFrame размера (n_samples, n_classes) с вероятностями
            принадлежности к каждому классу.
        """
        if self.task != "classification":
            raise ValueError("predict_proba доступен только для задачи классификации")
        X = np.array(X)
        distances = self._compute_distances(X)  # shape: (n_test, n_train)
        n_test = distances.shape[0]
        classes = np.unique(self.y_train)
        proba_list = []
        
        for i in range(n_test):
            current_k = min(self.k, len(self.X_train))
            neighbor_idx = np.argpartition(distances[i], current_k)[:current_k]
            neighbor_labels = self.y_train[neighbor_idx]
            
            if self.kernel_type is not None:
                dists = distances[i][neighbor_idx]
                u = dists / self.h
                kernel_func = self.kernels.get(self.kernel_type)
                weights = np.array([kernel_func(val) for val in u])
            else:
                weights = np.ones(current_k)
                
            total_weight = weights.sum()
            class_weights = {}
            for cls in classes:
                class_weights[cls] = weights[neighbor_labels == cls].sum()
            if total_weight == 0:
                prob = np.array([1/len(classes)]*len(classes))
            else:
                prob = np.array([class_weights[cls] / total_weight for cls in classes])
            proba_list.append(prob)
        proba_array = np.vstack(proba_list)
        return pd.DataFrame(proba_array, columns=classes)
    
    def predict(self, X):
        """
        Предсказывает метки классов или значения для входных данных.

        Для классификации используется голосование (взвешенное или простое).
        Для регрессии используется усреднение (взвешенное или простое).

        Args:
            X (array-like): Матрица признаков для предсказания.

        Returns:
            np.ndarray: Массив предсказанных значений.
        """
        X = np.array(X)
        distances = self._compute_distances(X)
        n_test = distances.shape[0]
        predictions = []
        
        if self.task == "classification":
            for i in range(n_test):
                current_k = min(self.k, len(self.X_train))
                neighbor_idx = np.argpartition(distances[i], current_k)[:current_k]
                neighbor_labels = self.y_train[neighbor_idx]
                
                if self.kernel_type is not None:
                    dists = distances[i][neighbor_idx]
                    u = dists / self.h
                    kernel_func = self.kernels.get(self.kernel_type)
                    weights = np.array([kernel_func(val) for val in u])
                    # Суммируем веса по классам
                    unique_labels = np.unique(neighbor_labels)
                    weight_sum = {label: weights[neighbor_labels == label].sum() for label in unique_labels}
                    max_weight = max(weight_sum.values())
                    # При равенстве голосов выбираем класс с наименьшим значением
                    candidates = [label for label, w in weight_sum.items() if np.isclose(w, max_weight)]
                    pred = np.min(candidates)
                else:
                    # Невзвешенное голосование
                    current_k = min(self.k, len(self.X_train))
                    neighbor_idx = np.argpartition(distances[i], current_k)[:current_k]
                    neighbor_labels = self.y_train[neighbor_idx]
                    vals, counts = np.unique(neighbor_labels, return_counts=True)
                    max_count = np.max(counts)
                    candidates = vals[counts == max_count]
                    pred = np.min(candidates)
                predictions.append(pred)
            return np.array(predictions)
        
        elif self.task == "regression":
            for i in range(n_test):
                current_k = min(self.k, len(self.X_train))
                neighbor_idx = np.argpartition(distances[i], current_k)[:current_k]
                if self.kernel_type is not None:
                    dists = distances[i][neighbor_idx]
                    u = dists / self.h
                    kernel_func = self.kernels.get(self.kernel_type)
                    weights = np.array([kernel_func(val) for val in u])
                    if weights.sum() == 0:
                        pred = np.mean(self.y_train[neighbor_idx])
                    else:
                        pred = np.dot(weights, self.y_train[neighbor_idx]) / weights.sum()
                else:
                    pred = np.mean(self.y_train[neighbor_idx])
                predictions.append(pred)
            return np.array(predictions)
        else:
            raise ValueError("Неподдерживаемый тип задачи. Используйте 'classification' или 'regression'.")
    
    def tune_parameters(self, X, y, param_grid, cv=5, scoring=None):
        """
        Подбирает оптимальные гиперпараметры `k` и `h` с помощью k-fold кросс-валидации.
        
        Args:
            X (array-like): Матрица признаков.
            y (array-like): Вектор целевых значений.
            param_grid (dict): Словарь с сеткой параметров для перебора, например:
                {'k': [3, 5, 7, 9], 'h': [0.1, 0.5, 1.0, 2.0]}
            cv (int, optional): Количество фолдов для кросс-валидации. Defaults to 5.
            scoring (callable, optional): Функция для оценки качества модели.
                Если None, используется accuracy для классификации и отрицательное
                MSE для регрессии. Defaults to None.
        
        Returns:
            tuple[dict, float]: Кортеж, содержащий словарь с лучшими параметрами
            и соответствующее им значение метрики.
        """
        X = np.array(X)
        if isinstance(y, (pd.Series, pd.DataFrame)):
            y = np.array(y).flatten()
        else:
            y = np.array(y).flatten()
            
        n_samples = X.shape[0]
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        fold_sizes = (n_samples // cv) * np.ones(cv, dtype=int)
        fold_sizes[:n_samples % cv] += 1
        current = 0
        folds = []
        for fold_size in fold_sizes:
            test_idx = indices[current:current+fold_size]
            train_idx = np.concatenate([indices[:current], indices[current+fold_size:]])
            folds.append((train_idx, test_idx))
            current += fold_size
        
        if scoring is None:
            if self.task == "classification":
                scoring = lambda true, pred: np.mean(true == pred)
            elif self.task == "regression":
                scoring = lambda true, pred: -np.mean((true - pred)**2)
            else:
                raise ValueError("Неподдерживаемый тип задачи")
        
        best_score = -np.inf if self.task=="classification" else np.inf
        best_params = {}
        
        for k_val in param_grid.get('k', [self.k]):
            for h_val in param_grid.get('h', [self.h]):
                scores = []
                for train_idx, test_idx in folds:
                    X_train_cv, X_test_cv = X[train_idx], X[test_idx]
                    y_train_cv, y_test_cv = y[train_idx], y[test_idx]
                    self.fit(X_train_cv, y_train_cv)
                    self.k = k_val
                    self.h = h_val
                    y_pred_cv = self.predict(X_test_cv)
                    scores.append(scoring(y_test_cv, y_pred_cv))
                avg_score = np.mean(scores)
                if self.task == "classification":
                    if avg_score > best_score:
                        best_score = avg_score
                        best_params = {'k': k_val, 'h': h_val}
                else:  # regression
                    if avg_score > best_score:
                        best_score = avg_score
                        best_params = {'k': k_val, 'h': h_val}
        self.k = best_params.get('k', self.k)
        self.h = best_params.get('h', self.h)
        return best_params, best_score
    
    def accuracy_score(self, y_true, y_pred):
        """
        Вычисляет точность (accuracy) для задачи классификации.

        Args:
            y_true (array-like): Истинные метки.
            y_pred (array-like): Предсказанные метки.

        Returns:
            float: Значение точности.
        """
        y_true = np.array(y_true).flatten()
        y_pred = np.array(y_pred).flatten()
        return np.mean(y_true == y_pred)
    
    def plot(self, X, y):
        """
        Визуализирует обучающую выборку и тестовые точки (для 2D данных).
        """
        if self.X_train is None:
            raise ValueError("Необходимо вызвать fit для установки обучающей выборки.")
        X_train = np.array(self.X_train)
        y_train = np.array(self.y_train)
        X = np.array(X)
        y = np.array(y)
        
        plt.figure(figsize=(8,6))
        plt.scatter(X_train[:,0], X_train[:,1], c=y_train, marker='o', label='Обучающая выборка')
        plt.scatter(X[:,0], X[:,1], c=y, marker='x', label='Целевые точки')
        plt.xlabel("Признак 1")
        plt.ylabel("Признак 2")
        plt.title("k-NN: Обучающая и целевая выборка")
        plt.legend()
        plt.show()
#######################################################################################################################      
KNNS = [KNN]