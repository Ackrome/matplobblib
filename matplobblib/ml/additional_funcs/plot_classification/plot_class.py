import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.stats import gaussian_kde

def plot_classification_2d(
    X, y, model,
    feature_indices=(0, 1),
    feature_names=None,
    class_names=None,
    cmap='viridis',
    scatter_kwargs=None,
    legend_kwargs=None
):
    """
    Визуализирует результаты 2D классификации с границами принятия решений и распределениями признаков.

    Args:
        X (array-like): Матрица признаков.
        y (array-like): Вектор меток классов.
        model: Обученная модель классификации, имеющая метод `predict_proba` или `decision_function`.
        feature_indices (tuple, optional): Индексы двух признаков для визуализации.
            Defaults to (0, 1).
        feature_names (list, optional): Названия признаков для подписей осей.
            Defaults to None.
        class_names (list, optional): Названия классов для легенды. Defaults to None.
        cmap (str, optional): Цветовая карта для областей решений. Defaults to 'viridis'.
        scatter_kwargs (dict, optional): Дополнительные аргументы для `plt.scatter`.
            Defaults to None.
        legend_kwargs (dict, optional): Дополнительные аргументы для `plt.legend`.
            Defaults to None.
    """
    # Проверка корректности feature_names
    if feature_names is not None:
        if len(feature_names) != 2:
            raise ValueError("feature_names должен содержать ровно 2 элемента")
    
    # Преобразование данных
    X = np.array(X)
    y = np.array(y).ravel()
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if X.shape[1] < 2:
        raise ValueError("Требуется как минимум 2 признака")

    # Проверка индексов признаков
    idx1, idx2 = feature_indices
    if idx1 >= X.shape[1] or idx2 >= X.shape[1]:
        raise ValueError("Неверные индексы признаков")

    # Подготовка данных
    X_subset = X[:, [idx1, idx2]]
    classes = np.unique(y)
    n_classes = len(classes)
    
    # Генерация сетки
    x_min, x_max = X_subset[:, 0].min() - 0.5, X_subset[:, 0].max() + 0.5
    y_min, y_max = X_subset[:, 1].min() - 0.5, X_subset[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    
    # Предсказание модели
    try:
        Z = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])
        if Z.shape[1] == 2:
            Z = Z[:, 1]  # Для бинарной классификации
        else:
            Z = np.argmax(Z, axis=1)  # Для многоклассовой
    except AttributeError:
        Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
        if n_classes == 2:
            Z = (Z > 0).astype(int)
        else:
            Z = np.argmax(Z, axis=1)
    Z = Z.reshape(xx.shape)

    # Настройки визуализации
    scatter_params = {'alpha': 0.8, 's': 40} | (scatter_kwargs or {})
    legend_params = {'frameon': False, 'loc': 'best'} | (legend_kwargs or {})
    
    # Создание графика
    fig = plt.figure(figsize=(10, 8), constrained_layout=True)
    gs = gridspec.GridSpec(2, 2, 
                          width_ratios=[4, 1],
                          height_ratios=[1, 4],
                          figure=fig)

    # Основной график
    ax_main = fig.add_subplot(gs[1, 0])
    if len(classes) > 1:
        if Z.ndim == 2:
            contour = ax_main.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)
        else:
            contour = ax_main.contour(xx, yy, Z, alpha=0.6, cmap=cmap)
    else:
        contour = ax_main.contourf(xx, yy, Z, alpha=0.3, cmap=cmap)

    # Точки классов
    for cls in classes:
        mask = y == cls
        label = class_names[cls] if class_names else f'Class {cls}'
        ax_main.scatter(X_subset[mask, 0], X_subset[mask, 1], 
                       label=label, **scatter_params)
        
    # Исправленная установка меток осей
    ax_main.set_xlabel(
        feature_names[0] if feature_names else f'Feature {idx1}'
    )
    ax_main.set_ylabel(
        feature_names[1] if feature_names else f'Feature {idx2}'
    )
    ax_main.legend(**legend_params)

    # Верхний график плотности
    ax_histx = fig.add_subplot(gs[0, 0])
    ax_histx.grid(False)
    for cls in classes:
        subset = X_subset[y == cls, 0]
        kde = gaussian_kde(subset)
        x = np.linspace(x_min, x_max, 100)
        ax_histx.plot(x, kde(x), label=f'Class {cls}')
        ax_histx.fill_between(x, kde(x), alpha=0.3)
    ax_histx.set_axis_off()

    # Правый график плотности
    ax_histy = fig.add_subplot(gs[1, 1])
    ax_histy.grid(False)
    for cls in classes:
        subset = X_subset[y == cls, 1]
        kde = gaussian_kde(subset)
        y_vals = np.linspace(y_min, y_max, 100)
        ax_histy.plot(kde(y_vals), y_vals, label=f'Class {cls}')
        ax_histy.fill_betweenx(y_vals, kde(y_vals), alpha=0.3)
    ax_histy.set_axis_off()

    plt.suptitle('Classification Visualization', y=0.92, fontsize=14)
    plt.show()

PLOT_CLASSIFICATION = [plot_classification_2d]