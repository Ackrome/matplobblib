
```python
%time sum(range(2000))
```
text_plain_output:

1999000



```python
%timeit sum(range(2000))
```

```python
%%time

s =0
for i in range(200):
    s+=1
```

```python
%%timeit

s =0
for i in range(200):
    s+=1
```

```python
import numpy as np
```

```python
def slow_sum(n,m):
    for i in range(n):
        a =np.random.rand(m)
        print(a)
    s =0
    for j in range(m):
        s+=a[j]
        print(s)

slow_sum(100,12)
```

```python
%prun slow_sum(100,10000)
```

```python
pip install line-profiler
```

```python
%load_ext line_profiler
```

```python
%lprun -f slow_sum slow_sum(1000,10000)
```

```python
import sys
sys.float_info
```
text_plain_output:

sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsilon=2.220446049250313e-16, radix=2, rounds=1)


1 100000000010 1000000000000000000000000000000000000000000000000000 ieee754

1. определим экспоненту: 100000000010 (base2) = $1*2^(10) +1*2^1$ = 1026

2. определим мантиссу:

3. финальное значение числа: $x =(-1)^1 * 2^3 * (1 + 0.5)$ =-12

представим число 15.0 в ieee 754:

1. число положительное, s =0

2. наибольшая степень двойки меньше 15: 8 ($2^3$), e =3

3. с учетом bias 3+1023 =1026 в двоичной системе 100000000010 base2

4. мантисса 15/8 - 1 =0.875(base10) = $1*2^{-1} + 1*2^{-2} +  1*2^{-3}$ =0.111(base2)

Представление числа 15: 0 100000000010 111000000000000000000000000000000000000000000

экспонента задает размер шага (меньше экспонента меньше шаг между соседними)


```python
np.spacing(1e6)
```
text_plain_output:

1.1641532182693481e-10



```python
1e6 == 1e6+np.spacing(1e6)/3
```
text_plain_output:

True


Самое большое число 0 111111111111111
Самое маленькое 1 111111111111111


```python
largest = (2**(2046-1023)*(1+sum(0.5**np.arange(1,53))))
largest
```
text_plain_output:

1.7976931348623157e+308



```python
import sys
sys.float_info.max
```
text_plain_output:

1.7976931348623157e+308


0 00000000000001 00000000000000000000000000000000 Самое маленькое не нулевое положительное


```python
smallest = (2**(1-1023))*(1+0)
smallest
```
text_plain_output:

2.2250738585072014e-308



```python
sys.float_info.min
```
text_plain_output:

2.2250738585072014e-308



```python
sys.float_info.max == sys.float_info.max + 2 #кодируем все то же максимальное число
```
text_plain_output:

True



```python
sys.float_info.max + sys.float_info.max # максимальное плюс максимальное = бесконечность
# переполнение
```
text_plain_output:

inf



```python
4.9 - 4.845 == 0.055 #))))
```
text_plain_output:

False



```python
4.9 - 4.845
```
text_plain_output:

0.055000000000000604



```python
4.8 - 4.845
```
text_plain_output:

-0.04499999999999993



```python
0.1 + 0.2 + 0.3 ==0.6
```
text_plain_output:

False



```python
round(0.1 + 0.2 + 0.3, 5) == round(0.6, 5) # устранение влияния специфики представления
```
text_plain_output:

True



```python
1 + 1/3 - 1/3
```
text_plain_output:

1.0



```python
def add_and_sub(i):
    res = 1
    for _ in range(i):
        res +=1/3
    for _ in range(i):
        res -=1/3
    return res
```

```python
add_and_sub(100)
```
text_plain_output:

1.0000000000000002



```python
add_and_sub(1000000)
```
text_plain_output:

0.9999999999727986


## Алгоритм Кахана

Позволяет уменьшить ошибку округления


```python
s =0 # объект, который хранит результат суммирования
c =0 # погрешность на каждом шаге
for i in range(len(x)):
    y =x[i] -c
    t =s + y
    c =(t - s) -y
    s =t
```
**ERROR:**
<span style="color:red"> *NameError: name 'x' is not defined*</span>

```python
import numpy as np
```

```python
from numba import jit
import time
```

```python
n =10**6
np.random.seed(42)
x =np.random.uniform(-1,1,n).astype(np.float32)

true_sum = np.sum(x, dtype= np.float64)
approx_sum = np.sum(x, dtype= np.float32)

def naive_sum(x):
    s = np.float32(0.0)
    for i in range(len(x)):
        s+=x[i]
    return(s)

@jit(nopython=True)
def kahan_sum(x):
    s =np.float32(0.0)
    c =np.float32(0.0)
    for i in range(len(x)):
        y =x[i] -c
        t =s + y
        c =(t - s) -y
        s =t
    return(s)

start =time.time()
d_sum =naive_sum(x)
time_naive = time.time() - start


start =time.time()
k_sum =kahan_sum(x)
time_kahan = time.time() - start


start =time.time()
d_sum =np.sum(x)
time_numpy = time.time() - start

print('Ошибка в numpy sum {0:3.1e}'.format(approx_sum-true_sum))
print('Ошибка в kahan sum {0:3.1e}'.format(k_sum-true_sum))
print('Ошибка в naive sum {0:3.1e}'.format(d_sum-true_sum))

print('\nВремя выполнения:')
print(f'numpy sum:   {time_numpy: .6f} сек')
print(f'naive sum:   {time_naive: .6f} сек')
print(f'kahan sum:   {time_kahan: .6f} сек')
```

```python

```
