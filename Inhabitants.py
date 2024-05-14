import random

import planisussConstants as const
from AnimalGroups import herd_cell_choice, Herd, Pride
from Others import neighborhood_cells

class Animals:
    def __init__(self, cell):
        self.lifetime = self.set_lifetime()
        self.socialAttitude = random.random()
        self.maxEnergy = const.MAX_ENERGY
        self.energy = self.set_energy()
        self.age = 0
        self.dead = False
        self.moved = False
        self.cell = cell

    def set_energy(self):
        energy = random.randint(50, self.maxEnergy)
        return energy
       
    def set_lifetime(self):
        if isinstance(self, Erbast):
            lifetime = random.randint(33, const.MAX_LIFE)
        if isinstance(self, Carviz):
            lifetime = random.randint(50, const.MAX_LIFE)
        return lifetime

    def get_energy(self):
        return self.energy
    
    def get_lifetime(self):
        return self.lifetime
   
    def get_social_attitude(self):
        return self.socialAttitude
   
    def ageing(self):
        self.age += 1

        if self.age % 10 == 0 and self.age != 0:
            self.decrease_maxEnergy(8) 
            self.decrease_energy(2)

        if self.age > self.lifetime and self.dead == False:
            self.die()

    def decrease_energy(self, decrease_amount):
        self.energy -= decrease_amount
        if self.energy <= 0:
            self.die()
    
    def decrease_maxEnergy(self, decrease_amount):
        self.maxEnergy -= decrease_amount
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy

    def die(self):
        if self.energy > 0:
            self.spawn_offspring()

        if isinstance(self, Erbast):
            if self.herd:
                self.leave_herd(self.herd)

        if isinstance(self, Carviz):
            if self.pride:
               self.leave_pride(self.pride)

        self.dead = True
        self.remove_dead()

    def remove_dead(self):
        if self.dead:
            self.cell.inhabitants.remove(self)

    def spawn_offspring(self):

        if isinstance(self, Erbast):
            
            #print('Ci sono 2 erbast in piu')

            if self.herd is not None:

                """ Offspring 1 """
                if self.herd.getSize() < const.MAX_HERD:

                    offspring1 = self.__class__(
                        cell = self.cell
                    )
                    offspring1.socialAttitude = self.socialAttitude
                    offspring1.energy = self.energy / 2
                    offspring1.lifetime = self.lifetime

                    offspring1.join_herd(self.herd)
                    #print(offspring1.herd)
                    self.cell.inhabitants.add(offspring1)
                
                else:
                    neighboring_cells = neighborhood_cells(self.cell.grid, self.cell, radius = const.OFFSPRING_RADIUS)
                    target_cell = herd_cell_choice(neighboring_cells, self.cell)

                    if target_cell != self.cell:
                        offspring1 = self.__class__(
                            cell = target_cell
                        )
                        offspring1.socialAttitude = self.socialAttitude
                        offspring1.energy = self.energy / 2
                        offspring1.lifetime = self.lifetime

                        newHerd = Herd()
                        newHerd.cell = target_cell
                        target_cell.herds.append(newHerd)
                        
                        offspring1.join_herd(newHerd)
                        #print(offspring1.herd)
                        target_cell.inhabitants.add(offspring1)

                #print(offspring1.cell.position)
                #print(offspring1.socialAttitude)
                #print(offspring1.energy)
                #print(offspring1.lifetime)
                #print('1')

                """ Offspring 2 """
                if self.herd.getSize() < const.MAX_HERD:

                    offspring2 = self.__class__(
                        cell = self.cell
                    )
                    offspring2.socialAttitude = self.socialAttitude
                    offspring2.energy = self.energy / 2
                    offspring2.lifetime = self.lifetime

                    offspring2.join_herd(self.herd)
                    #print(offspring2.herd)
                    self.cell.inhabitants.add(offspring2)
                
                else:
                    neighboring_cells = neighborhood_cells(self.cell.grid, self.cell, radius = const.OFFSPRING_RADIUS)
                    target_cell = herd_cell_choice(neighboring_cells, self.cell)

                    if target_cell != self.cell:
                        offspring2 = self.__class__(
                            cell = target_cell
                        )
                        offspring2.socialAttitude = self.socialAttitude
                        offspring2.energy = self.energy / 2
                        offspring2.lifetime = self.lifetime

                        newHerd = Herd()
                        newHerd.cell = target_cell
                        target_cell.herds.append(newHerd)
                        
                        offspring2.join_herd(newHerd)
                        #print(offspring2.herd)
                        target_cell.inhabitants.add(offspring2)

                #print(offspring2.cell.position)
                #print(offspring2.socialAttitude)
                #print(offspring2.energy)
                #print(offspring2.lifetime)
                #print('2')

        if isinstance(self, Carviz):
            
            #print('Ci sono 2 carviz in piu')

            if self.pride is not None:

                """ Offspring 1 """
                if self.pride.getSize() < const.MAX_PRIDE:

                    offspring1 = self.__class__(
                        cell = self.cell
                    )
                    offspring1.socialAttitude = self.socialAttitude
                    offspring1.energy = self.energy / 2
                    offspring1.lifetime = self.lifetime

                    offspring1.join_pride(self.pride)
                    #print(offspring1.pride)
                    self.cell.inhabitants.add(offspring1)

                else:
                    neighboring_cells = neighborhood_cells(self.cell.grid, self.cell, radius = const.OFFSPRING_RADIUS)
                    target_cell = random.choice(neighboring_cells)

                    if target_cell != self.cell:
                        offspring1 = self.__class__(
                            cell = target_cell
                        )
                        offspring1.socialAttitude = self.socialAttitude
                        offspring1.energy = self.energy / 2
                        offspring1.lifetime = self.lifetime

                        newPride = Pride()
                        newPride.cell = target_cell
                        target_cell.prides.append(newPride)
                        
                        offspring1.join_pride(newPride)
                        #print(offspring1.pride)
                        target_cell.inhabitants.add(offspring1)

                        # we spawn both offsprings in the same cell to avoid overpopulation
                        offspring2 = self.__class__(
                            cell = target_cell
                        )
                        offspring2.socialAttitude = self.socialAttitude
                        offspring2.energy = self.energy / 2
                        offspring2.lifetime = self.lifetime
                        
                        offspring2.join_pride(newPride)
                        #print(offspring2.pride)
                        target_cell.inhabitants.add(offspring2)

                        return

                """ Offspring 2 """
                if self.pride.getSize() < const.MAX_PRIDE:

                    offspring2 = self.__class__(
                        cell = self.cell
                    )
                    offspring2.socialAttitude = self.socialAttitude
                    offspring2.energy = self.energy / 2
                    offspring2.lifetime = self.lifetime

                    offspring2.join_pride(self.pride)
                    #print(offspring2.pride)
                    self.cell.inhabitants.add(offspring2)

                else:
                    neighboring_cells = neighborhood_cells(self.cell.grid, self.cell, radius = const.OFFSPRING_RADIUS)
                    target_cell = random.choice(neighboring_cells)

                    if target_cell != self.cell:
                        offspring2 = self.__class__(
                            cell = target_cell
                        )
                        offspring2.socialAttitude = self.socialAttitude
                        offspring2.energy = self.energy / 2
                        offspring2.lifetime = self.lifetime

                        newPride = Pride()
                        newPride.cell = target_cell
                        target_cell.prides.append(newPride)
                        
                        offspring2.join_pride(newPride)
                        #print(offspring2.pride)
                        target_cell.inhabitants.add(offspring2)

    def moves(self):
        self.decrease_energy(2)
        self.moved = True


class Erbast(Animals):
    def __init__(self, cell):
        super().__init__(cell)
        self.herd = None

    def eat_vegetob(self, vegetob_available):
        # the Erbast eats the biggest amount of Vegetob to reach maximum energy (100)
        amount_needed = max(0, 100 - self.energy)

        # limit the consumption to the available vegetob
        amount_needed = min(amount_needed, vegetob_available)
        energy_gain = self.cell.vegetob.consume(amount_needed)
        self.energy += energy_gain

    def join_herd(self, herd):    
        if herd.add_member(self): 
            if self.herd is not None:
                self.herd.remove_member(self)
            self.herd = herd
            self.cell = herd.cell

    def leave_herd(self, herd):
        herd.remove_member(self)
        self.herd = None

    def should_move_Erbast(self):

        if self.energy < 3 or self.moved == True:
            return False

        probability_of_moving = 0.3

        # increase probability if energy is low and vegetob's density is also low
        if self.energy < 20:
            if self.cell.get_vegetob_amount() < 20:
                probability_of_moving += 0.6

            elif self.cell.get_vegetob_amount() > 50:
                probability_of_moving -= 0.5
   
        # increase probability if energy is low and vegetob's density is also low
        if self.cell.get_vegetob_amount() > 60:
            probability_of_moving -= 0.3

        # increase probability of moving if energy is high and there is a better cell for movement
        neighboring_cells = neighborhood_cells(self.cell.grid, self.cell)
        
        if self.energy > 80 and herd_cell_choice(neighboring_cells, self.cell) != self.cell:
            probability_of_moving += 0.5

        # increase probability of moving if a Carviz is present
        carviz_present = any(isinstance(animal, Carviz) for animal in self.cell.inhabitants)

        if carviz_present:
            probability_of_moving += 1

        probability_of_moving = max(0, min(probability_of_moving, 1))

        #return probability_of_moving
        return random.random() < probability_of_moving


class Carviz(Animals):
    def __init__(self, cell):
        super().__init__(cell)
        self.pride = None

    def should_move_Carviz(self):
        erbast_present = any(isinstance(animal, Erbast) and not animal.dead for animal in self.cell.inhabitants)

        if erbast_present or self.moved == True:
            return False
        else:
            return True
    
    def join_pride(self, pride): 
        if pride.add_member(self):

            if self.pride is not None:
                self.pride.remove_member(self)
                
            self.pride = pride
            self.cell = pride.cell

    def leave_pride(self, pride):
        pride.remove_member(self)
        self.pride = None