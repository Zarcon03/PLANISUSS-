import numpy as np
import random

from Vegetob import Vegetob
import planisussConstants as const
import Inhabitants as In
from Others import neighborhood_cells


class Cells:
    def __init__(self,  vegetob=None, grid=None):
        self.type = None
        self.vegetob = vegetob
        self.inhabitants = set()
        self.position = None
        self.herds = []
        self.prides = []
        self.grid = grid

    def count_carviz(self):
        return sum(1 for animal in self.inhabitants if isinstance(animal, In.Carviz))
    
    def count_erbast(self):
        return sum(1 for animal in self.inhabitants if isinstance(animal, In.Erbast))

    def get_vegetob_amount(self):
        return self.vegetob.get_density() if self.vegetob else 0
    
    def set_type(self, stringa):
        self.type = stringa

    def vegetob_destroyer(self):
        if self.type == "Water":
            return

        if self.inhabitants == set():
            return

        density = 0
        neighboring_cells = neighborhood_cells(self.grid, self, radius=1)

        # we calculate the mean density of the neighboring cells and check if they are all at maximum
        for cell in neighboring_cells:
            density += cell.vegetob.get_density()
        
        if density / len(neighboring_cells) == 100:
            if self.herds != []:
                self.herds[0].members = []
                self.herds = []

            if self.prides != []:
                self.prides[0].members = []
                self.prides = []
                #print(self.prides)

            self.inhabitants = set()
            

def create_grid(numcells):

    """ Initialize an empty numpy array with the specified dimensions """

    griglia = np.empty((numcells, numcells), dtype=object)
    for i in range(numcells):
        for j in range(numcells):
            
            griglia[i][j] = Cells()

            if i == 0 or j == 0 or i == const.NUMCELLS-1 or j == const.NUMCELLS-1:
                # If it's an outer cell, make it water
                griglia[i][j].set_type('Water')
                griglia[i][j].position = (i, j)

            else:
                # If it's an inner cell, 20% chance of water, otherwise ground with Vegetob
                if np.random.random() < 0.2:
                    griglia[i][j].set_type('Water')
                    griglia[i][j].position = (i, j)

                else:
                    vegetob_density = random.randint(60, 80)
                    vegetob = Vegetob(vegetob_density)
                    griglia[i][j] = Cells(vegetob, griglia)
                    griglia[i][j].set_type('Ground')
                    griglia[i][j].position = (i, j)

            #print(griglia[i][j].position)
            #print(griglia[i][j].type)

    return griglia


def populate_grid(grid):
    carvizSpawned = 0
    erbastSpawned = 0

    # we select a random ground cell and put an erbast in it for ERBAST_SPAWNED times
    while erbastSpawned < const.ERBAST_SPAWNED:

        i = random.randint(1, const.NUMCELLS-2)
        j = random.randint(1, const.NUMCELLS-2)

        if grid[i][j].type == "Ground" and grid[i][j].count_erbast() < const.MAX_HERD:
            
            grid[i][j].inhabitants.add(In.Erbast(grid[i][j]))
            #print(grid[i][j].inhabitants)

            erbastSpawned += 1


    # we select a random ground cell and put an erbast in it for CARVIZ_SPAWNED times
    while carvizSpawned < const.CARVIZ_SPAWNED:

        i = random.randint(1, const.NUMCELLS-2)
        j = random.randint(1, const.NUMCELLS-2)

        if grid[i][j].type == "Ground" and grid[i][j].count_carviz() < const.MAX_PRIDE:

            grid[i][j].inhabitants.add(In.Carviz(grid[i][j]))
            #print(grid[i][j].inhabitants)
            
            carvizSpawned += 1