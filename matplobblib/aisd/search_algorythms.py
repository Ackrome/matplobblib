#######################################################################################################################
# Алгоритмы поиска и сортировки
#######################################################################################################################
def AISD_SA_1(arr):
    """
    Реализация быстрой сортировки (Quicksort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = []
        right = []
        for i in range(1, len(arr)):
            if arr[i] < pivot:
                left.append(arr[i])
            else:
                right.append(arr[i])
        return AISD_SA_1(left) + [pivot] + AISD_SA_1(right)
#######################################################################################################################
def AISD_SA_2(arr):
    """
    Реализация сортировки выбором (Selection Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
#######################################################################################################################
def AISD_SA_3(arr):
    """
    Реализация сортировки вставками (Insertion Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
#######################################################################################################################
def AISD_SA_4(arr):
    """
    Реализация сортировки пузырьком (Bubble Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j+1], arr[j]
    return arr
#######################################################################################################################
def AISD_SA_5(arr, x):
    """
    Реализация бинарного поиска (Binary Search).

    Args:
        arr (list): Отсортированный список для поиска.
        x: Элемент для поиска.

    Returns:
        int: Индекс найденного элемента или -1, если элемент не найден.
    """
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1
#######################################################################################################################
def AISD_SA_6(arr):
    """
    Реализация шейкерной сортировки (Cocktail Shaker Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    n = len(arr)
    start = 0
    end = n - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1
    return arr
#######################################################################################################################
def AISD_SA_7(arr):
    """
    Реализация сортировки расческой (Comb Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    n = len(arr)
    gap = n
    shrink = 1.3
    swapped = True
    while gap > 1 or swapped:
        gap = int(gap/shrink)
        if gap < 1:
            gap = 1
        i = 0
        swapped = False
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
            i += 1
    return arr
#######################################################################################################################
def _AISD_SA_8_merge(left_half, right_half):
    """
    Вспомогательная функция для слияния двух отсортированных списков.

    Args:
        left_half (list): Первая отсортированная половина.
        right_half (list): Вторая отсортированная половина.

    Returns:
        list: Объединенный отсортированный список.
    """
    result = []
    i = 0
    j = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            result.append(left_half[i])
            i += 1
        else:
            result.append(right_half[j])
            j += 1

    result.extend(left_half[i:])
    result.extend(right_half[j:])

    return result

def AISD_SA_8(arr):
    """
    Реализация сортировки слиянием (Merge Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = AISD_SA_8(left_half)
    right_half = AISD_SA_8(right_half)

    return _AISD_SA_8_merge(left_half, right_half)
#######################################################################################################################
def AISD_SA_9(arr):
    """
    Реализация сортировки Шелла (Shell Sort).

    Args:
        arr (list): Список для сортировки.

    Returns:
        list: Отсортированный список.
    """
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
#######################################################################################################################
AISD_SA = [
    AISD_SA_1,
    AISD_SA_2,
    AISD_SA_3,
    AISD_SA_4,
    AISD_SA_5,
    AISD_SA_6,
    AISD_SA_7,
    AISD_SA_8,
    AISD_SA_9,
]
