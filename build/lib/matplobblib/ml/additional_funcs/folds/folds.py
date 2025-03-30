import numpy as np
def Kfold_split(n_samples, n_splits=5, shuffle=True, random_state=None):
        """
        Реализация KFold-разбиения.
        
        Параметры:
          n_samples: общее число образцов
          n_splits: число фолдов
          shuffle: перемешивать ли индексы перед разбиением
          random_state: зерно генератора случайных чисел
          
        Возвращает:
          Генератор кортежей (train_indices, test_indices)
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