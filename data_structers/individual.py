import numpy as np
from data_structers.inputdata import InputData
import matplotlib.pyplot as plt


def delete_adjacents(alist):
    new = []
    if alist[0] != 0:
        new.append(alist[0])
    for i in range(1, len(alist)):
        if alist[i] == alist[i - 1] and alist[i] != -1:
            continue
        elif i + 1 < len(alist) and alist[i] == 0 and alist[i + 1] == -1:
            continue
        else:
            new.append(alist[i])
    if new[-1] == 0:
        new.pop(-1)
    return np.array(new)


class OperatorsStats:
    cross_indvidual_random_counter = 0
    cross_indvidual_longest_common_counter = 0
    delete_random_car_counter = 0
    shift_car_counter = 0
    add_random_comeback_counter = 0
    delete_random_comeback_counter = 0
    add_random_car_counter = 0
    swap_element_order_counter = 0
    change_random_element_counter = 0

    def __init__(self):
        pass

    def __str__(self):
        return str(self.cross_indvidual_random_counter) + ',' + str(
            self.cross_indvidual_longest_common_counter) + ',' + str(
            self.delete_random_car_counter) + ',' + str(self.shift_car_counter) + ',' + str(
            self.add_random_comeback_counter) + ',' + str(self.delete_random_comeback_counter) + ',' + str(
            self.add_random_car_counter) + ',' + str(
            self.swap_element_order_counter) + ',' + str(self.change_random_element_counter)


class Individual:
    cost_function_value = 0
    number_of_cars = 0
    max_number_of_cars = 0

    def __init__(self, _input_data: InputData = None, array=None):
        if _input_data is not None:
            self.genesis = OperatorsStats()
            number_of_streets = _input_data.streets.shape[0]
            number_of_bins = _input_data.streets.ilosc_koszy.sum()
            max_number_of_cars = _input_data.cars.shape[0] - 1
            self.max_number_of_cars = max_number_of_cars
            number_of_cars = np.random.randint(0, max_number_of_cars)
            self.number_of_cars = number_of_cars
            max_number_of_kurs = number_of_bins / _input_data.cars.pojemnosc.min()
            min_number_of_kurs = number_of_bins / _input_data.cars.pojemnosc.max()
            number_of_kurs = np.random.randint(min_number_of_kurs, max_number_of_kurs)

            self.street_order = np.arange(number_of_streets, dtype=np.int32)
            for i in range(0, number_of_cars):
                self.street_order = np.append(self.street_order, -1)
            for i in range(0, number_of_kurs):
                self.street_order = np.append(self.street_order, 0)
            np.random.shuffle(self.street_order)
            self.car_order = np.arange(0, max_number_of_cars)
            np.random.shuffle(self.car_order)
            self.cost_function_value = 0
            self.genesis.cross_indvidual_longest_common_counter = 1
            self.genesis.cross_indvidual_random_counter = 1
        if array is not None:
            self.street_order = array

    def calc_distance(self, inp: InputData):
        distance = inp.distance_matrix[0][self.street_order[0]]  # od bazy do pierwszego
        '''
        przy odwolywaniu sie do elementow zapomnial pan ze wiersz zerowy zawsze reprezentuje baze....
        '''
        for i in range(1, self.street_order.shape[0] - 1):
            aktualna_pozycja = self.street_order[i]
            if self.street_order[i] > 0 or (self.street_order[i] == 0 and self.street_order[i - 1] != -1):
                step_cost = inp.distance_matrix[self.street_order[i - 1]][self.street_order[i]]
                distance += step_cost
            elif self.street_order[i] == 0 and self.street_order[i - 1] == -1:
                step_cost = inp.distance_matrix[0][self.street_order[i]]
                distance += step_cost
            elif self.street_order[i] == -1:
                # zmiana auta
                step_cost = inp.distance_matrix[self.street_order[i - 1]][0]
                distance += step_cost
            else:
                continue
        distance += inp.distance_matrix[self.street_order[-1]][0]
        return distance

    def calc_car_cost(self, inp: InputData):
        '''
        zle odwoływało sie do kosztow pojazdu. samochod 500 ma kozt 2000 a osiaga funkcja celu wartosc < 2000 xd

        :param inp:
        :return:
        '''
        active_cars = []
        cost = 0
        car_index = 0
        order = np.concatenate((np.array([-1]), self.street_order), axis=None)
        length = len(order)
        for i in range(0, length - 1):
            if order[i] == -1 and ((order[i + 1] == 0 and order[i + 2] > 0) or order[i + 1] > 0):
                active_cars.append(car_index)
                car_index += 1
            elif order[i] == -1 and order[i + 1] == -1:
                car_index += 1
        if len(active_cars) > self.number_of_cars + 1:
            raise ValueError('Car numbes too large in cf ')
        for xx in active_cars:
            cost += inp.cars.koszt_wyjazdu[xx]

        return cost

    def calc_cost_0(self):
        cost = 0
        order = delete_adjacents(self.street_order)

        for i in range(1, len(order) - 1):
            if order[i] == 0:
                cost += 1
        return cost

    def calc_overload(self, inp: InputData):
        cost = 0
        current_car = 0
        current_car_loaded = 0
        for i in range(0, self.street_order.shape[0]):
            if self.street_order[i] > 0:
                current_car_loaded += inp.streets_ilosc_koszy[self.street_order[i]]
                if current_car_loaded > inp.cars_pojemnosc[current_car]:
                    cost += abs(inp.cars_pojemnosc[current_car] - current_car_loaded) ** 2
            elif self.street_order[i] == 0:
                # kurs na baze do [0]

                if current_car_loaded < inp.cars_pojemnosc[current_car]:
                    cost += (inp.cars_pojemnosc[current_car] - current_car_loaded)
                current_car_loaded = 0

            elif self.street_order[i] == -1:
                # zmiana auta
                if current_car_loaded < inp.cars_pojemnosc[current_car]:
                    cost += (inp.cars_pojemnosc[current_car] - current_car_loaded)
                current_car_loaded = 0
                current_car += 1
            else:
                raise ValueError(" Number <  but not 0 or -1")
        return cost

    def calculate_cost_value(self, inp: InputData):
        A = 2  # koszt km
        B = 2  # koszt zebrania 1 kosza
        C = 0.1  # koszt przejechania 1 posesji
        D = 1  # koszt przeładowania
        E = 1  # koszt wysypu smieciarki ( 0 )
        self.street_order = np.array(delete_adjacents(self.street_order))

        cost = B * self.calc_distance(inp)
        # cost += E * self.calc_cost_0()
        cost += D * self.calc_overload(inp)
        cost += self.calc_car_cost(inp)
        self.cost_function_value = cost

    def show_indyvidual(self, inp: InputData):

        plt.plot(inp.streets.longitude, inp.streets.latitude, 'ro')
        color = np.random.randint(0, 7)
        colour = ['blue', 'green', 'red', 'orange', 'cyan', 'black', 'pink', 'magenta']
        for i in range(0, self.street_order.shape[0] - 1):
            if self.street_order[i] == 0:
                color = np.random.randint(0, 7)
            if self.street_order[i] != -1 and self.street_order[i + 1] != -1:
                plt.plot([inp.streets.longitude[self.street_order[i]], inp.streets.longitude[self.street_order[i + 1]]],
                         [inp.streets.latitude[self.street_order[i]], inp.streets.latitude[self.street_order[i + 1]]],
                         color=colour[color])
            else:
                color = np.random.randint(0, 7)

        plt.axis(
            [min(inp.streets.longitude) - 0.002, max(inp.streets.longitude) + 0.002, min(inp.streets.latitude) - 0.002,
             max(inp.streets.latitude) + 0.002])
        plt.show()

        auta = []
        kursy = []
        ulice = []
        html = ""
        z = 0
        order = delete_adjacents(self.street_order)
        if order[-1] == 0:
            order = order[:-2]

        for i in range(0, len(order)):
            if (z > 0 and order[i] == 0):
                continue

            if order[i] > 0:
                ulice.append(order[i])
                z = 0
            elif order[i] == 0:
                kursy.append(ulice.copy())
                ulice.clear()
                z += 1
            elif order[i] == -1:
                auta.append(kursy.copy())
                kursy.clear()
                ulice.clear()

        kursy.append(ulice.copy())
        auta.append(kursy.copy())

        for i in range(0, len(auta)):
            html += "<h3> auto " + i.__str__() + "</h3>"
            html += "<p>" + inp.cars.nazwa[i] + ", poj: " + inp.cars.pojemnosc[i].__str__() + "</p>"
            for j in range(0, len(auta[i])):
                html += "<h4>  kurs " + j.__str__() + "</h4><ol>"
                razem = 0
                for k in range(0, len(auta[i][j])):
                    razem += inp.streets.ilosc_koszy[auta[i][j][k]]
                    html += "<li>" + auta[i][j][k].__str__()
                    html += "--" + inp.streets.miejscowosc[auta[i][j][k]] + ", " + inp.streets.ulica[auta[i][j][k]] \
                            + ", " + inp.streets.ilosc_koszy[auta[i][j][k]].__str__() + "</li>"
                html += "<li><b>RAZEM: " + str(razem) + " / " + inp.cars.pojemnosc[i].__str__() + " koszy</b></li>"
                html += "</ol>"
        html_file = open("../Reports/report.html", "w")
        html_file.write(html)
        html_file.close()


class Population:
    ind_list = []

    def __init_(self, ind_list: [] = []):
        self.ind_list = ind_list

    def append(self, ind: Individual) -> None:
        self.ind_list.append(ind)

    def sort_pop(self):
        def cost_function_compare(ind1: Individual):
            return ind1.cost_function_value

        return sorted(self.ind_list, key=cost_function_compare)


def combine_stats(stat1: OperatorsStats, stat2: OperatorsStats) -> OperatorsStats:
    x = OperatorsStats()
    x.cross_indvidual_random_counter = max(
        [stat1.cross_indvidual_random_counter, stat2.cross_indvidual_random_counter])
    x.cross_indvidual_longest_common_counter = max(
        [stat1.cross_indvidual_longest_common_counter, stat2.cross_indvidual_longest_common_counter])
    x.delete_random_car_counter = (stat1.delete_random_car_counter + stat2.delete_random_car_counter)/2
    x.shift_car_counter = (stat1.shift_car_counter + stat1.shift_car_counter)/2
    x.add_random_comeback_counter = (stat1.add_random_comeback_counter + stat2.add_random_comeback_counter)/2
    x.delete_random_comeback_counter = (stat1.delete_random_comeback_counter + stat2.delete_random_comeback_counter)/2
    x.add_random_car_counter = (stat1.add_random_car_counter + stat2.add_random_car_counter)/2
    x.swap_element_order_counter = (stat1.swap_element_order_counter + stat2.swap_element_order_counter)/2
    x.change_random_element_counter = (stat1.change_random_element_counter + stat2.change_random_element_counter)/2
    return x
