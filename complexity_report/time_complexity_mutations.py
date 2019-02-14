import timeit
from data_structers.individual import Individual
import numpy as np
from data_structers.mutation_operators import change_random_element, swap_element_order, add_random_car, shift_car, \
    add_random_comeback, delete_random_comeback
import matplotlib.pyplot as plt
import time


# https://www.pythoncentral.io/time-a-python-function/
def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


xx = []
y = []
yy = []
yyy = []
yyyy = []
yyyyy = []
yyyyyy = []

reapets_num = 3000
for i in range(5, 1000):
    x = Individual()
    x.street_order = np.random.randint(low=-1, high=297, size=i)
    x.street_order = np.insert(x.street_order, i - 3, -1)
    x.street_order = np.insert(x.street_order, i - 2, -1)
    x.street_order = np.insert(x.street_order, i - 1, -1)
    wrapped = wrapper(change_random_element, x)
    wrappedd = wrapper(swap_element_order, x)
    wrappeddd = wrapper(add_random_car, x)
    wrappedddd = wrapper(shift_car, x)
    wrappeddddd = wrapper(add_random_comeback, x)
    wrappedddddd = wrapper(delete_random_comeback, x)

    random_element_stat = []
    xx.append(i)
    y.append(timeit.timeit(wrapped, number=reapets_num))
    yy.append(timeit.timeit(wrappedd, number=reapets_num))
    yyy.append(timeit.timeit(wrappeddd, number=reapets_num))
    yyyy.append(timeit.timeit(wrappedddd, number=reapets_num))
    yyyyy.append(timeit.timeit(wrappeddddd, number=reapets_num))
    yyyyyy.append(timeit.timeit(wrappedddddd, number=reapets_num))

plt.plot(xx, y, label='zamiana węzłów')
plt.plot(xx, yy, label='zamiana ulic')
plt.plot(xx, yyy, label='dodanie nowego samochodu')
plt.plot(xx, yyyy, label='zmiana pozycji samochodu')
plt.plot(xx, yyyyy, label='dodanie powrotu do bazy')
plt.plot(xx, yyyyyy, label='usunięcie powrotu do bazy')

plt.ylabel('czas [sek]')
plt.legend()
plt.xlabel('długość genotypu')
plt.title('Test dla 3000 powtórzeń')
plt.grid()
plt.savefig("../Reports/mutation_time_complex.svg", format="svg", dpi=1200)
plt.show()
plt.close()
