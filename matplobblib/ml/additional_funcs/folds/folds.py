import numpy as np
def Kfold_split(n_samples, n_splits=5, shuffle=True, random_state=None):
        """
        Генерирует индексы для разделения данных на обучающие и тестовые наборы (K-Fold).
        
        Args:
            n_samples (int): Общее количество образцов в данных.
            n_splits (int, optional): Количество фолдов (частей). Defaults to 5.
            shuffle (bool, optional): Перемешивать ли данные перед разбиением.
                Defaults to True.
            random_state (int, optional): Зерно для генератора случайных чисел
                для воспроизводимости перемешивания. Defaults to None.
          
        Yields:
            tuple[np.ndarray, np.ndarray]: Кортеж, содержащий индексы для
            обучающего и тестового наборов для каждой итерации.
        """
        indices = np.arange(n_samples)
        if shuffle:
            rng = np.random.default_rng(random_state)
            rng.shuffle(indices)
        fold_sizes = (n_samples // n_splits) * np.ones(n_splits, dtype=int)
        fold_sizes[:n_samples % n_splits] += 1
        current = 0
        for fold_size in fold_sizes:
            test_indices = indices[current:current + fold_size]
            train_indices = np.concatenate([indices[:current], indices[current + fold_size:]])
            yield train_indices, test_indices
            current += fold_size

FOLDS = [Kfold_split]