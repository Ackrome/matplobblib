from ...forall import *
#######################################################################################################################
# Логистическая регрессия
#######################################################################################################################
class LogisticRegression:
    """Логистическая регрессия с использованием градиентного спуска."""
    def __init__(self):
        self.w = None  # Вектор весов (numpy array, shape: (n_features, 1))
    
    def predict_proba(self, X):
        """
        Вычисляет вероятность принадлежности к классу 1.
        
        Аргументы:
          X (array-like): Матрица признаков размера (n_samples, n_features).
          
        Возвращает:
          numpy.array: Вероятности для каждого объекта, shape (n_samples,).
        """
        X = np.array(X)
        z = X @ self.w  # Линейная комбинация, shape: (n_samples, 1)
        return self.sigm(z).flatten()  # Приводим к 1D массиву
    
    def predict(self, X, threshold=0.5):
        """
        Предсказывает классы (0 или 1) для объектов.
        
        Аргументы:
          X (array-like): Матрица признаков размера (n_samples, n_features).
          threshold (float): Порог классификации, по умолчанию 0.5.
          
        Возвращает:
          numpy.array: Вектор предсказанных классов (0 или 1).
        """
        proba = self.predict_proba(X)
        return np.where(proba >= threshold, 1, 0)
    
    def loss(self, X, y):
        """
        Вычисляет логарифмическую функцию потерь (log loss).
        
        Аргументы:
          X (array-like): Матрица признаков размера (n_samples, n_features).
          y (array-like): Вектор истинных меток (0 или 1), shape (n_samples,).
          
        Возвращает:
          float: Среднее значение логарифмической потери.
        """
        proba = self.predict_proba(X)
        # Для избежания log(0) ограничим значения вероятностей eps
        eps = 1e-15
        proba = np.clip(proba, eps, 1 - eps)
        y = np.array(y)
        return -np.mean(y * np.log(proba) + (1 - y) * np.log(1 - proba))
    
    def fit(self, X, y, learning_rate=0.1, n_iter=1000):
        """
        Обучение модели с помощью градиентного спуска.
        
        Аргументы:
          X (array-like): Матрица признаков размера (n_samples, n_features).
          y (array-like): Вектор истинных меток (0 или 1), shape (n_samples,).
          learning_rate (float): Скорость обучения.
          n_iter (int): Количество итераций обучения.
        """
        X = np.array(X)
        y = np.array(y).reshape(-1, 1)  # Приводим к вектору-столбцу
        n_samples, n_features = X.shape
        
        # Инициализируем веса единицами
        self.w = np.ones((n_features, 1))
        
        for i in range(n_iter):
            z = X @ self.w                   # (n_samples, 1)
            predictions = self.sigm(z)   # (n_samples, 1)
            # Градиент: X.T @ (predictions - y) / n_samples
            grad = X.T @ (predictions - y) / n_samples
            self.w -= learning_rate * grad
            # (Опционально можно выводить значение потерь каждые 100 итераций)
            # if i % 100 == 0:
            #     print(f"Iteration {i}, loss: {self.loss(X, y.flatten())}")
    
    def accuracy_score(self, X, y):
        """
        Вычисляет точность модели (accuracy).
        
        Аргументы:
          X (array-like): Матрица признаков.
          y (array-like): Вектор истинных меток (0 или 1).
          
        Возвращает:
          float: Доля правильно предсказанных объектов.
        """
        y_pred = self.predict(X)
        y = np.array(y)
        return np.mean(y_pred == y)
    
    def plot(self, X, y):
        """
        Визуализирует разделяющую границу для двумерных данных.
        
        Аргументы:
          X (array-like): Матрица признаков размера (n_samples, 2).
          y (array-like): Вектор истинных меток (0 или 1).
        """
        X = np.array(X)
        y = np.array(y)
        if X.shape[1] != 2:
            raise ValueError("Метод plot поддерживает только двумерные данные.")
        
        h = 0.02  # шаг сетки
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        grid = np.c_[xx.ravel(), yy.ravel()]
        Z = self.predict(grid)
        Z = Z.reshape(xx.shape)
        
        plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
        plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.coolwarm)
        plt.title("Логистическая регрессия: разделяющая граница")
        plt.xlabel("Признак 1")
        plt.ylabel("Признак 2")
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.show()
  
CM = [LogisticRegression]