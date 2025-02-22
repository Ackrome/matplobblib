from ...forall import *
#######################################################################################################################
def describe_text(data:str,splitter:str,g:float = 0.9, draw_boxes=False, q_l=63):
    """Функция для нахождения статистической информации по выборке.
    <br>В информации о выборке будут следующие значения:
    
        - Объем выборки до удаления пропущенных данных
        - Количество пропущенных данных (NA)
        - Объем выборки после удаления пропущенных данных
        - Минимальное значение в вариационном ряду
        - Максимальное значение в вариационном ряду
        - Размах выборки
        - Значение первой квартили (Q1)
        - Значение медианы (Q2)
        - Значение третьей квартили (Q3)
        - Квартильный размах
        - Среднее выборочное значение
        - Стандартное отклонение (S)
        - Исправленная дисперсия 
        - Эксцесс
        - Коэффициент асимметрии
        - Ошибка выборки
        - Значение (q_l/100)%-квантили
        - Мода
        - Как часто встречается "мода"
        - Верхняя граница нормы (Xst_max)
        - Нижняя граница нормы (Xst_min)
        - Количество выбросов ниже нижней нормы
        - Количество выбросов выше верхней нормы
        - Левая граница {g}-доверительного интервала для E(X)
        - Правая граница {g}-доверительного интервала для E(X)
        - Левая граница {g}-доверительного интервала для Var(X)
        - Правая граница {g}-доверительного интервала для Var(X)
    

    Args:
        data (str): Текст выборки одной строкой без переносов
        splitter (str): Разделитель между каждым значением выборки
        g (float, optional): Коэффициент доверия - Гамма для нахождения интервалов E(X) и Var(X). Стандартно равен 0.9.
        draw_boxes (bool, optional): Рисовать график или нет? По умолчанию - НЕТ
        q_l (float, optional): Странная квантиль в процентах. По умолчанию - 63
    
    Returns:
        res_df (pandas.DataFrame): Результирующая таблица статистической информации по выборке
        
        Если draw_boxes == True, то до вывода pd.DataFrame будут выведены два графика "Ящик с усами" - один до очистки, другой после
    """
    import pandas as pd
    import numpy as np
    import scipy.stats
    import matplotlib.pyplot as plt
    
    index = pd.Index(f'''Объем выборки до удаления пропущенных данных
Количество пропущенных данных (NA)
Объем выборки после удаления пропущенных данных
Минимальное значение в вариационном ряду
Максимальное значение в вариационном ряду
Размах выборки
Значение первой квартили (Q1)
Значение медианы (Q2)
Значение третьей квартили (Q3)
Квартильный размах
Среднее выборочное значение
Стандартное отклонение (S) корень из дисп.в (исправленной)
Исправленная дисперсия 
Эксцесс
Коэффициент асимметрии
Ошибка выборки
Значение {(q_l/100)}%-квантили
Мода
Как часто встречается "мода"
Верхняя граница нормы (Xst_max)
Нижняя граница нормы (Xst_min)
Количество выбросов ниже нижней нормы
Количество выбросов выше верхней нормы
Левая граница {g}-доверительного интервала для E(X)
Правая граница {g}-доверительного интервала для E(X)
Левая граница {g}-доверительного интервала для Var(X)
Правая граница {g}-доверительного интервала для Var(X)
'''.split('\n'))
    
    data_list=[]
    df=pd.DataFrame([float(i) if i!='NA' and i!='-NA' else np.nan for i in data.split(splitter)])
    
    length_before=df.size
    data_list.append(length_before)
    
    df=df.dropna()
    length_after=df.size
    data_list.extend([abs(length_after-length_before),length_after])
    
    minn=df.describe().loc['min'].values[0]
    maxx=df.describe().loc['max'].values[0]
    data_list.extend([minn,maxx,maxx-minn])
    
    Q1=df.describe().loc['25%'].values[0]
    Q2=df.describe().loc['50%'].values[0]
    Q3=df.describe().loc['75%'].values[0]
    
    mean = df.describe().loc['mean'].values[0]
    
    data_list.extend([Q1,Q2,Q3,Q3-Q1,mean,df.std(ddof=1,axis=0)[0],df.var(ddof=1)[0],df.kurt()[0],df.skew()[0]])
    
    data_list.append(data_list[11]/data_list[2]**0.5)
    data_list.extend(df.quantile((q_l/100)))
    
    if df.mode().count()[0] == df.count().iloc[0]:
        data_list.append(np.nan)
        data_list.append(0)
    else:
        data_list.append(df.mode().iloc[0,0])
        data_list.append(df.value_counts()[df.mode().iloc[0,0]])
        
    data_list.extend([data_list[8]+1.5*data_list[9],data_list[6]-1.5*data_list[9]])
    data_list.extend([len(df[df.iloc[:,0]<data_list[20]]),len(df[df.iloc[:,0]>data_list[19]])])
    
    z = scipy.stats.t.ppf((g+1)/2,length_after-1)
    sigma = df.std(ddof=1,axis=0)[0]
    delta = z * sigma/np.sqrt(length_after)

    data_list.extend([(mean-delta),(mean+delta)])

    z = scipy.stats.t.ppf((g+1)/2,length_after-1)
    sigma = df.std(ddof=1,axis=0)[0]
    var = sigma**2
    delta_R = length_after*var/scipy.stats.chi2.ppf((1-g)/2,length_after)
    delta_L = length_after*var/scipy.stats.chi2.ppf((1+g)/2,length_after)

    data_list.extend([delta_L,delta_R])

    if draw_boxes:
        df.boxplot()
        plt.xlabel('Ящик с усами до очистки')
        plt.show()

        clean_df=df[(df.iloc[:,0]>data_list[20]) & (df.iloc[:,0]<data_list[19])]
        clean_df.boxplot()
        plt.xlabel('Ящик с усами после очистки (Без NA и выбросов)')
        plt.show()
    
    res_df = pd.DataFrame(data_list,index[:len(data_list)], dtype=str)
    
    return res_df
#######################################################################################################################
def describe_pairs(dic, alpha1,alpha2, alternative1,alternative2,swap_columns = False):
    """
    Анализ пар значений и статистическая проверка гипотез.

    Функция принимает строку с парами числовых значений, уровень значимости 
    и тип альтернативной гипотезы. Выполняется проверка гипотез о равенстве 
    средних и дисперсий двух выборок, а также вычисляется коэффициент корреляции Пирсона.

    Параметры:
        dic (str): Строка, содержащая пары чисел в формате "{(x1, y1); (x2, y2); ...}".
                   Пропуски значений указываются как 'NA'.
        alpha1 (float): Уровень значимости для проверки гипотезы 1.
        alpha2 (float): Уровень значимости для проверки гипотезы 2.
        alternative1 (str): Тип альтернативной гипотезы для сравнения средних значений.
                           Возможные значения: 'two-sided', 'less', 'greater'.
        alternative2 (str): Тип альтернативной гипотезы для сравнения дисперсий.
                           Возможные значения: 'two-sided', 'greater'.
        swap_columns (bool): Если True, меняет местами столбцы X и Y в результирующей таблице.

    Возвращает:
        pd.DataFrame: Таблица с результатами анализа:
            - 1. Введите выборочный коэффициент корреляции Пирсона между X и Y
            - 2.1 Введите значение P-value в проверке гипотезы о равенстве средних значений показателей фирм при альтернативной гипотезе о том, что среднее значение показателя больше у первой фирмы (без каких-либо предположений о равенстве дисперсий) 
            - 2.2 На уровне значимости {`alpha1`} можно ли утверждать, что среднее значение показателя больше у первой фирмы? Введите 1 - если да, и 0 - если нет: Минимальное значение в вариационном ряду
            - 3.1 Введите значение P-value в проверке гипотезы о равенстве дисперсий показателей двух фирм при альтернативной гипотезе об их неравенстве
            - 3.2 На уровне значимости `alpha2` можно ли утверждать, что дисперсии показателей фирм различны? Введите 1 - если да, и 0 - если нет

    Пример:
        >>> dic = '{(-187.6, -170.9); (-190.5, NA); (NA, -214.4)}'
        >>> alpha = 0.01
        >>> alternative = 'two-sided'
        >>> result = describe_pairs(dic, alpha, alternative)
        >>> print(result)
    """
    import re
    import pandas as pd
    from scipy.stats import f, ttest_ind, bartlett
    
    # Извлечение пар значений
    pairs = re.findall(r'\(([^,]+), ([^)]+)\)', dic)

    # Преобразование в DataFrame
    df = pd.DataFrame(pairs, columns=["Column 1", "Column 2"])

    # Вывод таблицы
    some_list = []
    for i in range(df.shape[0]):
        if not(df.iloc[i,0] == 'NA' or df.iloc[i,1] == 'NA'):
            some_list.append([df.iloc[i,0],df.iloc[i,1]])
    df = pd.DataFrame(np.array(some_list).astype(float), columns=["X", "Y"])
    
    # Перемена местами столбцов, если swap_columns=True
    if swap_columns:
        df = df.rename(columns={"X": "Y", "Y": "X"})


    index = pd.Index(f'''1. Введите выборочный коэффициент корреляции Пирсона между X и Y: 
    2.1 Введите значение P-value в проверке гипотезы о равенстве средних значений показателей фирм при альтернативной гипотезе о том, что среднее значение показателя больше у первой фирмы (без каких-либо предположений о равенстве дисперсий): 
    2.2 На уровне значимости {alpha1} можно ли утверждать, что среднее значение показателя больше у первой фирмы? Введите 1 - если да, и 0 - если нет: Минимальное значение в вариационном ряду
    3.1 Введите значение P-value в проверке гипотезы о равенстве дисперсий показателей двух фирм при альтернативной гипотезе {alternative2}: 
    3.2 На уровне значимости {alpha2} можно ли утверждать, что дисперсии показателей фирм различны? Введите 1 - если да, и 0 - если нет: 
    '''.split('\n'))

    # 2.1 Проверка гипотезы о равенстве средних значений (альтернатива: среднее больше у X)
    t_stat, p_value_means = ttest_ind(df['X'], df['Y'], alternative=alternative1, equal_var=False)

    # 2.2 Проверка гипотезы на уровне значимости alpha1
    mean_test_result = int(p_value_means < alpha1)

    if alternative2=='greater':
        s1 = df['X'].var(ddof=1)
        s2 = df['Y'].var(ddof=1)
        df1= df['X'].size-1
        df2= df['Y'].size-1
        p_value_variances = f.sf(s1/s2,df1,df2)
        
    elif alternative2=='less':
        df = df.rename(columns={"X": "Y", "Y": "X"})
        s1 = df['X'].var(ddof=1)
        s2 = df['Y'].var(ddof=1)
        df1= df['X'].size-1
        df2= df['Y'].size-1
        p_value_variances = f.sf(s1/s2,df1,df2)
        
    else:
        # 3.1 Проверка гипотезы о равенстве дисперсий
        f_stat, p_value_variances = bartlett(df['X'], df['Y'])

    # 3.2 Проверка гипотезы на уровне значимости alpha2
    variance_test_result = int(p_value_variances < alpha2)

    data_list=[df.corr('pearson').iloc[0,1],p_value_means,mean_test_result,p_value_variances,variance_test_result]
    res_df = pd.DataFrame(data_list,index[:len(data_list)], dtype=str)
        
    return res_df
#######################################################################################################################
def describe_symbols(text,alpha1,alpha2):
    """
    Анализ категориальных данных и проверка статистических гипотез.

    Функция принимает строку с категоризированными данными, уровень значимости
    для построения доверительных интервалов и проверки гипотезы о равномерном
    распределении ответов. Выполняется расчет частот ответов, доверительных
    интервалов для долей, а также проверка гипотезы о равномерности распределения.

    Параметры:
        text (str): Строка с данными в формате 'категория1; категория2; ...', 
                    пропуски указываются как 'NA'.
        alpha1 (float): Уровень значимости для доверительных интервалов долей.
        alpha2 (float): Уровень значимости для проверки гипотезы о равномерности.

    Возвращает:
        pd.DataFrame: Таблица с результатами анализа:
            - Количество очищенных значений.
            - Количество уникальных категорий.
            - Частота каждой категории.
            - Доля каждой категории.
            - Границы доверительных интервалов для долей.
            - Степени свободы, критическое и наблюдаемое значения хи-квадрат,
              а также результат проверки гипотезы о равномерности распределения
              (1 - гипотеза отвергается, 0 - принимается).

    Пример:
        >>> text = 'A; B; NA; A; C; A; B; NA; C; C; A'
        >>> alpha1 = 0.05
        >>> alpha2 = 0.01
        >>> result = describe_symbols(text, alpha1, alpha2)
        >>> print(result)
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import chi2, norm
    
    indextext = '''1. Введите объем очищенной от "NA" выборки:  
2. Введите количество различных вариантов ответов респондентов, встречающиеся в очищенной выборке:  
3  Введите количество респондентов, которые дали ответ:'''
    
    no_na = np.array(text.replace('; NA','').split('; '))
    lens = []

    data_list = [no_na.size, np.unique(no_na).size]
    data_list.append(' ')
    

    for i in np.unique(no_na):
        lens.append(no_na[no_na==i].size)
        data_list.append(no_na[no_na==i].size)
        indextext+=f'\n{i}'

    indextext+='\n4. Введите долю респондентов, которые дали ответ:'
    data_list.append(' ')
    for i in np.unique(no_na):
        data_list.append(no_na[no_na==i].size/no_na.size)
        indextext+=f'\n{i}'

    
    

    indextext+=f'\n5 - 6. Введите границы {1 - alpha1}-доверительного интервала для истинной доли ответов  '
    data_list.append(' ')
    for i in np.unique(no_na):
        p_hat = no_na[no_na==i].size/no_na.size

        # Z-значение для 1 - alpha-го доверительного интервала
        z_critical = norm.ppf(1 -  alpha1/ 2)
        margin_of_error = z_critical * np.sqrt(p_hat * (1 - p_hat) / no_na.size)

        ci_lower = p_hat - margin_of_error
        ci_upper = p_hat + margin_of_error
        
        
        data_list.append([ci_lower,ci_upper])
        indextext+=f'\n{i}'
           

    degrees_of_freedom = np.unique(no_na).size - 1

    

    # Критическое значение Хи-квадрат
    chi_critical = chi2.ppf(1 - alpha2, degrees_of_freedom)

    

    # Частоты
    expected = np.full(len( np.unique(no_na)), no_na.size / len( np.unique(no_na)))  # Равновероятное распределение
    # Статистика Хи-квадрат
    chi_square_stat = ((lens - expected)**2 / expected).sum()


    indextext+='\n7. Введите количество степеней свободы :\n8. Введите критическое значение статистики хи-квадрат  :\n9. Введите наблюдаемое значение хи-квадрат  :\n10. Введите 1, если есть основания отвергнуть гипотезу о равновероятном распределении ответов, или введите 0, если таких оснований нет :'
    data_list.extend([degrees_of_freedom,chi_critical,chi_square_stat,int(chi_square_stat > chi_critical)])
    
    # 11. Гистограмма для исходной выборки
    plt.figure(figsize=(10, 6))
    plt.hist(no_na, bins=np.unique(no_na).size, edgecolor='black', alpha=0.7, )
    plt.xticks(range(np.unique(no_na).size), np.unique(no_na))
    plt.title("Гистограмма распределения ответов")
    plt.xlabel("Категория")
    plt.ylabel("Частота")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    index = pd.Index(indextext.split('\n'))
    
    res_df = pd.DataFrame(data_list,index[:len(data_list)], dtype=str)
            
    return res_df
#######################################################################################################################
DT = [describe_text,describe_pairs,describe_symbols]