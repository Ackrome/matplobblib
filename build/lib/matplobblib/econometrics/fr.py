#######################################################################################################################
# Работа с моделями
#######################################################################################################################
def make_model_outputs(endog, exog,untrust = 0.05, endog_name = 'Y', exog_name = 'X', func_endog = lambda y: y, func_exog = lambda x: x):
    """Выполняет задания с номера 2 в определенной работе.
    Вот эти задания:
    - **Исследование взаимосвязи данных показателей с помощью диаграммы рассеяния и коэффициента корреляции.** Построить график диаграммы рассеяния зависимой переменной с экзогенным фактором. Оценить коэффициент корреляции между объясняемой и объясняющей пе-ременными. Проанализировать тесноту и направление связи.
    - **Оценивание качества спецификации модели.** Выпишите полученное уравнение регрессии.  Дайте экономическую интерпретацию параметрам модели. Проверить статистическую значимость регрессии в целом. Проверить статистическую значимость оценок параметров. Оценить точность модели с помощью средней относительной ошибки аппроксимации. Сделайте выводы   качестве уравнения регрессии.
    - **Проверьте остатки на нормальное распределение одним из тестов (выбрать самостоятельно)**
    - **Проверка предпосылки теоремы Гаусса-Маркова о гомоскедастичности случайных возмущений.** Выполнить визуальный анализ гетероскедастичности с помощью графиков.  Провести поверку по одному из тестов - выбор теста зависит от выполнения п. 4. Обосновать применение предложенного вами теста. Сделать выводы. При необходимости предложить вариант корректировки гетероскедастичности.
    
    Args:
        endog (array-like): Эндогенная переменная (Y)
        exog (array-like): Экзогенная переменная (X)
        untrust (float, optional): Параметр недоверия(чаще alpha). Стандартно = 0.05.
        endog_name (str, optional): Имя эндогенной переменной (Y). Стандартно = 'Y'.
        exog_name (str, optional):  Имя экзогенной переменной (X). Стандартно = 'X'.
        func_endog (method_object, optional): Функция для изменения эндогенной переменной (Y). Стандартно = lambda y:y.
        func_exog (method_object, optional): Функция для изменения экзогенной переменной (X). Стандартно = lambda x:x.

    """
    import scipy.stats
    import sympy
    import numpy
    import seaborn
    import matplotlib.pyplot as plt
    from IPython.display import Math,Latex
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_goldfeldquandt
    
    def corr_type(r)->str:
        
        ans=''
        if r > 0:
            ans += 'ПРЯМАЯ '
        elif r < 0:
                ans += 'ОБРАТНАЯ '
                
        if abs(r) == 0:
                ans += 'НЕ НАБЛЮДАЕТСЯ '
        elif abs(r) < 0.3:
                ans += 'ОЧЕНЬ СЛАБАЯ '
        elif 0.3 <= abs(r) < 0.5:
                ans += 'СЛАБАЯ'
        elif 0.5 <= abs(r) < 0.7:
                ans += 'УМЕРЕННАЯ '
        elif 0.7 <= abs(r) < 1:
                ans += 'СИЛЬНАЯ '
        else:
                ans += 'ФУНКЦИОНАЛЬНАЯ '
        return ans

    
    def custom(endog, exog):        
        vectorized_func_endog = numpy.vectorize(func_endog)
        vectorized_func_exog = numpy.vectorize(func_exog)
        
        endog = vectorized_func_endog(endog)
        exog = vectorized_func_exog(exog)
        
        return endog,exog
        
    
    prev_exog = exog.copy()
    prev_endog = endog.copy()
    ##############################################################################################################################################################
    display(Math('№2'))
    
    plt.scatter(endog, exog)
    plt.xlabel(exog_name)
    plt.ylabel(endog_name)
    plt.show()
    
    with numpy.errstate(divide='ignore', invalid='ignore'):
        cor_matr = numpy.corrcoef(numpy.concatenate((endog,exog), axis = 1), rowvar=False)
        cor_matr[numpy.isnan(cor_matr)] = 0
    
    corr  = cor_matr[0,1] 
    display(Math(('Коэффициент корреляции между исходными объясняемой и объясняющей переменными равен r_{' + f'{endog_name},' + f'{exog_name}' + '} =' + f' {corr}. Вид связи - {corr_type(corr)}').replace(' ','~')))    
    ##############################################################################################################################################################
    display(Math('№3'))
    
    model_type = custom
    
    endog, exog = model_type(endog, exog)
    
    exog = sm.add_constant(exog)
    model = sm.OLS(endog,exog).fit()
    
    if model.pvalues[0]>untrust:
        print(f'Константа, при построении модели с ней, статистически незначима.({model.pvalues[0]}>{untrust})')
        model = sm.OLS(endog,prev_exog).fit()
    
    r2=model.rsquared
    params=model.params
    nobs=model.nobs
    df=model.df_model
    tvalues=model.tvalues
    pvalues=model.pvalues
    f_pvalue=model.f_pvalue
    fvalue=model.fvalue
    
    exog = model.model.exog                                  # X
    endog = model.model.endog.reshape((exog.shape[0],1))     # Y
    predict = model.predict(exog)
    
    display(model.summary())   
    
    t_crit = scipy.stats.t.ppf(1 - untrust/2, nobs - (df + 1))
    print(f'Коэффициент Детерминаци равен: {str(round(r2*100,3)).replace(".",",")}% .')
    print(f'\nКоэфициенты b при каждом члене равны соответственно: {params} .')
    
    coefs = []
    
    for i in range(len(params)):
        
        if pvalues[i]<untrust:
            print(f'\nКоэффициент {str(params[i]).replace(".",",")} стат. значим, т.к. значение t = {str(round(abs(tvalues[i]),4)).replace(".",",")} больше t_критического = {str(round(t_crit,4)).replace(".",",")} <=> pvalue={str(pvalues[i]).replace(".",",")} < {str(untrust).replace(".",",")}')
            coefs.append(params[i])
            
        else:
            print(f'\nКоэффициент {str(params[i]).replace(".",",")} стат. незначим, т.к. значение t = {str(round(abs(tvalues[i]),4)).replace(".",",")} меньше t_критического = {str(round(t_crit,4)).replace(".",",")} <=> pvalue={str(pvalues[i]).replace(".",",")} > {str(untrust).replace(".",",")}')
            coefs.append(0)
            
    if untrust>f_pvalue:
        print(f'\n\nРегрессия стат. значима, т.к. F-значение критерия фишера = {str(round(fvalue,4)).replace(".",",")} больше F_критического <=> fvalue={str(f_pvalue).replace(".",",")} < {str(untrust).replace(".",",")}')
    else:
        print(f'\n\nРегрессия стат. незначима, т.к. F-значение критерия фишера = {str(round(fvalue,4)).replace(".",",")} меньше F_критического <=> fvalue={str(f_pvalue).replace(".",",")} > {str(untrust).replace(".",",")}')
    
    
    try:
        if exog.shape[1]>=2:    
            x = [1]+[sympy.symbols(','.join(f'x_{i+1}' for i in range(len(params)-1)))]
            y = sum(numpy.multiply(x,coefs))
            
            display(Math('Уравнение~регрессии:~~~~y = '+ sympy.latex(y)))
            
        elif exog.shape[1]==1:
            x = [sympy.symbols(','.join(f'x_{i+1}' for i in range(len(params))))]
            y = sum(numpy.multiply(x,coefs))
            
            display(Math('Уравнение~регрессии:~~~~y = '+ sympy.latex(y)))
        
    except:
        print('Нет коэффициентов')
        pass

    
    display(Math(f'Средняя относительная ошибка апроксимации (MAPE) = {numpy.mean(abs(model.predict(exog) - endog)/endog)*100}\%'.replace(' ','~')))
    print('Это метрика, которая используется для оценки точности модели.\nОна показывает, насколько модель отклоняется от истинных значений в среднем в процентах.')
    coefs = numpy.array(coefs)
    tr_coefs_indexes = numpy.where(coefs != 0)

    
    concat_tr_array = numpy.concatenate((endog,exog[:,*tr_coefs_indexes]), axis = 1)
    
    with numpy.errstate(divide='ignore', invalid='ignore'):
        cor_matr = numpy.corrcoef(concat_tr_array, rowvar=False)
        cor_matr[numpy.isnan(cor_matr)] = 0 
    
    
    ticks = ['$y$']+[f'${i}$' for i in x]
    
    
    plt.scatter(endog,model.predict(exog))
    plt.plot([endog.min(),endog.max()],[endog.min(),endog.max()], c='r')
    plt.xlabel(endog_name)
    plt.ylabel(endog_name)
    plt.show()
    
    seaborn.heatmap(cor_matr, annot=True, xticklabels=ticks, yticklabels=ticks, cmap='coolwarm')
    plt.show()
    ##############################################################################################################################################################
    display(Math('№4'))
    resid = model.resid

    display(Math('Jarque-Bera'))
    jb_stat, jb_p_value = scipy.stats.jarque_bera(resid)
    print("Статистика:", jb_stat)
    print("p-значение:", jb_p_value)

    if jb_p_value < untrust:
        print("Данные не распределены нормально (отвергаем H0) \n")
    else:
        print("Данные распределены нормально (не отвергаем H0)\n")

    display(Math('Shapiro-Wilk'))
    stat, p_value = scipy.stats.shapiro(resid)

    print("Статистика:", stat)
    print("p-значение:", p_value)

    if p_value > untrust:
        print("Данные распределены нормально (не отвергаем H0)\n")
    else:
        print("Данные не распределены нормально (отвергаем H0) \n")



    def helwig_test(data):
        # Шаг 1: Сортируем данные и определяем размер выборки
        data_sorted = numpy.sort(data)
        n = len(data)

        # Шаг 2: Оценка среднего и стандартного отклонения
        mean, std = numpy.mean(data), numpy.std(data, ddof=1)

        # Шаг 3: Вычисляем эмпирическую функцию распределения (ЭФР)
        ecdf = numpy.arange(1, n + 1) / n

        # Шаг 4: Строим теоретическую нормальную функцию распределения (НФР)
        theoretical_cdf = scipy.stats.norm.cdf(data_sorted, mean, std)


        # Шаг 5: Вычисляем максимальное отклонение между ЭФР и НФР
        max_deviation = numpy.max(numpy.abs(ecdf - theoretical_cdf))

        # Вывод результата
        print("Максимальное отклонение (D):", max_deviation)
        return max_deviation


    display(Math('Helwig'))
    n = len(resid)
    
    critical_value = scipy.stats.kstwobign.ppf(1 - untrust) / numpy.sqrt(n)
    
    if helwig_test(resid) > critical_value:
        
        print(f"H0 отвергается на уровне значимости {untrust}.")
    else:
        
        print(f"Нет оснований отвергнуть H0 на уровне значимости {untrust}.")
    ##############################################################################################################################################################
    display(Math('№5'))
    
    display(Math('Goldfeld-Quandt'))
    
    k=0
    if model!='linear':
        print('Осуществим этот тест на преобразованных для модели данных')
        j_exog =  (exog[:,1] if exog.shape[1]>=2 else exog).reshape((-1,1))
        if het_goldfeldquandt(endog,j_exog)[1] < untrust:
            print(f'Согласно тесту Голдфельда-Куандта, данные гетероскедастичны: {het_goldfeldquandt(endog,j_exog)[1]} < {untrust}\n')
            k+=1
        else:
            print(f'Согласно тесту Голдфельда-Куандта, данные гомоскедастичны: {het_goldfeldquandt(endog,j_exog)[1]} > {untrust}')
        
        print('Это заметно и на графике:')
        
        plt.scatter(resid**2,j_exog)
        plt.xlabel(exog_name)
        plt.ylabel('$e^2$')
        plt.show()
        
    print('Осуществим этот тест на изначальных данных')
    if het_goldfeldquandt(prev_endog, prev_exog)[1] < untrust:
        print(f'Согласно тесту Голдфельда-Куандта, данные гетероскедастичны: {het_goldfeldquandt(prev_endog, prev_exog)[1]} < {untrust}\n')
        k+=1
    else:
        print(f'Согласно тесту Голдфельда-Куандта, данные гомоскедастичны: {het_goldfeldquandt(prev_endog, prev_exog)[1]} > {untrust}\n')
    print('Это заметно и на графике:')
        
    plt.scatter(resid**2, prev_exog)
    plt.xlabel(exog_name)
    plt.ylabel('$e^2$')
    plt.show()
    
    if k>=1:
        print(Math('Попробуем провести корректировку гетероскедастичности делением функции на x^{1/2}'.replace(' ','~')))
        
        prev_j_exog = j_exog.copy()
        j_exog = sm.add_constant(j_exog)
        j_exog = j_exog/prev_j_exog**0.5
        y_x05 = predict/prev_j_exog**0.5
        model = sm.OLS(y_x05,j_exog).fit()
        
        
        if any([model.pvalues[i]>untrust for i in range(len(model.pvalues))]) or model.f_pvalue>untrust:
            print(f'Данная модель оказалась статистически незначимой.Попробуем построить другую, делением функции на x ')
            j_exog = prev_j_exog.copy()
            j_exog = sm.add_constant(j_exog)
            j_exog = j_exog/prev_j_exog
            y_x1 = predict/prev_j_exog
            
            model = sm.OLS(y_x1,j_exog).fit()
            
            if any([model.pvalues[i]>untrust for i in range(len(model.pvalues))]) or model.f_pvalue>untrust:
                print('Попытки скорректировать гетероскедастичность не увенчались успехом')
    
    return model
#######################################################################################################################