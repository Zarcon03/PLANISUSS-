import numpy as np

from Grid import *
import planisussConstants as const
from Vegetob import *
from AnimalGroups import *

def create_visualization_matrix(grid):
    visualization_matrix = np.zeros((const.NUMCELLS, const.NUMCELLS, 3))

    for i in range(const.NUMCELLS):
        for j in range(const.NUMCELLS):
            cell = grid[i][j]
            if cell.type == 'Water':
                visualization_matrix[i, j] = [0.2, 0.2, 1]  # light blue for water
            elif cell.type == 'Ground':
                if cell.vegetob:
                    density_percentage = cell.vegetob.density / 100.0
                    color = [1 - 1 * density_percentage, 1, 1 - 1 * density_percentage]

                    visualization_matrix[i, j] = color


                    if cell.count_erbast():
                        ratio = cell.count_erbast()/const.MAX_HERD
                        visualization_matrix[i, j] = [0, 0, 0.4 - 0.4*ratio]  # dark blue for erbast


                if cell.count_carviz():
                    ratio = cell.count_carviz()/const.MAX_PRIDE
                    visualization_matrix[i, j] = [1, 0.5 - 0.5*ratio, 0.5 - 0.5*ratio]  # red for carviz

    return visualization_matrix