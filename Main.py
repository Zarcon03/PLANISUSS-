import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Visualization import create_visualization_matrix
import planisussConstants as const
from Grid import *
from Struggle import *
from Others import quit, pause, speed_plus, speed_minus


def main():

    # visualization function
    def update_visualization(grid, cax):

        # update the image data for the current visualization
        cax.set_array(create_visualization_matrix(grid))

        # removes from the matrix ticks and ticks labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        
        # update the matrix title
        ax.set_title(f'Day {day}')

        # update and visualize the Animal presence graph
        ax1.cla()
        ax1.plot(days, erbast_counts, color = 'blue', label='Erbast')
        ax1.plot(days, carviz_counts, color = 'red', label='Carviz')
        ax1.legend()
        ax1.set_xlabel('days')
        ax1.set_ylabel('animal presence')
        ax1.set_title('animal over days')
        ax1.grid(True)

        # update and visualize the Vegetob density graph
        ax2.cla()
        ax2.plot(days, vegetob_count, color = 'green', label='Vegetob')
        ax2.legend()
        ax2.set_xlabel('days')
        ax2.yaxis.set_label_position("right")
        ax2.set_ylabel('Vegetob density')
        ax2.yaxis.tick_right()
        ax2.set_title('Vegetob over days')
        ax2.grid(True)

        # draw the updated figure and style it
        plt.style.use('Solarize_Light2')
        plt.draw()


    """ GRID CREATION """
    grid = create_grid(const.NUMCELLS)

    populate_grid(grid)

    # create a figure and axis
    fig, (ax1, ax, ax2) = plt.subplots(1,3)

    # create the visualization matrix for the initial state
    visualization_matrix = create_visualization_matrix(grid)

    # display the initial visualization
    cax = ax.imshow(visualization_matrix, interpolation='nearest')
    
    # make the plot interactive
    plt.ion()

    # create the pause button 
    ax_stop_go = plt.axes([0.402, 0.11, 0.1, 0.07])
    button_stop_go = Button(ax_stop_go, 'Stop/Go', color='blue', hovercolor='blue')
    button_stop_go.on_clicked(pause)

    # create the quit button
    ax_close = plt.axes([0.52, 0.11, 0.1, 0.07])
    button_quit = Button(ax_close, 'Quit', color = 'red', hovercolor='red')
    button_quit.on_clicked(quit)

    # create the speed buttons
    ax_speed_plus = plt.axes([0.05, 0.95, 0.05, 0.03])
    button_speed_plus = Button(ax_speed_plus, '+', color = 'yellow', hovercolor='white')
    button_speed_plus.on_clicked(speed_plus)

    ax_speed_minus = plt.axes([0, 0.95, 0.05, 0.03])
    button_speed_minus = Button(ax_speed_minus, '-', color = 'yellow', hovercolor='white')
    button_speed_minus.on_clicked(speed_minus)

    """ List inizialization for graphs """
    erbast_counts = []
    carviz_counts = []
    vegetob_count = []
    days = []

    """ Start of the main loop for simulation """
    for day in range(const.NUMDAYS):
        
        from Others import is_paused, vel

        erbast_daily = 0 
        carviz_daily = 0
        vegetob_daily = 0
        days.append(day)

        """ GROWING PHASE """

        for row in range(const.NUMCELLS):
            for col in range(const.NUMCELLS):

                if grid[row][col].type == "Ground":
                    grid[row][col].vegetob.growing()
                    
                    vegetob_daily += grid[row][col].get_vegetob_amount()

        # Check for pause
        while is_paused:
            plt.pause(1)
            from Others import is_paused

        """ MOVEMENT PHASE """

        for row in range(const.NUMCELLS):
            for col in range(const.NUMCELLS):


                if grid[row][col].type == "Ground":
                
                    lenHerds = len(grid[row][col].herds)
                    lenPrides = len(grid[row][col].prides)

                    for i in range(lenHerds):
                        grid[row][col].herds[0].movement()

                    for i in range(lenPrides):
                        #print('carviz move')
                        grid[row][col].prides[0].movement()
        
        # Check for pause
        while is_paused:
            plt.pause(1)
            from Others import is_paused

        """ GRAZING PHASE """

        for row in range(const.NUMCELLS):
            for col in range(const.NUMCELLS):

                if grid[row][col].type == "Ground":

                    for i in range(len(grid[row][col].herds)):
                        grid[row][col].herds[i].graze()

        # Check for pause
        while is_paused:
            plt.pause(1)
            from Others import is_paused

        """ STRUGGLE PHASE """

        for row in range(const.NUMCELLS):
            for col in range(const.NUMCELLS):

                if grid[row][col].type == "Ground":
                    # group organization of herds
                    herd_org(grid[row][col])

                    # group organizaion of prides
                    pride_org(grid[row][col])

                    # the prides that didn't fight start the hunt
                    if grid[row][col].prides:

                        for pride in grid[row][col].prides:
                            if pride.fight == False:
                                pride.hunt()

                            # we set the fight variable back to false for the next day loop
                            else:
                                pride.fight = False

        # Check for pause
        while is_paused:
            plt.pause(1)
            from Others import is_paused                

        """ SPAWNING PHASE """

        for row in range(const.NUMCELLS):
            for col in range(const.NUMCELLS):

                if grid[row][col].type == "Ground":

                    animals = grid[row][col].inhabitants.copy()

                    for animal in animals:
                        animal.ageing()
                    
                    # keep count of the number of animals each day
                    erbast_daily += grid[row][col].count_erbast()
                    carviz_daily += grid[row][col].count_carviz()


        # update of the graphs lists
        erbast_counts.append(erbast_daily)
        carviz_counts.append(carviz_daily)
        vegetob_count.append(vegetob_daily)


        """ VSUALIZATION """

        update_visualization(grid, cax)

        # pause for a short time to create an animation effect
        plt.pause(vel)
        
        # Check for pause
        while is_paused:
            plt.pause(1)
            from Others import is_paused
                
    # manual close after all days
    plt.ioff()
    plt.show(block=True)  # block until the window is closed

    #plt.savefig("Sim" + str(count) + ".png")
    #plt.close()