import numpy as np
import sys
import planisussConstants as const


def neighborhood_cells(grid, cell, radius=2):
    current_x, current_y = cell.position
    neighboring_cells = []

    # getting the dimensions using np.shape
    grid_shape = np.shape(grid)
    for i in range(max(0, current_x - radius), min(grid_shape[0], current_x + radius + 1)):
        for j in range(max(0, current_y - radius), min(grid_shape[1], current_y + radius + 1)):
            if (i, j) != (current_x, current_y) and grid[i][j].type != 'Water':
                neighboring_cells.append(grid[i][j])
    #for i in range(len(neighboring_cells)):
    #    print(neighboring_cells[i].position)
    #return 'prova'
    return neighboring_cells

# quit function
def quit(event):
    sys.exit()

# pause check variable 
is_paused = False

# pause function
def pause(event):
    global is_paused

    if is_paused:
        is_paused = False
    else:
        is_paused = True

# speed variable
vel = const.ANI_SPEED

# speed functions
def speed_plus(event):
    global vel

    vel = max(0.1, (vel - 0.1))

def speed_minus(event):
    global vel

    vel = min(1, (vel + 0.1))