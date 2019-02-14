from data_structers.individual import Population, Individual, delete_adjacents
from data_structers.algorithm_report import AlgorithmNotificator
from data_structers.cross_operators import cross_indvidual_random, cross_indvidual_longest_common
from data_structers.mutation_operators import *

from data_structers.mutation_operators import swap_element_order, add_random_car, change_one_element_permutation, \
    get_time_based_unique_vector, shift_car, change_random_element
import numpy as np
import random
from time import gmtime, strftime
from datetime import datetime
import copy


def tournament_select_parents(population: Population, turnament_size: int = 2) -> []:
    tournament = []
    indexes = get_time_based_unique_vector(0, len(population.ind_list), turnament_size)
    for i in indexes:
        tournament.append(population.ind_list[i])
    turnament_key = lambda a: a.cost_function_value
    tournament = sorted(tournament, key=turnament_key)
    if len(tournament) < 2:
        raise ValueError('Tournament size < 2 ')
    return tournament[:2]


def get_cf_table(population: Population) -> []:
    arr = []
    for ind in population.ind_list:
        arr.append(ind.cost_function_value)
    return arr


def evolution_simulator(initial_population: Population, max_iteration: int, inp_data, cross_coe, mutation_coe: int,
                        turnament_size: int):
    start_time = strftime("%H:%M:%S", gmtime())
    evoluting_population = copy.deepcopy(initial_population)
    cross_limit = round(len(evoluting_population.ind_list) * cross_coe / 100)
    mutation_limit = round(len(evoluting_population.ind_list) * mutation_coe / 100)
    max_population_size = len(initial_population.ind_list)
    history = copy.deepcopy(AlgorithmNotificator())
    for iteration in range(max_iteration):
        '''
        kontrola iteracji i czasu
        '''
        if (iteration % 10 == 0):
            print("iteracja: " + str(iteration) + " z " + str(max_iteration) + " czas: " + strftime("%H:%M:%S",
                                                                                                    (gmtime())))
        '''
        Aktualizacja raportu
        '''
        for ind in evoluting_population.ind_list:
            ind.calculate_cost_value(inp_data)
        evoluting_population.ind_list = evoluting_population.sort_pop()
        history.best_individual = evoluting_population.ind_list[0]
        history.best_individuals_cf.append(evoluting_population.ind_list[0].cost_function_value)
        history.worst_individuals_cf.append(evoluting_population.ind_list[-1].cost_function_value)
        cf_vector = get_cf_table(evoluting_population)
        history.mean_cost_function_value.append(np.mean(cf_vector))
        history.std_cost_function_value.append(np.std(cf_vector))
        '''
        wykonujemy operacje krzyzowania
        dopoki inex < od max krzyzowan
        1) Wybierz 2 rodzicow
        2) Skrzyzuj 
        3) Usun najgorsze rozwiazanie, wstaw nowo otrzymane
        '''
        for cross_number_counter in range(cross_limit):
            chosen_parents = tournament_select_parents(evoluting_population, min(turnament_size, max_population_size))

            if cross_number_counter % 2 == 0:
                descendant = cross_indvidual_longest_common(chosen_parents[0], chosen_parents[1])
            else:
                descendant = cross_indvidual_random(chosen_parents[0], chosen_parents[1])
            descendant.calculate_cost_value(inp_data)
            sparta_wsp = random.randint(0, 100)

            if descendant.cost_function_value > history.mean_cost_function_value[-1]:
                if sparta_wsp >= 5:
                    del descendant
                else:
                    evoluting_population.ind_list[-(cross_number_counter + 1)] = descendant
            else:
                evoluting_population.ind_list[-(cross_number_counter + 1)] = descendant

        for mutation_number_counter in range(mutation_limit):
            scaller = random.randint(1, 6)

            mutant = evoluting_population.ind_list[random.randint(1, len(evoluting_population.ind_list) - 1)]
            save_street_order = mutant.street_order.copy()
            save_cost_value = mutant.cost_function_value

            if scaller is 1:
                change_random_element(mutant)
            elif scaller is 2:
                swap_element_order(mutant)
            elif scaller is 3:
                add_random_car(mutant)
            elif scaller is 4:
                delete_random_comeback(mutant)
            elif scaller is 5:
                add_random_comeback(mutant)
            elif scaller is 6:
                shift_car(mutant)
            elif scaller is 7:
                delete_random_car(mutant)
            else:
                raise ValueError('Bad mutation scaller')
            mutant.calculate_cost_value(inp_data)
            if save_cost_value < mutant.cost_function_value:
                mutant.street_order = save_street_order.copy()
                mutant.cost_function_value = save_cost_value
                if scaller is 1:
                    mutant.genesis.change_random_element_counter += 1
                elif scaller is 2:
                    mutant.genesis.swap_element_order_counter += 1
                elif scaller is 3:
                    mutant.genesis.add_random_car_counter += 1
                elif scaller is 4:
                    mutant.genesis.delete_random_comeback_counter += 1
                elif scaller is 5:
                    mutant.genesis.add_random_comeback_counter += 1
                elif scaller is 6:
                    mutant.genesis.shift_car_counter += 1
                elif scaller is 7:
                    mutant.genesis.delete_random_car_counter += 1
        if len(evoluting_population.ind_list) != max_population_size:
            raise ValueError("Evolutioning population changed size")
    evoluting_population.ind_list = evoluting_population.sort_pop()
    history.best_individual = evoluting_population.ind_list[0]
    history.best_individuals_cf.append(evoluting_population.ind_list[0].cost_function_value)
    history.worst_individuals_cf.append(evoluting_population.ind_list[-1].cost_function_value)
    cf_vector = get_cf_table(evoluting_population)
    history.mean_cost_function_value.append(np.mean(cf_vector))
    history.std_cost_function_value.append(np.std(cf_vector))
    stop_time = strftime("%H:%M:%S", gmtime())
    FMT = '%H:%M:%S'
    history.evolution_time = datetime.strptime(start_time, FMT) - datetime.strptime(stop_time, FMT)
    return history
