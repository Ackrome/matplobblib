from ...forall import *


def simple_iteration_system(G, x0, eps=1e-6, max_iter=1000):
    """
    G: функция, задающая итерационный процесс (x_next = G(x_current))
    x0: начальное приближение (вектор)
    eps: точность
    max_iter: максимальное число итераций
    """
    x = x0.copy()
    for _ in range(max_iter):
        x_next = G(x)
        if np.linalg.norm(x_next - x) < eps:
            return x_next
        x = x_next
    raise RuntimeError("Метод не сошёлся за указанное число итераций")

#метод простых итераций (СНУ)
def simple_iteration_system_no_np(G, x0, eps=1e-6, max_iter=1000):
    """
    Модифицированная версия без использования np.linalg.norm
    """
    x = x0.copy()
    for _ in range(max_iter):
        x_next = G(x)
        # Вычисление евклидовой нормы через сумму квадратов
        diff = x_next - x
        norm_sq = sum(diff[i]**2 for i in range(len(diff)))
        if norm_sq < eps**2:  # Сравнение квадратов для избежания sqrt
            return x_next
        x = x_next
    raise RuntimeError("Метод не сошёлся за указанное число итераций")


# метод Зейделя
def seidel_method(g_funcs, x0, tol=1e-6, max_iter=100):
    x = x0.copy()
    n = len(x)
    for _ in range(max_iter):
        x_prev = x.copy()
        for i in range(n):
            x[i] = g_funcs[i](x)
        # Проверка максимального изменения через базовый Python
        max_diff = max(abs(x[i] - x_prev[i]) for i in range(n))
        if max_diff < tol:
            return x
    raise RuntimeError("Метод не сошёлся")

# метод Ньютона
def newton_system(F, J, x0, tol=1e-6, max_iter=100):
    """
    Модифицированная версия с ручным решением СЛАУ
    """
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        F_val = F(x)
        # Проверка нормы невязки через сумму квадратов
        if sum(f**2 for f in F_val) < tol**2:
            return x

        J_val = J(x)
        a, b, c, d = J_val[0,0], J_val[0,1], J_val[1,0], J_val[1,1]
        det = a*d - b*c

        if abs(det) < 1e-12:
            raise ValueError("Вырожденная матрица Якоби")

        # Решение системы методом Крамера
        e, f = -F_val
        dx = (e*d - b*f) / det
        dy = (a*f - e*c) / det

        x += np.array([dx, dy])

    raise RuntimeError("Метод не сошёлся")

SISTEMS = [simple_iteration_system,simple_iteration_system_no_np,seidel_method,newton_system]