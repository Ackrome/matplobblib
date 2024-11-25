from matplotlib.patches import Patch
from collections import Counter
from graphviz import Digraph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#######################################################################################################################
# Реализация дерева решений
#######################################################################################################################
class DecisionTree:
    """Класс дерева решений
    """
    def __init__(self,model_type = 'Classifier', max_depth=None, min_samples_leaf=1, max_leaves=None, criterion="gini", check_k_threshold=0, min_gain=0.01, class_weights=None, chek_k_features=0):
        """
        Класс дерева решений
        --------------------------
        Params:
        :param model_type: `'Classifier'` or `'Regressor'`
        :param max_depth: Максимальная глубина дерева
        :param min_samples_leaf: Минимальное количество объектов в листе
        :param max_leaves: Максимальное количество листьев
        :param criterion: Критерий для оценки качества разбиения из [`gini`,`entropy`,`misclassification`,`mae`,`mse`]
            - gini - критерий Жини
            - entropy - критерий энтропии
            - misclassification - критерий ошибок классификации
            - mae - критерий средней абсолютной ошибки
            - mse - критерий средней квадратичной ошибки
        :param check_k_threshold: Параметр для оценки качества разбиения<br>- k=0 - проверка на всех уникальных объектах в листе<br> - k>=1 - проверка на k уникальных объектах в листе.
        :param min_gain: Минимальное улучшение качества разбиения.
        :param class_weights: Словарь вида {class: weight}, определяющий веса для классов.
        :param chek_k_features: Сколько случайных столбцов проверять при каждом разделении.
        """
        self.model_type = model_type
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_leaves = max_leaves
        
        self.criterion = criterion.lower()  # Приводим к нижнему регистру для унификации
        assert (model_type=='Regressor' and criterion in ['mse','mae']) or (model_type=='Classifier' and criterion in ['gini','entropy','misclassification','mae','mse']), 'Неправильно выбрана функция информативности'
        
        self.check_k_threshold = check_k_threshold
        assert self.check_k_threshold >= 0, 'Параметр check_k_threshold должен быть неотрицательным'
        if self.check_k_threshold == 0:
            self.check_k_threshold = np.inf
        
        self.min_gain = min_gain
        if self.min_gain == None:
            self.min_gain = 0
        assert self.min_gain >= 0, 'Параметр min_gain должен быть неотрицательным'
        
        self.tree = None
        self.leaf_count = 0  # Счетчик листьев
        
        self.class_weights = class_weights  # Поддержка весов классов
        assert isinstance(self.class_weights, dict) or self.class_weights is None, 'class_weights должен быть словарем вида {class: weight}'
        
        self.chek_k_features = chek_k_features
        

        # Проверяем корректность критерия
        valid_criteria = {"gini", "entropy", "misclassification", "mae", "mse"}
        if self.criterion not in valid_criteria:
            raise ValueError(f"Некорректный критерий '{criterion}'. Выберите из {valid_criteria}.")

    def fit(self, X, y):
        """
        Обучает модель дерева решений на заданных данных.

        Args:
            X (array-like): Матрица признаков, где каждая строка соответствует одному образцу,
                            а каждый столбец - одному признаку.
            y (array-like): Вектор целевых значений, где каждый элемент соответствует целевому 
                            значению для соответствующей строки в X.

        Построение дерева начинается с вызова рекурсивной функции `build_tree`.
        """
        # Проверяем корректность весов
        if self.class_weights==None:
            self.class_weights = {cls: 1 for cls in np.unique(y)}
        else:
            unique_classes = np.unique(y)
            for cls in unique_classes:
                if cls not in list(self.class_weights.keys()):
                    raise ValueError(f"Класс {cls} отсутствует в class_weights.")
        
        if self.chek_k_features>X.shape[1]:
            self.chek_k_features=X.shape[1]
            print(f'chek_k_features({self.chek_k_features}) не может быть больше, чем столбцов в X. chek_k_features взято за количество столбцов в X ')
        
        # Построение дерева начинается с вызова рекурсивной функции `build_tree`
        self.leaf_count = 0  # Сбрасываем счетчик листьев перед обучением
        self.tree = self.build_tree(X, y)

    def build_tree(self, X, y, depth=0):
        """
        Построение дерева решений
        --------------------------
        
        Рекурсивная функция, которая строит дерево решений.
        
        Args:
            X (array-like): Матрица признаков.
            y (array-like): Вектор целевых значений.
            depth (int, optional): Текущая глубина дерева. Defaults to 0.
        
        Returns:
            dict: Словарь, содержащий информацию о текущей вершине дерева.
        """
        # Условие остановки рекурсии
        if (
            (self.max_depth is not None and depth >= self.max_depth)  # Превышена глубина
            or len(set(y)) == 1  # Все элементы относятся к одному классу
            or len(y) < self.min_samples_leaf  # Мало объектов для деления
            or (self.max_leaves is not None and self.leaf_count >= self.max_leaves)  # Превышено количество листьев
        ):
            self.leaf_count += 1  # Создаем новый лист
            return self.majority_class(y)

        # Найти лучшее разбиение
        feature, threshold = self.best_split(X, y)
        if feature is None:
            self.leaf_count += 1  # Если деление невозможно, создаем лист
            return self.majority_class(y)
        
        # Разделить данные на левое и правое поддеревья
        left_indices = X[:, feature] < threshold
        right_indices = X[:, feature] >= threshold

        left_child = self.build_tree(X[left_indices], y[left_indices], depth + 1)
        right_child = self.build_tree(X[right_indices], y[right_indices], depth + 1)

        return {"feature": feature, "threshold": threshold, "left": left_child, "right": right_child}

    def best_split(self, X, y):
        # Найти лучшее разбиение
        """
        Вычисляет лучшее разбиение данных, чтобы минимизировать или максимизировать указанный критерий.

        Args:
            X (array-like): Матрица признаков, где каждая строка представляет объект, а каждый столбец - признак.
                            
            y (array-like): Целевые значения, соответствующие каждому объекту в X.

        Returns:
            tuple: Кортеж, содержащий индекс лучшего признака и значение порога для разбиения данных.
        """

        best_feature, best_threshold = None, None
        
        # Устанавливаем начальное значение метрики в зависимости от типа критерия
        if self.criterion in {"gini", "entropy", "mae", "mse"}:
            best_metric = float("inf")  # Минимизируем
        elif self.criterion == "misclassification":
            best_metric = -float("inf")  # Максимизируем
        
        n_samples, n_features = X.shape

        if self.chek_k_features==0:
            features = list(range(n_features))
        else:
            features = np.random.choice(list(range(n_features)),self.chek_k_features,False)
            
        for feature in features:
            unique_values = np.unique(X[:, feature])
            
            if self.check_k_threshold==0:
                thresholds = unique_values  # Если k = 0, берем все.
            else:
                thresholds = np.linspace(unique_values.min(), unique_values.max(), self.check_k_threshold)
    
            
            
            for threshold in thresholds:
                left_indices = X[:, feature] < threshold
                right_indices = X[:, feature] >= threshold
                
                # Проверяем минимальное количество объектов в листе
                if (
                    len(left_indices[left_indices]) < self.min_samples_leaf
                    or len(right_indices[right_indices]) < self.min_samples_leaf
                ):
                    continue

                metric = self.split_metric(y[left_indices], y[right_indices])

                # Обновляем лучший критерий в зависимости от его направления (минимизация/максимизация)
                if (
                    (self.criterion in {"gini", "entropy", "mae", "mse"} and metric < best_metric)
                    or (self.criterion == "misclassification" and metric > best_metric)
                ) and abs(metric-best_metric) >= self.min_gain:
                    best_metric, best_feature, best_threshold = metric, feature, threshold

        return best_feature, best_threshold


    def split_metric(self, left_y, right_y):
        """
        Вычисляет критерий для разделения.
        
        Args:
            left_y (array-like): Вектор целевых значений для левого поддерева.
            right_y (array-like): Вектор целевых значений для правого поддерева.
        
        Returns:
            numerical: Критерий для разделения.
        """
        if self.criterion == "gini":
            return self.gini_index(left_y, right_y)
        elif self.criterion == "entropy":
            return self.entropy_index(left_y, right_y)
        elif self.criterion == "misclassification":
            return self.misclassification_error(left_y, right_y)
        elif self.criterion == "mae":
            return self.mean_absolute_error(left_y, right_y)
        elif self.criterion == "mse":
            return self.mean_squared_error(left_y, right_y)

    
    def gini_index(self, left_y, right_y):
        """
        Вычисляет критерий Джини для измерения неоднородности

        Args:
            left_y (array-like): Вектор целевых значений для левого поддерева.
            right_y (array-like): Вектор целевых значений для правого поддерева.

        Returns:
            numerical: Критерий Джини.
        """
        def gini(y):
            counts = Counter(y)
            total = sum(self.class_weights.get(cls, 1) * count for cls, count in counts.items())
            return 1 - sum((self.class_weights.get(cls, 1) * count / total) ** 2 for cls, count in counts.items())

        n = len(left_y) + len(right_y)
        left_weighted = (len(left_y) / n) * gini(left_y)
        right_weighted = (len(right_y) / n) * gini(right_y)
        return left_weighted + right_weighted
    

    def entropy_index(self, left_y, right_y):
        """
        Вычисляет энтропийный индекс для измерения неоднородности.

        Args:
            left_y (array-like): Вектор целевых значений для левого поддерева.
            right_y (array-like): Вектор целевых значений для правого поддерева.

        Returns:
            numerical: Энтропийный индекс.
        """
        def entropy(y):
            counts = Counter(y)
            total = sum(self.class_weights.get(cls, 1) * count for cls, count in counts.items())
            return -sum((self.class_weights.get(cls, 1) * count / total) * 
                        np.log2((self.class_weights.get(cls, 1) * count / total))
                        for cls, count in counts.items() if count > 0)

        n = len(left_y) + len(right_y)
        left_weighted = (len(left_y) / n) * entropy(left_y)
        right_weighted = (len(right_y) / n) * entropy(right_y)
        return left_weighted + right_weighted


    def misclassification_error(self, left_y, right_y):
        """
        Вычисляет критерий ошибки классификации (misclassification error)

        Args:
            left_y (array-like): Вектор целевых значений для левого поддерева.
            right_y (array-like): Вектор целевых значений для правого поддерева.

        Returns:
            numerical: Критерий ошибки классификации.
        """
        def misclass_error(y):
            # Считаем количество объектов каждого класса
            counts = Counter(y)
            # Учитываем веса классов
            total_weight = sum(self.class_weights.get(cls, 1) * count for cls, count in counts.items())
            # Определяем частоту самого популярного класса с учетом весов
            max_class_weighted_freq = max(self.class_weights.get(cls, 1) * count / total_weight for cls, count in counts.items())
            # Ошибка классификации = 1 - частота самого популярного класса
            return 1 - max_class_weighted_freq

        n = len(left_y) + len(right_y)  # Общее число объектов
        # Взвешенная ошибка классификации для левого и правого подмножеств
        left_weighted = (len(left_y) / n) * misclass_error(left_y)
        right_weighted = (len(right_y) / n) * misclass_error(right_y)
        return left_weighted + right_weighted


    def mean_absolute_error(self, left_y, right_y):
        """
        Вычисляет критерий средней абсолютной ошибки (MAE)

        Args:
            left_y (array-like): Вектор целевых значений для левого поддерева.
            right_y (array-like): Вектор целевых значений для правого поддерева.

        Returns:
            numerical: Критерий средней абсолютной ошибки.
        """
        def mae(y):
            mean = np.mean(y)
            return np.mean(np.abs(y - mean))

        n = len(left_y) + len(right_y)
        return (len(left_y) / n) * mae(left_y) + (len(right_y) / n) * mae(right_y)

    def mean_squared_error(self, left_y, right_y):
        """
        Вычисляет критерий средней квадратичной ошибки (MSE)

        Args:
            left_y (array-like): Вектор целевых значений для левого поддерева.
            right_y (array-like): Вектор целевых значений для правого поддерева.

        Returns:
            numerical: Критерий средней квадратичной ошибки.
        """
        def mse(y):
            mean = np.mean(y)
            return np.mean((y - mean) ** 2)

        n = len(left_y) + len(right_y)
        return (len(left_y) / n) * mse(left_y) + (len(right_y) / n) * mse(right_y)

     
    def majority_class(self, y):
        """
        Определяет большинственный класс

        Args:
            y (array-like): Массив целевых значений

        Returns:
            object: Большинственный класс
        """
        counts = Counter(y)
        weighted_counts = {cls: count * self.class_weights.get(cls, 1) for cls, count in counts.items()}
        return max(weighted_counts, key=weighted_counts.get) if self.model_type == "Classifier" else np.mean(y)


    def predict(self, X):
        """
        Проводит предсказание по каждому образцу из `X`

        Args:
            X (array-like): Матрица признаков

        Returns:
            array-like: Предсказанные значения
        """
        return np.array([self._predict(sample, self.tree) for sample in X])

    def _predict(self, sample, tree):
        """
        Рекурсивное предсказание для каждого узла дерева

        Args:
            sample (array-like): Образец, для которого нужно предсказать значение.
            tree (dict): Словарь, содержащий информацию о текущей вершине дерева.

        Returns:
            object: Предсказанное значение.
        """
        if not isinstance(tree, dict):
            return tree

        feature = tree["feature"]
        threshold = tree["threshold"]
        if sample[feature] < threshold:
            return self._predict(sample, tree["left"])
        else:
            return self._predict(sample, tree["right"])

    def visualize_tree(self):
        """
        Возвращает граф, изображающий дерево решений.

        Returns:
            graphviz.Digraph: Граф, изображающий дерево решений.
        """
        dot = Digraph()
        self._add_nodes_edges(dot, self.tree)
        dot.render("decision_tree", format="png", cleanup=True)  # Сохранить дерево как PNG
        return dot

    def _add_nodes_edges(self, dot, tree, parent=None, edge_label=""):
        """
        Рекурсивно добавляет узлы и ребра к графу, представляющему дерево решений.

        Args:
            dot (graphviz.Digraph): Граф, в который добавляются узлы и ребра.
            tree (dict or object): Информация о текущей вершине дерева.
                Если это листовой узел, то tree - объект, представляющий класс.
                Если это внутренний узел, то tree - словарь, содержащий 
                    "feature" (int): индекс признака, по которому происходит разбиение,
                    "threshold" (float): порог разбиения,
                    "left" (dict or object): левое поддерево,
                    "right" (dict or object): правое поддерево.
            parent (str or None): Идентификатор родительского узла.
            edge_label (str): Метка для ребра, соединяющего текущий узел с родительским.
        """
        # Если это листовой узел, добавляем его как конечный класс
        if not isinstance(tree, dict):
            node_id = str(id(tree))
            dot.node(node_id, label=f"Class: {tree}", shape="ellipse", color="lightblue2", style="filled")
            if parent:
                dot.edge(parent, node_id, label=edge_label)
            return

        # Создаем узел с условием разбиения
        node_id = str(id(tree))
        feature = tree["feature"]
        threshold = tree["threshold"]
        label = f"X[{feature}] < {threshold:.2f}"
        dot.node(node_id, label=label, shape="box", color="lightgrey", style="filled")

        # Если это не корень, добавляем ребро к узлу
        if parent:
            dot.edge(parent, node_id, label=edge_label)

        # Рекурсивно добавляем левое и правое поддеревья
        self._add_nodes_edges(dot, tree["left"], parent=node_id, edge_label="True")
        self._add_nodes_edges(dot, tree["right"], parent=node_id, edge_label="False")

    def plot_decision_boundaries(self, X, y, feature_indices=(0, 1), resolution=100, figsize=(8, 6)):
        """
        Визуализирует области пространства, принадлежащие различным классам (поддержка нескольких классов).
        
        Параметры:
        ----------
        X : ndarray
            Матрица признаков (n_samples, n_features).
        y : ndarray
            Вектор меток классов (n_samples,).
        feature_indices : tuple (default=(0, 1))
            Индексы признаков, которые будут использоваться для построения областей.
        resolution : int (default=100)
            Количество точек на единицу длины сетки (для сглаживания).
        figsize : tuple (default=(8, 6))
            Размер изображения.
        """
        if len(feature_indices) != 2:
            raise ValueError("Для визуализации выберите ровно 2 признака.")

        feature1, feature2 = feature_indices
        x_min, x_max = X[:, feature1].min() - 1, X[:, feature1].max() + 1
        y_min, y_max = X[:, feature2].min() - 1, X[:, feature2].max() + 1

        # Создаем сетку точек
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, resolution),
            np.linspace(y_min, y_max, resolution)
        )
        grid_points = np.c_[xx.ravel(), yy.ravel()]

        # Предсказываем классы для каждой точки сетки
        full_dim_grid = np.zeros((grid_points.shape[0], X.shape[1]))
        full_dim_grid[:, feature1] = grid_points[:, 0]
        full_dim_grid[:, feature2] = grid_points[:, 1]
        grid_predictions = self.predict(full_dim_grid).reshape(xx.shape)

        # Визуализируем границы
        plt.figure(figsize=figsize)
        n_classes = len(set(y))
        cmap_background = plt.get_cmap("tab20", n_classes)
        cmap_points = plt.get_cmap("viridis", n_classes)

        plt.contourf(xx, yy, grid_predictions, alpha=0.3, cmap=cmap_background)
        scatter = plt.scatter(X[:, feature1], X[:, feature2], c=y, cmap=cmap_points, edgecolor="k", s=30)

        plt.xlabel(f"Feature {feature1}")
        plt.ylabel(f"Feature {feature2}")
        plt.title("Decision Boundaries")

        if self.model_type!='Regressor':
            # Добавляем легенду
            legend1 = plt.legend(*scatter.legend_elements(), title="Classes (Points)", loc="upper right")
            plt.gca().add_artist(legend1)

            # Добавляем таблицу цветов фона
            class_patches = [
                Patch(color=cmap_background(i), label=f"Class {i}") for i in range(n_classes)
            ]
            legend2 = plt.legend(handles=class_patches, title="Classes (Background)", loc="lower right")
            plt.gca().add_artist(legend2)
        
        plt.show()
    
    def plot_regr(self, y_true, y_pred):
        """
        Нарисовать график рассеяния истинных и предсказанных значений для моделей регрессии.

        Аргументы:
            y_true (array-like): истинные целевые значения.
            y_pred (array-like): предсказанные целевые значения.

        Примечания:
            Эта функция применяется только для моделей регрессии (т.е., `self.model_type == 'Regressor'`).

        Возвращает:
            None
        """
        assert self.model_type == 'Regressor', 'Эта функция только для регрессии'
        plt.scatter(y_true, y_pred)
        plt.scatter(y_true, y_true)
        plt.show()
#######################################################################################################################
TREES = [DecisionTree]