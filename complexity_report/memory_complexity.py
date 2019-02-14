from data_structers.individual import Population, Individual
from collections import namedtuple
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from pympler import asizeof

pops = []
nods = []
size = []

for pop in range(200, 350):
    for nod in range(1, 200):
        for xx in range(1, pop):
            xx = Individual()
            xx.street_order = np.zeros(nod, np.int32)
            size.append(round(pop * asizeof.asizeof(xx) / 1000))
            pops.append(pop)
            nods.append(nod)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(pops, nods, size)
ax.set_xlabel('rozmiar populacji')
ax.set_ylabel('liczba węzłów')
ax.set_zlabel('pamięć [KB]')
plt.title('F:(rozmiar populacji, liczba ulic) -> zużywana pamięć')
plt.savefig("../Reports/memory_complex.svg", format="svg", dpi=1200)
plt.show()
