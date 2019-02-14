from data_structers.individual import Individual, combine_stats
import numpy as np
import random
from datetime import datetime


def longest_common_num_seq(s1, s2):
    m = [[0] * (1 + s2.size) for i in range(1 + s1.size)]
    longest, x_longest = 0, 0
    for x in range(1, 1 + s1.size):
        for y in range(1, 1 + s2.size):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def create_cross_table(array1: np.array, array2: np.array) -> np.array:
    common = longest_common_num_seq(array1, array2)
    if len(common < 3):
        p = random.randint(0, len(array2))
        k = random.randint(p, len(array2))
        common = array2[p:k]
    tab1 = np.setdiff1d(array1, common)
    '''tablica bez wspolnego podciagu, trzeba ja pomieszac i wstawic podciag w jakies miejsce'''
    res = tab1
    random.seed(datetime.now())
    res = np.insert(arr=res, obj=random.randint(0, res.size), values=common)
    return res


def cross_indvidual_longest_common(ind1: Individual, ind2: Individual) -> Individual:
    '''
    :param ind1:
    :param ind2:
    :return: new individual cross of ind1 and ind2
    '''
    child = Individual()
    child.street_order = create_cross_table(np.copy(ind1.street_order), np.copy(ind2.street_order))
    child.genesis = combine_stats(stat1=ind1.genesis, stat2=ind2.genesis)

    child.genesis.cross_indvidual_longest_common_counter += 1
    child.max_number_of_cars = ind1.max_number_of_cars
    child.number_of_cars = np.count_nonzero(child.street_order == -1)
    return child


def cross_indvidual_random(ind1: Individual, ind2: Individual) -> Individual:
    '''
    :param ind1:
    :param ind2:
    :return: new individual cross of ind1 and ind2
    '''
    random.seed(datetime.now())
    pos = random.randint(0, ind1.street_order.shape[0] - 1)
    il_el = random.randint(1, min(ind1.street_order.shape[0] - pos, 10))
    part1 = ind1.street_order[pos:pos + il_el].copy()
    new = ind2.street_order.copy()
    for i in range(0, len(part1)):
        j = 0
        while j < len(new):
            if part1[i] == new[j]:
                new = np.delete(new, j)
                break
            j += 1
    new = np.array(new)
    part1 = np.array(part1)
    child = Individual()
    pos2 = random.randint(0, len(new))
    tmp = np.concatenate((new[0:pos2], part1, new[pos2:len(new)]), axis=None)
    child.street_order = tmp
    child.genesis = combine_stats(stat1=ind1.genesis, stat2=ind2.genesis)
    child.genesis.cross_indvidual_random_counter += 1
    child.max_number_of_cars = ind1.max_number_of_cars
    child.number_of_cars = np.count_nonzero(child.street_order == -1)
    return child
