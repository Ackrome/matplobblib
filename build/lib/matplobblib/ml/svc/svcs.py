from ...forall import *
from cvxopt import matrix, solvers

from ..additional_funcs.folds import Kfold_split
class SVC:
    def __init__(self, kernel='linear', C=None, kernel_params=None):
        """
        Инициализация SVC.

        Параметры:
          kernel: тип ядра ('linear', 'polynomial', 'rbf')
          C: параметр регуляризации; если None, то будет подобран автоматически
          kernel_params: словарь с параметрами ядра (например, degree для полиномиального или sigma для RBF)
        """
        self.kernel = kernel
        self.C = C
        self.kernel_params = kernel_params if kernel_params is not None else {}
        self.alphas = None
        self.sv_X = None
        self.sv_y = None
        self.b = None
    

    def _kernel_function(self, x1, x2):
        """
        Вычисление ядра между векторами x1 и x2.
        """
        if self.kernel == 'linear':
            return np.dot(x1, x2)
        elif self.kernel == 'polynomial':
            degree = self.kernel_params.get('degree', 3)
            coef0 = self.kernel_params.get('coef0', 1)
            return (np.dot(x1, x2) + coef0) ** degree
        elif self.kernel == 'rbf':
            sigma = self.kernel_params.get('sigma', 1.0)
            return np.exp(-np.linalg.norm(x1 - x2) ** 2 / (2 * sigma ** 2))
        else:
            raise ValueError("Неподдерживаемое ядро. Выберите 'linear', 'polynomial' или 'rbf'.")

    def _tune_C(self, X, y, folds=5, candidates=None):
        """
        Автоматический подбор параметра регуляризации C с помощью кросс-валидации.
        
        Параметры:
          X: массив признаков размером (n_samples, n_features)
          y: вектор меток (-1 или 1) размером (n_samples,)
          folds: число фолдов для кросс-валидации (по умолчанию 5)
          candidates: список кандидатов для C; если None, используются значения [0.01, 0.1, 1, 10, 100]
        
        Возвращает:
          Оптимальное значение C, дающее наилучший средний результат по кросс-валидации.
        """
        if candidates is None:
            candidates = [0.01, 0.1, 1, 10, 100]
        best_score = -np.inf
        best_C = None
        n_samples = X.shape[0]

        for candidate in candidates:
            scores = []
            # Используем нашу функцию _kfold_split вместо sklearn
            for train_index, val_index in Kfold_split(n_samples, n_splits=folds, shuffle=True, random_state=42):
                X_train, X_val = X[train_index], X[val_index]
                y_train, y_val = y[train_index], y[val_index]
                # Создаем новую модель с текущим кандидатом для C
                svc_candidate = SVC(kernel=self.kernel, C=candidate, kernel_params=self.kernel_params)
                svc_candidate.fit(X_train, y_train)
                scores.append(svc_candidate.score(X_val, y_val))
            avg_score = np.mean(scores)
            if avg_score > best_score:
                best_score = avg_score
                best_C = candidate
        return best_C

    def fit(self, X, y):
        """
        Обучение модели SVC по обучающей выборке.

        Параметры:
          X: массив признаков размером (n_samples, n_features)
          y: вектор меток (-1 или 1) размером (n_samples,)
        """
        # Если параметр C не задан, подбираем его автоматически с помощью кросс-валидации
        if self.C is None:
            self.C = self._tune_C(X, y)
            print(f"Подобрано оптимальное значение C = {self.C}")

        n_samples, n_features = X.shape

        # Вычисляем матрицу Грама (K)
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i, j] = self._kernel_function(X[i], X[j])

        # Формулировка задачи квадратичного программирования:
        # Минимизировать (1/2)α^T P α – q^T α при ограничениях: 0 <= α_i <= C
        P = matrix(np.outer(y, y) * K)
        q = matrix(-np.ones(n_samples))
        G_top = -np.eye(n_samples)
        G_bottom = np.eye(n_samples)
        G = matrix(np.vstack((G_top, G_bottom)))
        h_top = np.zeros(n_samples)
        h_bottom = np.ones(n_samples) * self.C
        h = matrix(np.hstack((h_top, h_bottom)))
        A = matrix(y, (1, n_samples), tc='d')
        b = matrix(0.0)

        solvers.options['show_progress'] = False
        solution = solvers.qp(P, q, G, h, A, b)
        alphas = np.ravel(solution['x'])

        # Опорные векторы: те, для которых α > eps
        sv = alphas > 1e-5
        self.alphas = alphas[sv]
        self.sv_X = X[sv]
        self.sv_y = y[sv]

        # Вычисляем сдвиг b по условию KKT для опорных векторов
        self.b = 0
        for i in range(len(self.alphas)):
            self.b += self.sv_y[i] - np.sum(
                self.alphas * self.sv_y *
                np.array([self._kernel_function(self.sv_X[i], sv_x) for sv_x in self.sv_X])
            )
        self.b /= len(self.alphas)

    def project(self, X):
        """
        Вычисление значений функции принятия решения для объектов X.

        Параметры:
          X: массив объектов размером (n_samples, n_features)

        Возвращает:
          Массив значений функции принятия решения.
        """
        y_predict = np.zeros(len(X))
        for i in range(len(X)):
            s = 0
            for alpha, sv_y, sv in zip(self.alphas, self.sv_y, self.sv_X):
                s += alpha * sv_y * self._kernel_function(X[i], sv)
            y_predict[i] = s
        return y_predict + self.b

    def predict(self, X):
        """
        Предсказывает метки классов (-1 или 1) для объектов X.

        Параметры:
          X: массив объектов размером (n_samples, n_features)

        Возвращает:
          Вектор предсказанных меток.
        """
        return np.sign(self.project(X))

    def score(self, X, y):
        """
        Вычисляет точность модели на заданных данных.

        Параметры:
          X: массив объектов размером (n_samples, n_features)
          y: истинные метки классов размером (n_samples,)

        Возвращает:
          Точность (доля правильно предсказанных объектов).
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)

    def visualize(self, X, y):
        """
        Визуализация границы принятия решения, отступов и опорных векторов.
        Работает только для двумерных данных.

        Параметры:
          X: массив объектов размером (n_samples, 2)
          y: истинные метки классов размером (n_samples,)
        """
        if X.shape[1] != 2:
            raise ValueError("Визуализация поддерживается только для 2D данных.")

        plt.figure(figsize=(10, 6))
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=30, edgecolors='k')

        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                             np.linspace(y_min, y_max, 300))
        grid = np.c_[xx.ravel(), yy.ravel()]
        Z = self.project(grid)
        Z = Z.reshape(xx.shape)

        plt.contour(xx, yy, Z, levels=[-1, 0, 1],
                    linestyles=['--', '-', '--'], colors='k')
        plt.scatter(self.sv_X[:, 0], self.sv_X[:, 1], s=100,
                    facecolors='none', edgecolors='k', label='Опорные векторы')
        plt.legend()
        plt.title("Граница принятия решения SVC")
        plt.xlabel("Признак 1")
        plt.ylabel("Признак 2")
        plt.show()

SVCS = [SVC]