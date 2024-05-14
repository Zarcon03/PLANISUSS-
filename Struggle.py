from Inhabitants import *
import random


def herd_org(cell):
    if cell.count_erbast():

        if len(cell.herds) == 0:
            new_herd = Herd()
            new_herd.cell = cell
            cell.herds.append(new_herd)
            erbast_list = [animal for animal in cell.inhabitants if isinstance(animal, Erbast)]

            for animal in erbast_list:      
                animal.join_herd(new_herd)
            #print(new_herd.members)

        else:
            erbast_list = [animal for animal in cell.inhabitants if isinstance(animal, Erbast) and animal.moved == True]

            for animal in erbast_list:
                animal.join_herd(cell.herds[0])

def pride_org(cell):

    while cell.count_carviz() > const.MAX_PRIDE:
        fight(cell)
        #print('hanno fightato')
        #print(cell.prides)

    """ WE CHECK WETHER THERE ARE MULTIPLE PRIDES IN THE CELL AND IF THEY CAN'T MERGE THEY FIGHT TILL ONLY ONE SURVIVES """

    if len(cell.prides) != 1 and cell.count_carviz() > 0:

        while len(cell.prides) != 0:
            cell.prides.remove(cell.prides[0])
        #print(cell.prides)

        new_pride = Pride()
        cell.prides.append(new_pride)
        #print(cell.prides)
        carviz_list = [animal for animal in cell.inhabitants if isinstance(animal, Carviz)]

        for animal in carviz_list:
            animal.join_pride(new_pride)
            #print(new_pride.members)
        

def fight(cell):
    pride1 = cell.prides[0]
    pride2 = cell.prides[1]
    energy1 = 0
    energy2 = 0

    for animal in pride1.members:
        energy1 += animal.energy

    for animal in pride2.members:
        energy2 += animal.energy
    
    """ THE FIGHT RESULT DEPENDS ON A RANDOM FACTOR THAT FAVOURITES PRIDES WITH HIGHER ENERGY """

    if random.randint(0, int(energy1)) > random.randint(0, int(energy2)):

        while len(pride2.members) != 0:
            pride2.members[0].decrease_energy(101)
        #print("membri morti pride2 " + str(pride2.members))

        cell.prides.remove(pride2)
        #print(cell.prides)

        # the animals of the winning pride get a boost of social attitude
        for animal in pride1.members:
            n = animal.socialAttitude + 0.1
            animal.socialAttitude = max(n, 1)

        pride1.fight = True
        #print('ha vinto il pride: ' + str(pride1) + 'e i suoi membri sono: ' + str(pride1.members))
    
    else:

        while len(pride1.members) != 0:
            pride1.members[0].decrease_energy(101)
        #print('membri morti pride1 ' + str(pride1.members))
        
        cell.prides.remove(pride1)
        #print(cell.prides)

        # the animals of the winning pride get a boost of social attitude
        for animal in pride2.members:
            n = animal.socialAttitude + 0.1
            animal.socialAttitude = max(n, 1)

        pride2.fight = True
        #print('ha vinto il pride: ' + str(pride2) + 'e i suoi membri sono: ' + str(pride2.members))