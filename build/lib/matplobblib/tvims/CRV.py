from .rrstr import *
#######################################################################################################################
# Непрерывные случайные величины
#######################################################################################################################
def CRV_1(a,b,betas,powers,all_power,q_l=0.9):
    """Абсолютно непрерывная случайная величина  X  может принимать значения только в отрезке [a, b].<br>
    На этом отрезке плотность распределения случайной величины  X  имеет вид:<br> 
    f(x) = C * (1 + sum(betas_i * x ^ powers_i) )^all_power,<br>
    где С - положительная константа.<br>
    Найти:
    - константу C 
    - математическое ожидание E(X)
    - стандартное отклонение σX
    - квантиль уровня k распределения X

    Args:
        a (numerical): Начало отрезка
        b (numerical): Конец отрезка
        betas (array-like): Список коэффициентов при каждом x
        powers (array-like): Список степеней при каждом x
        all_power (numerical): Степень всего выражения
        q_l (numerical, optional): Уровень квантиля. Стандартно равен 0.9

    Returns:
        result (tuple): Ответы на задание по очереди, одновременно с выведением через print()
        
        ### 1 f"C = {C}")
        ### 2 f"E = {f_C.mean()}"
        ### 3 f"sigma = {f_C.std()}"
        ### 4 f"q = {f_C.ppf(q_l)}"
    """
    
    import scipy.stats
    import scipy.integrate
    import sympy
    import numpy as np

    
    assert len(betas)==len(powers), 'Степеней должно быть столько же, сколько коэффициентов Бета'

    # F = f(x) без C    
    F = lambda x: (1+ np.sum([betas[i]*x**powers[i] for i in range(len(betas))]))**all_power

    C = 1 / scipy.integrate.quad(F, a, b)[0]
    def f(x):
        return C * F(x)
    class dist_f_C(scipy.stats.rv_continuous):
    #функция вероятности
        def _pdf(self,x):
            return f(x) if (a<= x <=b) else 0
        #функция значений
        def _expect(self,x):
            return x
    #зададим распределение
    f_C = dist_f_C(a = a, b = b)
    
    #1
    print(f"C = {rrstr(C,5)}")
    #2
    print(f"E = {rrstr(f_C.mean(),3)}")
    #3
    print(f"sigma = {rrstr(f_C.std(),3)}")
    #4
    print(f"q = {rrstr(f_C.ppf(q_l),3)}")
    
    return (C,f_C.mean(),f_C.std(),f_C.ppf(q_l))
#######################################################################################################################
def CRV_2(a,b,betas,powers,all_power,q_l=0.9):
    """Случайная величина X равномерно распределена на отрезке [a,b].<br>
    Случайная величина Y выражается через X следующим образом:<br>
    Y = C * (1 + sum(betas_i * x ^ powers_i) )^all_power<br>
    Найдите:
    - математическое ожидание  E(Y)
    - стандартное отклонение σY
    - асимметрию As(Y)
    - квантиль уровня q_l распределения Y

    Args:
        a (numerical): Начало отрезка
        b (numerical): Конец отрезка
        betas (array-like): Список коэффициентов при каждом x
        powers (array-like): Список степеней при каждом x
        all_power (numerical): Степень всего выражения
        q_l (numerical, optional): Уровень квантиля. Стандартно равен 0.9

    Returns:
        result (tuple): Ответы на задание по очереди, одновременно с выведением через print()
            ### 1 f"EY = {EY}"
            ### 2 "Qy = {Qy}"
            ### 3 f"AsY = {AsY}"
            ### 4 f"q = {q}"
    """
    
    import scipy.stats
    import scipy.integrate
    import sympy
    import numpy as np
    import math
    
    assert len(betas)==len(powers), 'Степеней должно быть столько же, сколько коэффициентов Бета'
    
    F = lambda x: (1+ np.sum([betas[i]*x**powers[i] for i in range(len(betas))]))**all_power
    
    ab = [a, b]
    p = 1/(ab[1]-ab[0])
    EY = p * scipy.integrate.quad(F, a, b)[0]
    
    f = lambda x: (F(x))**2
    VarY = p * scipy.integrate.quad(f, a, b)[0] - EY**2
    Qy = math.sqrt(VarY)
    
    f = lambda x: p * (F(x) - EY)**3
    AsY = scipy.integrate.quad(f, a, b)[0]/Qy**3
    
    q = F(ab[0] + (ab[1] - ab[0])*q_l)
    
    #1
    print(f"EY = {rrstr(EY,1)}")
    #2
    print(f"Qy = {rrstr(Qy,2)}")
    #3
    print(f"AsY = {rrstr(AsY,4)}")
    #4
    print(f"q = {rrstr(q,3)}")
    
    return (EY,Qy,AsY,q)
#######################################################################################################################
CRV = [CRV_1,CRV_2]