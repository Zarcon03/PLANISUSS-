import planisussConstants as const
from Inhabitants import *
from Grid import *
from Others import neighborhood_cells
import random

class Group:
    def __init__(self):
        self.members = []
        self.cell = None

    def add_member(self, animal):
        if len(self.members) < self.max_size and animal not in self.members:
            self.members.append(animal)
            
            if self.cell is None:
                self.cell = animal.cell
            return True
            
        return False

    def remove_member(self, animal):
        if animal in self.members:
            self.members.remove(animal)

    def getSize(self):
        return len(self.members)
    
    def isFull(self):
        return len(self.members) >= self.max_size
    
    def group_movement_choice(self):
        if isinstance(self, Herd):
            sumTrue = sumFalse = 0

            for animal in self.members:
                if animal.should_move_Erbast():
                    #print('vero')
                    sumTrue += 1
                else:
                    #print('falso')
                    sumFalse += 1

            if sumTrue >= sumFalse:
                return True
            
            return False
        
        if isinstance(self, Pride):
            sumTrue = sumFalse = 0

            for animal in self.members:
                if animal.should_move_Carviz():
                    #print('vero')
                    sumTrue += 1
                else:
                    #print('falso')
                    sumFalse += 1

            if sumTrue >= sumFalse:
                return True
            
            return False            
        

class Herd(Group):
    def __init__(self):
        super().__init__()
        self.max_size = const.MAX_HERD

    def graze(self):
        vegetob_available = self.cell.get_vegetob_amount()

        """ DISTRIBUTE VEGETOB AMONG MEMBERS OF THE GROUP BASED ON THEIR ENERGY LEVELS """
        
        # sort members by energy in ascending order
        sorted_members = sorted(self.members, key=lambda erbast: erbast.energy)

        # calculate the total energy deficit of all members
        total_deficit = sum(100 - erbast.energy for erbast in sorted_members)

        # calculate vegetob distribution
        vegetob_per_erbast = []

        for erbast in sorted_members:
            if total_deficit:
                share = (100 - erbast.energy) / total_deficit
                vegetob_share = share * vegetob_available
                vegetob_share = int(vegetob_share)
                vegetob_per_erbast.append((erbast, vegetob_share))

        # distribute vegetob among members
        for erbast, vegetob in vegetob_per_erbast:
            erbast.eat_vegetob(vegetob)

    def movement(self):
        neighboring_cells = neighborhood_cells(self.cell.grid, self.cell)
         
        if neighboring_cells:
            new_cell = herd_cell_choice(neighboring_cells, self.cell)
            
            if new_cell == self.cell: return
        else: 
            return
        
        if self.group_movement_choice():
            moving_animals = [animal for animal in self.members if animal.should_move_Erbast() or animal.socialAttitude >= 0.7 and animal.energy > 2]
        else:
            moving_animals = [animal for animal in self.members if animal.should_move_Erbast() and animal.socialAttitude < 0.7]

        # check if the new cell can host all moving animals
        while new_cell.count_erbast() + len(moving_animals) > const.MAX_HERD:
            neighboring_cells.remove(new_cell)
            new_cell = herd_cell_choice(neighboring_cells, self.cell)

            if new_cell == self.cell: return
        #print(new_cell.position)

        """ MOVEMENT PHASE """

        member_list = self.members.copy()
        
        for animal in member_list:
            if animal in moving_animals:

                    self.cell.inhabitants.remove(animal)
                    new_cell.inhabitants.add(animal)
                    #print("L'animale: " + str(animal) + "è stato aggiunto ad inhabitants: " + str(new_cell.inhabitants))

                    animal.leave_herd(self)
                    #print("L'animale: " + str(animal) + "ha lasciato l'herd:" + str(self.members))

                    animal.cell = new_cell
                    #print("L'animale: " + str(animal) + "si è mosso nella cella: " + str(new_cell.position))
                    
                    animal.moves()
                    #print(animal.energy, animal.moved)
            else:
                animal.moved = False
                #print('animale non mosso: ' + str(animal))

        # remove empty herds
        if self.members == []:
            self.cell.herds.remove(self)

def herd_cell_choice(cells_list, cella):
    cell_list = []
    target_score = get_cell_score_herd(cella)

    for cell in cells_list:
        score = get_cell_score_herd(cell)

        if score > target_score:
            target_score = score
            cell_list = []
            cell_list.append(cell)
        
        if score == target_score:
            cell_list.append(cell)

    return random.choice(cell_list) if cell_list else cella

def get_cell_score_herd(cell):

    """ THE SCORE HEAVILY DEPENDS ON VEGETOB DENSITY, 
        IT'S ALSO AFFECTED NEGATIVELY BY CARVIZ PRESENCE """    
    
    carviz_score = const.MAX_PRIDE - cell.count_carviz()
    vegetob_score = cell.get_vegetob_amount() / 100 if cell.vegetob else 0
    score = carviz_score * vegetob_score

    return score

class Pride(Group):
    def __init__(self):
        super().__init__()
        self.max_size = const.MAX_PRIDE
        self.fight = False

    def movement(self):
        neighboring_cells = neighborhood_cells(self.cell.grid, self.cell)
         
        if neighboring_cells:
            new_cell = pride_cell_choice(neighboring_cells, self.cell)
            
            if new_cell == self.cell: 
                return
        else:
            return
            
        if self.group_movement_choice():
            moving_animals = [animal for animal in self.members if animal.should_move_Carviz() or animal.socialAttitude >= 0.7 and animal.energy > 2]
        else:
            moving_animals = [animal for animal in self.members if animal.should_move_Carviz() and animal.socialAttitude < 0.7]

        if moving_animals:
            new_pride = Pride()
            new_pride.cell = new_cell
            new_cell.prides.append(new_pride)
        #print(new_cell.position)

        """ MOVEMENT PHASE """

        member_list = self.members.copy()
        
        for animal in member_list:
            if animal in moving_animals:

                    self.cell.inhabitants.remove(animal)
                    new_cell.inhabitants.add(animal)

                    animal.join_pride(new_pride)
                    #print("ciao, sono entrato nel pride: " + str(new_pride) + ",\n e mi chiamo: " + str(animal) + "\n")

                    animal.moves()
            else:
                animal.moved = False
                #print("ciao, mi chiamo: " + str(animal) + " e non mi sono mosso")

        # remove empty prides
        if self.members == []:
            self.cell.prides.remove(self)

    def hunt(self):
        if len(self.cell.herds) == 0 or self.cell.herds[0].members == []:
            return

        strongest_erbast = max(self.cell.herds[0].members, key=lambda erbast: erbast.energy)
        n = (strongest_erbast.energy * 20) // 100

        """
            The pride loses energy based on the energy of the strongest_erbats, 
            regardless of the result of the hunt
        """
        s = n

        while s > 0:
            # a quick check to make sure the pride has members
            if len(self.members) == 0:
                self.cell.prides.remove(self)
                return
            
            i = random.randint(0, max(0, len(self.members) - 1))

            # a random carviz of the pride loses 1 energy for each iteration
            self.members[i].decrease_energy(1)
            s -= 1

        """ 
            We calculate the probability of the hunt being successful based on the energy amount
            of the strongest_erbast. Assuming that if it has low energy it will have a low percentage 
            possibility of survival, and with its survival rate going up to 20% if it has max energy
        """

        if random.randint(0, 100) > n:
            food = strongest_erbast.energy
            sorted_members = sorted(self.members, key=lambda carviz: carviz.energy)
            total_deficit = sum(100 - carviz.energy for carviz in sorted_members)

            # calculate vegetob distribution
            for carviz in sorted_members:
                if total_deficit:
                    share = (100 - carviz.energy) / total_deficit
                    energy_share = share * food
                    energy_share = int(energy_share)
                    carviz.energy = min(carviz.maxEnergy, (carviz.energy + energy_share))

            strongest_erbast.decrease_energy(100)

        # if the erbast manages to survive he loses half his energy
        else:
            strongest_erbast.energy = strongest_erbast.energy // 2


def pride_cell_choice(cells_list, cella):
    cell_list = []
    target_score = get_cell_score_pride(cella)

    for cell in cells_list:
        score = get_cell_score_pride(cell)

        if score > target_score:
            target_score = score
            cell_list = []
            cell_list.append(cell)
        
        if score == target_score:
            cell_list.append(cell)

    return random.choice(cell_list) if cell_list else cella

def get_cell_score_pride(cell):

    """ THE SCORE HEAVILY DEPENDS ON ERBAST PRESENCE, 
        IT'S ALSO AFFECTED NEGATIVELY BY CARVIZ PRESENCE """

    erbast_score = cell.count_erbast()
    carviz_score = cell.count_carviz() // const.MAX_PRIDE
    n = random.random()
    score = (erbast_score + n) - carviz_score

    return score