import timeit
from data_structers.individual import Individual
import numpy as np
from data_structers.mutation_operators import change_random_element, swap_element_order, add_random_car, shift_car, \
    add_random_comeback, delete_random_comeback
import matplotlib.pyplot as plt
from data_structers.cross_operators import cross_indvidual_random, cross_indvidual_longest_common


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


x = []
random = []
common = []

reapets_num = 250
for i in range(5, 250):
    print(i)
    first = Individual()
    second = Individual()
    first.street_order = np.random.randint(low=-1, high=297, size=i)
    first.street_order = np.insert(first.street_order, i - 3, -1)
    first.street_order = np.insert(first.street_order, i - 2, -1)
    first.street_order = np.insert(first.street_order, i - 1, -1)
    second.street_order = np.random.randint(low=-1, high=297, size=i)
    second.street_order = np.insert(second.street_order, i - 3, -1)
    second.street_order = np.insert(second.street_order, i - 2, -1)
    second.street_order = np.insert(second.street_order, i - 1, -1)
    wrapped = wrapper(cross_indvidual_random, first, second)
    wrappedd = wrapper(cross_indvidual_longest_common, first, second)

    x.append(i)
    random.append(timeit.timeit(wrapped, number=reapets_num))
    common.append(timeit.timeit(wrappedd, number=reapets_num))


plt.plot(x, random, label='krzyżowanie losowe')
plt.plot(x, common, label='krzyżowanie z podciągu')
plt.ylabel('czas [sek]')
plt.legend()
plt.xlabel('długość genotypu')
plt.title('Test dla '+str(reapets_num)+' powtórzeń')
plt.grid()
plt.savefig("../Reports/cross_time_complex.svg", format="svg", dpi=1200)
plt.show()