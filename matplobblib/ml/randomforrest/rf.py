from ..tree.trees import *
import numpy as np
from collections import Counter


class RandomForest:
    """
    Класс для реализации алгоритма Random Forest.
    """

    def __init__(
            self,
            n_trees=100,
            model_type='Classifier',
            max_depth=None,
            min_samples_leaf=1,
            max_leaves=None,
            criterion="gini",
            check_k_threshold=0,
            min_gain=0.01,
            class_weights=None,
            chek_k_features=0,
            bootstrap=True):
        """
        Инициализация параметров случайного леса.

        Args:
            n_trees (int): Количество деревьев в лесу.
            model_type (str): Тип модели ('Classifier' или 'Regressor').
            max_depth (int): Максимальная глубина каждого дерева.
            min_samples_leaf (int): Минимальное количество объектов в листе.
            max_leaves (int): Максимальное количество листьев.
            criterion (str): Критерий разбиения ('gini', 'entropy', 'mse', и т.д.).
            check_k_threshold (int): Параметр для проверки качества разбиения.
            min_gain (float): Минимальное улучшение качества разбиения.
            class_weights (dict): Веса классов для задачи классификации.
            chek_k_features (int): Количество случайных признаков для разбиения.
            bootstrap (bool): Использовать ли бутстрэп (случайные подвыборки с повторением).
        """
        self.n_trees = n_trees
        self.model_type = model_type
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_leaves = max_leaves
        self.criterion = criterion
        self.check_k_threshold = check_k_threshold
        self.min_gain = min_gain
        self.class_weights = class_weights
        self.chek_k_features = chek_k_features
        self.bootstrap = bootstrap
        self.trees = []  # Список для хранения деревьев

    def fit(self, X, y):
        """
        Обучение случайного леса.

        Args:
            X (array-like): Матрица признаков.
            y (array-like): Вектор целевых значений.
        """
        self.trees = []
        n_samples, n_features = X.shape

        for _ in range(self.n_trees):
            # Создаем случайную подвыборку с повторением (бутстрэп)
            if self.bootstrap:
                indices = np.random.choice(n_samples, n_samples, replace=True)
                X_bootstrap = X[indices]
                y_bootstrap = y[indices]
            else:
                X_bootstrap = X
                y_bootstrap = y

            # Создаем и обучаем дерево
            tree = DecisionTree(
                model_type=self.model_type,
                max_depth=self.max_depth,
                min_samples_leaf=self.min_samples_leaf,
                max_leaves=self.max_leaves,
                criterion=self.criterion,
                check_k_threshold=self.check_k_threshold,
                min_gain=self.min_gain,
                class_weights=self.class_weights,
                chek_k_features=self.chek_k_features
            )
            tree.fit(X_bootstrap, y_bootstrap)
            self.trees.append(tree)

    def predict(self, X):
        """
        Предсказание случайного леса.

        Args:
            X (array-like): Матрица признаков.

        Returns:
            array-like: Предсказанные значения.
        """
        if self.model_type == 'Classifier':
            return self._predict_classifier(X)
        elif self.model_type == 'Regressor':
            return self._predict_regressor(X)

    def _predict_classifier(self, X):
        """
        Предсказание для задачи классификации (голосование).

        Args:
            X (array-like): Матрица признаков.

        Returns:
            array-like: Предсказанные метки классов.
        """
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        majority_vote = np.apply_along_axis(lambda x: Counter(x).most_common(1)[
            0][0], axis=0, arr=tree_predictions)
        return majority_vote

    def _predict_regressor(self, X):
        """
        Предсказание для задачи регрессии (усреднение).

        Args:
            X (array-like): Матрица признаков.

        Returns:
            array-like: Усредненные предсказанные значения.
        """
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.mean(tree_predictions, axis=0)

    def feature_importances(self, X, y):
        """
        Вычисление важности признаков на основе суммарного снижения неоднородности (impurity decrease)
        по всем деревьям случайного леса.

        Аргументы:
            X (numpy.ndarray): Матрица признаков (n_samples, n_features), желательно те данные, на которых обучалась модель.
            y (numpy.ndarray): Истинные метки (или значения) целевой переменной, соответствующие X.

        Возвращает:
            numpy.ndarray: Вектор важностей признаков, сумма которого равна 1.
        """
        total_samples = len(y)
        n_features = X.shape[1]
        importances = np.zeros(n_features)

        def compute_impurity(y_subset):
            if len(y_subset) == 0:
                return 0
            if self.criterion == "gini":
                counts = Counter(y_subset)
                total = sum(
                    self.class_weights.get(
                        cls,
                        1) * count for cls,
                    count in counts.items())
                return 1 - sum((self.class_weights.get(cls, 1) * \
                               count / total) ** 2 for cls, count in counts.items())
            elif self.criterion == "entropy":
                counts = Counter(y_subset)
                total = sum(
                    self.class_weights.get(
                        cls,
                        1) * count for cls,
                    count in counts.items())
                return -sum((self.class_weights.get(cls, 1) * count / total) *
                            np.log2(self.class_weights.get(cls, 1) * count / total)
                            for cls, count in counts.items() if count > 0)
            elif self.criterion == "misclassification":
                counts = Counter(y_subset)
                total = sum(
                    self.class_weights.get(
                        cls,
                        1) * count for cls,
                    count in counts.items())
                max_prob = max(
                    self.class_weights.get(
                        cls,
                        1) * count / total for cls,
                    count in counts.items())
                return 1 - max_prob
            elif self.criterion == "mse":
                mean_y = np.mean(y_subset)
                return np.mean((y_subset - mean_y) ** 2)
            elif self.criterion == "mae":
                mean_y = np.mean(y_subset)
                return np.mean(np.abs(y_subset - mean_y))
            else:
                return 0

        def traverse_tree(node, indices):
            # Если узел — лист, прекращаем рекурсию
            if not isinstance(node, dict):
                return
            feature = node["feature"]
            threshold = node["threshold"]

            # Вычисляем impurity в текущем узле
            y_node = y[indices]
            impurity_parent = compute_impurity(y_node)

            # Определяем индексы объектов для левого и правого поддеревьев
            left_mask = X[indices, feature] < threshold
            right_mask = ~left_mask  # или X[indices, feature] >= threshold
            left_indices = indices[left_mask]
            right_indices = indices[right_mask]

            # Если разделение не эффективно, пропускаем данный узел
            if len(left_indices) == 0 or len(right_indices) == 0:
                return

            impurity_left = compute_impurity(y[left_indices])
            impurity_right = compute_impurity(y[right_indices])
            n_node = len(indices)
            weighted_impurity = (len(left_indices) / n_node) * impurity_left + \
                (len(right_indices) / n_node) * impurity_right
            impurity_decrease = impurity_parent - weighted_impurity

            # Взвешиваем вклад по числу объектов, попавших в узел
            importance_contribution = (
                n_node / total_samples) * impurity_decrease
            importances[feature] += importance_contribution

            # Рекурсивно обрабатываем поддеревья
            traverse_tree(node["left"], left_indices)
            traverse_tree(node["right"], right_indices)

        # Для каждого дерева случайного леса запускаем обход от корня со всеми
        # объектами
        indices = np.arange(total_samples)
        for tree in self.trees:
            traverse_tree(tree.tree, indices)

        # Нормализуем итоговый вектор важностей так, чтобы их сумма была равна
        # 1
        total_importance = np.sum(importances)
        if total_importance > 0:
            importances = importances / total_importance
        return importances


RF = [RandomForest]