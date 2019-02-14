import numpy as np
from data_structers.individual import Individual
import random
from datetime import datetime

'''

                        HELPERY
'''


def get_time_based_unique_vector(low: int, hight: int, size: int) -> np.array:
    random.seed(datetime.now())
    if hight - low < size:
        raise ValueError("Unable to rand unique Vector low=" + str(low) + "max=" + str(hight) + "size=" + str(size))
    x = random.sample(range(low, hight), size)
    return np.array(x)


def change_one_element_permutation(array: np.array) -> np.array:
    size = array.size
    element_position_out, element_position_in = np.random.randint(low=0, high=size - 1, size=2)
    el = array[element_position_out];
    try:
        if el < 0:
            raise ValueError('Trying to change Car route pointer')
    except ValueError as bad:
        while el < 0:
            element_position_out, element_position_in = np.random.randint(low=0, high=size - 1, size=2)
            el = array[element_position_out]
    size2 = array.size
    if size != size2:
        raise BaseException('Array size mis match:' + size2.__str__() + ' vs ' + size.__str__())
    array = np.delete(array, element_position_out)
    array = np.insert(array, element_position_in, el)
    return array


def shift_one_marker(array: np.array, marker) -> np.array:
    shift_pointers = np.argwhere(array == marker)
    if shift_pointers.size is not 0:
        pointer_to_shift = shift_pointers[get_time_based_unique_vector(low=0, hight=shift_pointers.size, size=1)]
        place_to_shift = get_time_based_unique_vector(low=0, hight=array.size, size=1)
        array[pointer_to_shift], array[place_to_shift] = array[place_to_shift], array[pointer_to_shift]
    return array


def add_marker_in_random(array: np.array, marker: int, n_elements: int = 1) -> np.array:
    rnd = get_time_based_unique_vector(0, array.size, n_elements)
    for x in rnd:
        array = np.insert(array, x, marker)
    return array


def swap_random_elements(array: np.array, n_elements: int = 2) -> np.array:
    indexes_to_swap = get_time_based_unique_vector(0, array.shape[0], n_elements)
    value_at_indexes = []
    for elem in indexes_to_swap:
        value_at_indexes.append(array[elem])
    indexes_to_swap = np.roll(indexes_to_swap, n_elements - 1)
    for i in range(len(indexes_to_swap)):
        array[indexes_to_swap[i]] = value_at_indexes[i]
    return array


'''
Lista operatorow mutacji:




'''


def change_random_element(individual: Individual):
    '''
    1: Wygeneruj losowa wartosc z zakresu
    2: Wez te liczbe i usun ja z kolejki
    3: wstaw liczbe w dowolne miejsce
    :param individual:
    :return: Zmutowany osobnik o zmienionym jednym elemencie wariancji
    '''
    individual.street_order = change_one_element_permutation(np.copy(individual.street_order))


def swap_element_order(individual: Individual, n_elements: int = 2) -> None:
    '''

    :param individual:
    :param n_elements:
    :return:
    '''
    individual.street_order = swap_random_elements(individual.street_order, n_elements)


def add_random_car(individual: Individual) -> None:
    '''

    :param individual:
    :param n_elements: insert -1 to vector n_eleements times
    :return:
    '''
    if individual.max_number_of_cars > individual.number_of_cars + 1:
        individual.street_order = add_marker_in_random(individual.street_order, -1, n_elements=1)
        individual.number_of_cars = np.count_nonzero(individual.street_order == -1)


def delete_random_comeback(individual: Individual) -> None:
    zer_counter = np.count_nonzero(individual.street_order == 0)
    if zer_counter > 1:
        zero_indexes = np.where(individual.street_order == 0)[0]
        index = np.random.choice(zero_indexes, 1)
        if individual.street_order[index] == 0:
            individual.street_order = np.delete(individual.street_order, index)


def add_random_comeback(individual: Individual) -> None:
    individual.street_order = add_marker_in_random(individual.street_order, 0, 1)


def shift_car(individual: Individual) -> None:
    '''
    Not tested!
    :param individual:
    :return:
    '''
    individual.street_order = shift_one_marker(individual.street_order, marker=-1)


def delete_random_car(individual: Individual) -> None:
    print('dupa')
    car_counter = np.count_nonzero(individual.street_order == -1)
    if car_counter > 1:
        car_indexes = np.where(individual.street_order == 0)[0]
        index = np.random.choice(car_indexes, 1)
        if individual.street_order[index] == -1:
            individual.street_order = np.delete(individual.street_order, index)
