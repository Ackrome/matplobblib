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
DT = [describe_text]