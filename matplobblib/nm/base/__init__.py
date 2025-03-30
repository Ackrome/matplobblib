from ...forall import *
def perepolnenie():
    '''переполнение'''
    print(f'переполнение')
    print(np.iinfo(np.int32).max)
    print(np.int32(np.iinfo(np.int32).max) + 1)
    print(sys.float_info.max)
    print(sys.float_info.max + 5 - sys.float_info.max)
    print(sys.float_info.max + sys.float_info.max)
    print('''    print(f'переполнение')
    print(np.iinfo(np.int32).max)
    print(np.int32(np.iinfo(np.int32).max) + 1)
    print(sys.float_info.max)
    print(sys.float_info.max + 5 - sys.float_info.max)
    print(sys.float_info.max + sys.float_info.max)''')


def poterya_tochnosti():
    '''потеря точности'''
    print(f'потеря точности')
    print(1.000_000_001 - 1.000_000_000)
    print()
    print('''#потеря точности;
print(f'потеря точности')
print(1.000_000_001 - 1.000_000_000)
print()''')

def oshibka_okrugleniya():
    '''ошибки округления'''
    print(f'ошибки округления')
    print(0.1 + 0.2 == 0.3)
    print()
    print('''


#ошибки округления;
print(f'ошибки округления')
print(0.1 + 0.2 == 0.3)
print()''')
    

def nakoplenie_oshibok():
    '''накопление ошибок'''
    print(f'накопление ошибок')
    x = 0
    true_init = 100_000.0
    for _ in range(1_000_000):
      x+=0.1
    print(x)
    print(true_init-x)
    print()
    print('''
#накопление ошибок;
print(f'накопление ошибок')
x = 0
true_init = 100_000.0
for _ in range(1_000_000):
  x+=0.1
print(x)
print(true_init-x)
print()''')



def poterya_znachimosti():
    '''потеря значимости'''
    #потеря значимости
    print(f'потеря значимости')
    print(np.exp(1e-10) - 1)
    print()
    print('''#потеря значимости
print(f'потеря значимости')
print(np.exp(1e-10) - 1)
print()''')




def summirovanie_po_Kohanu():
    

    #суммирования по Кохану
    print(f'суммирования по Кохану')
    def kahan_sum(numbers):
        total = 0.0
        resid = 0.0
        for num in numbers:
            y = num - resid
            temp = total + y
            resid = (temp - total) - y
            total = temp
        return total
    mx = list(range(1,10**5))
    kahan_sum(mx)
    print('''#суммирования по Кохану
    print(f'суммирования по Кохану')
    def kahan_sum(numbers):
        total = 0.0
        resid = 0.0
        for num in numbers:
            y = num - resid
            temp = total + y
            resid = (temp - total) - y
            total = temp
        return total
    mx = list(range(1,10**5))
    kahan_sum(mx)''')


BASE = [perepolnenie,poterya_tochnosti,oshibka_okrugleniya,nakoplenie_oshibok,poterya_znachimosti,summirovanie_po_Kohanu]