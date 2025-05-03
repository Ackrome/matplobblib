import numpy as np
from tqdm import tqdm

from ..householder import Householder
from ...eigen.qr import QR_alg
from ...eigen.vectors_from_values import compute_orthonormal_basis

def SVD(F_star, FLOAT_TOLERANCE=1e-12):
    """
    Выполняет сингулярное разложение (SVD) матрицы с использованием структурированного подхода.

    Теоретическое описание:
    Сингулярное разложение (SVD) представляет собой разложение матрицы F* на три матрицы: 
    F* = U * Σ * V^T, где U и V - ортогональные матрицы, а Σ - диагональная матрица сингулярных значений. 
    Алгоритм основан на следующих этапах:
    1. Вычисление матрицы A = F*ᵀF*.
    2. Приведение A к тридиагональной форме методом Хаусхолдера.
    3. Нахождение собственных значений матрицы A через QR-алгоритм.
    4. Вычисление собственных векторов матрицы A с ортогонализацией Грама-Шмидта.
    5. Получение сингулярных значений как квадратных корней из собственных значений.
    6. Вычисление левых сингулярных векторов U через матричное умножение.
    7. Транспонирование V для получения VT.

    Практическая реализация:
    Реализация использует NumPy для матричных операций и tqdm для отслеживания прогресса. 
    При малых сингулярных значениях применяется корректировка обратной матрицы для предотвращения деления на ноль.

    Parameters
    ----------
    F_star : np.ndarray or list of lists
        Входная матрица размерности (m, n), для которой требуется выполнить SVD.
    FLOAT_TOLERANCE : float, optional
        Допустимая погрешность для численных операций. По умолчанию 1e-12.

    Returns
    -------
    U : np.ndarray
        Матрица левых сингулярных векторов размерности (m, m).
    singular_values : np.ndarray
        Вектор сингулярных значений размерности (min(m, n),).
    VT : np.ndarray
        Транспонированная матрица правых сингулярных векторов размерности (n, n).

    Examples
    --------
    >>> import numpy as np
    >>> F_star = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float64)
    >>> U, s, VT = SVD(F_star)
    >>> print("U:", U)
    >>> print("Сингулярные значения:", s)
    >>> print("VT:", VT)

    Notes
    -----
    1. Функция предполагает наличие вспомогательных функций `Householder`, `QR_alg` и `compute_orthonormal_basis`.
    2. Численная нестабильность возможна при малых сингулярных значениях, что требует корректировки обратной матрицы.
    3. Эффективность QR-алгоритма и метода Хаусхолдера зависит от структуры входной матрицы и заданных параметров точности.

    References
    ----------
    .. [3] "SVD для PCA и рекомендательных систем" - (https://example.com/svd-pca)
    .. [7] "Оптимизация SVD для больших матриц" - (https://example.com/svd-optimization)
    .. [8] "Геометрический смысл SVD" - (https://example.com/svd-geometry)
    """
    print("Начало вычисления SVD (структурированный подход с njit и NumPy).")

    # Преобразование входных данных в NumPy массив
    if isinstance(F_star, list):
        print("Преобразование входного списка списков в NumPy массив.")
        F_star_np = np.array(F_star, dtype=np.float64)
    elif isinstance(F_star, np.ndarray):
        print("Использование входного NumPy массива.")
        F_star_np = F_star.astype(np.float64)
    else:
        raise TypeError("Входная матрица F_star должна быть списком списков или NumPy массивом.")

    # Проверка размерности
    if F_star_np.ndim != 2 or F_star_np.size == 0:
        raise ValueError("Входная матрица F_star должна быть непустой двумерной матрицей.")

    # Основные этапы вычислений с прогресс-баром
    steps = [
        "Вычисление A = F*ᵀ × F*",
        "Приведение A к тридиагональной форме (Хаусхолдер)",
        "Нахождение собственных значений A (QR-алгоритм)",
        "Нахождение собственных векторов A (обратная итерация)",
        "Вычисление сингулярных значений",
        "Вычисление левых сингулярных векторов U",
        "Транспонирование V для получения VT"
    ]

    with tqdm(total=len(steps), desc="Процесс SVD") as pbar:

        # Этап 1: Вычисление матрицы A = F_star.T @ F_star
        print(f"Этап 1: {steps[0]}")
        A = F_star_np.T @ F_star_np
        pbar.update(1)
        print("Этап 1 завершен.")

        # Этап 2: Приведение к тридиагональной форме методом Хаусхолдера
        print(f"Этап 2: {steps[1]}")
        H = Householder(A)  # Функция содержит собственный прогресс-бар
        assert all([all([round(H[i][j],5)==0 for j in range(0, i-1)]) for i in range(2, len(H))]), 'Неправильное преобразование хаусхолдера'
        pbar.update(1)
        print("Этап 2 завершен.")

        # Этап 3: Нахождение собственных значений матрицы H через QR-алгоритм
        print(f"Этап 3: {steps[2]}")
        eigenvalues_A = QR_alg(H, miter=500, tol=FLOAT_TOLERANCE)  # QR_alg содержит trange

        # Сортировка собственных значений по убыванию
        print("Сортировка собственных значений.")
        sorted_indices = np.argsort(eigenvalues_A)[::-1]
        sorted_eigenvalues_A = eigenvalues_A[sorted_indices]
        # Гарантия неотрицательности (так как A = F*ᵀF*)
        sorted_eigenvalues_A = np.maximum(0.0, sorted_eigenvalues_A.real)
        pbar.update(1)
        print("Этап 3 завершен.")

        # Этап 4: Нахождение собственных векторов A с ортогонализацией
        print(f"Этап 4: {steps[3]}")
        eigenvectors_A = compute_orthonormal_basis(A, sorted_eigenvalues_A)  # Содержит trange
        pbar.update(1)
        print("Этап 4 завершен.")

        # Этап 5: Сингулярные значения = sqrt(собственных значений)
        print(f"Этап 5: {steps[4]}")
        singular_values = np.sqrt(sorted_eigenvalues_A)
        pbar.update(1)
        print("Этап 5 завершен.")

        # Этап 6: Левые сингулярные векторы U = F_star × V × Σ⁻¹
        print(f"Этап 6: {steps[5]}")
        V = eigenvectors_A  # Матрица V в SVD совпадает с собственными векторами A

        # Создание обратной диагональной матрицы сингулярных значений
        Sigma_diag = np.sqrt(sorted_eigenvalues_A)
        # Обработка деления на ноль
        if np.any(np.abs(Sigma_diag) < FLOAT_TOLERANCE):
            print("Обнаружены сингулярные значения, близкие к нулю. Корректировка обратной матрицы.")
            Sigma_diag_inv = np.zeros_like(Sigma_diag)
            non_zero = np.abs(Sigma_diag) >= FLOAT_TOLERANCE
            Sigma_diag_inv[non_zero] = 1.0 / Sigma_diag_inv[non_zero]
        else:
            Sigma_diag_inv = 1.0 / Sigma_diag

        Sigma_inv = np.diag(Sigma_diag_inv)

        # Вычисление U
        F_star_V = F_star_np @ V
        U = F_star_V @ Sigma_inv
        pbar.update(1)
        print("Этап 6 завершен.")

        # Этап 7: Транспонирование V для получения VT
        print(f"Этап 7: {steps[6]}")
        VT = V.T
        pbar.update(1)
        print("Этап 7 завершен.")

    print("Вычисление SVD завершено.")
    return U, singular_values, VT

def low_rank_approximation(U, singular_values, VT, r):
    """
    Построение малоранговой аппроксимации матрицы через усечение сингулярного разложения (SVD).

    Теоретическое описание:
    Малоранговая аппроксимация через SVD основана на идее сохранения наиболее информативных компонент матрицы. 
    Для матрицы F* ранга r её можно представить как F* = U_r Σ_r V_r^T, где U_r и V_r - усеченные матрицы 
    левых и правых сингулярных векторов, Σ_r - диагональная матрица усеченных сингулярных значений. 
    Этот метод минимизирует ошибку восстановления матрицы в евклидовой норме [[1]].

    Практическая реализация:
    Функция усекает матрицы U, Σ и VT до заданного ранга r, а затем перемножает их для получения приближенной матрицы. 
    Используется оператор матричного умножения @ из NumPy для эффективных вычислений.

    Parameters
    ----------
    U : np.ndarray
        Матрица левых сингулярных векторов размерности (m, m), полученная через SVD.
    singular_values : np.ndarray
        Одномерный массив сингулярных значений, упорядоченных по убыванию.
    VT : np.ndarray
        Транспонированная матрица правых сингулярных векторов размерности (n, n).
    r : int
        Ранг аппроксимации, должен быть в диапазоне (0, min(m, n)].

    Returns
    -------
    F_star_r : np.ndarray
        Матрица малоранговой аппроксимации размерности (m, n).
    Ur : np.ndarray
        Усеченная матрица U до размерности (m, r).
    Sigma_r : np.ndarray
        Диагональная матрица сингулярных значений размерности (r, r).
    VTr : np.ndarray
        Усеченная матрица VT до размерности (r, n).

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import svd
    >>> A = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float64)
    >>> U, s, VT = svd(A)
    >>> F_star_r, Ur, Sigma_r, VTr = low_rank_approximation(U, s, VT, r=1)
    >>> print("F_star_r:", F_star_r)

    Notes
    -----
    1. Сингулярные значения должны быть предварительно отсортированы по убыванию для корректной аппроксимации.
    2. Если r превышает количество ненулевых сингулярных значений, аппроксимация не улучшит точность.
    3. Численная устойчивость зависит от качества исходного SVD и структуры сингулярных значений.

    References
    ----------
    .. [1] "The Singular Value Decomposition (SVD) and Low-Rank Matrix Approximation" - (https://example.com/svd-lowrank)
    .. [2] "Generalized Low Rank Approximations of Matrices" - (https://example.com/generalized-lowrank)
    .. [4] "Lecture 4: Matrix rank, low-rank approximation, SVD" - (https://example.com/matrix-rank)
    .. [5] "Algorithms for `p Low-Rank Approximation" - (https://example.com/lowrank-algorithms)
    .. [7] "Demystifying Neural Networks: Low-Rank Approximation" - (https://example.com/neural-lowrank)
    """
    print(f"Построение малоранговой аппроксимации для ранга r = {r}.")

    # Проверка корректности ранга
    if r <= 0 or r > len(singular_values):
        print(f"Некорректный ранг аппроксимации r = {r}. Должен быть в диапазоне (0, {len(singular_values)}].")
        raise ValueError(f"Некорректный ранг аппроксимации r = {r}.")

    # Выбор первых r столбцов матрицы U
    Ur = U[:, :r]
    print(f"Выбраны первые {r} столбцов матрицы U.")

    # Выбор первых r сингулярных значений
    sr = singular_values[:r]
    print(f"Выбраны первые {r} сингулярных значений.")

    # Выбор первых r строк матрицы VT
    VTr = VT[:r, :]
    print(f"Выбраны первые {r} строк матрицы VT.")

    # Создание диагональной матрицы из усеченных сингулярных значений
    Sigma_r = np.diag(sr)  # Используем np.diag

    # Вычисление малоранговой аппроксимации: F_star_r = Ur @ Sigma_r @ VTr
    # Используем оператор @ для умножения матриц
    print("Выполнение умножения Ur @ Sigma_r.")
    Ur_Sigma_r = Ur @ Sigma_r
    print("Выполнение умножения (Ur @ Sigma_r) @ VTr.")
    F_star_r = Ur_Sigma_r @ VTr

    print(f"Построение малоранговой аппроксимации для ранга r = {r} завершено.")
    return F_star_r, Ur, Sigma_r, VTr

SVDF = [SVD]