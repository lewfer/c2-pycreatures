"""
    Py Creatures, a virtual world for teaching intermediate Python skills

    Copyright (C) 2020  Llewelyn Fernandes, Think Create Learn

    This file is part of Py Creatures.

    Py Creatures is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""    

# world.py
# 
# Represents the world in which creatures live.  

# Pygame will handle the graphics for us
import pygame
from pygame.math import Vector2

# Module to write to our log file
import pycreatures_logging as log

# Modules for file and directory handling
from os import listdir
import importlib
from pathlib import Path, PurePath
from copy import copy
import csv

# Random number generation
from random import randint, random

# Creatures
from creatures.creature import Creature
from creature_data import CreatureData
from battle_result import BattleResult
from creatures.actions.interaction import Interaction

from creatures.sun import Sun


# General settings
from settings import *


class World():
    """ The world in which creatures live.  Provides functionality for drawing the world, 
        managing the life and health of creatures, managing creature interactions.
        Note that some of the methods here would, by best object-orientation practice, 
        normally be part of the Creature class, but they are kept here to prevent the 
        student from overriding them. """

    def __init__(self):
        '''Setup the world'''

        # Initialise Pygame
        pygame.init()
        
        # Set up display
        self.__display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption('Py Creatures')

        # Track time
        self.__clock = pygame.time.Clock()
        self.__startTime = pygame.time.get_ticks() 

        # List of creature modules
        self.__modules = []

        # Create a list of actual creatures in the world
        # Uses a sprite group to hold live creatures:
        # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group.add
        self.__creatures = pygame.sprite.Group()

        # Create the sun
        self.__sun = Sun()

        # Load all the modules for the creatures
        self.__loadCreatureModules()

        # Create the intial creatures in the world
        self.__createInitialCreatures()       

        # Start the clock ticking
        self.__tickCount = 0 

        # Our general font
        self.__font = pygame.font.SysFont(None, 25)
        self.__bold_font = pygame.font.SysFont(None, 25, bold=True)
        self.__italic_font = pygame.font.SysFont(None, 25, italic=True)
        self.__header_font = pygame.font.SysFont(None, 45)

        # Energy absorbed from creature activity
        #self.__floating_energy = 0

        # !!
        self.walls = []
        self.walls.append({"colour":BLACK, "rect":[200,200, 300,10]})
        self.walls.append({"colour":BLACK, "rect":[200,200, 10,300]})



    def run(self):
        '''Run the world.  Contains our main Pygame loop.'''

        # Will change to True when we quit the game
        game_exit = False

        # Create a csv file for recording the history of what happened
        with open('pycreatures_history.csv', mode='w', newline='') as csvfile:
            self.__history = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.__writeHistoryHeader()


            # List of sprites that have been clicked on (should be 0 or 1 sprite)
            clicked_sprites = []

            # Enter the Pygame main loop
            while not game_exit:

                # Handle Pygame events
                for event in pygame.event.get():
                    # Quit request?
                    if event.type == pygame.QUIT:
                        game_exit = True

                    # Mouse click?
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Find sprites clicked on
                        click_pos = pygame.mouse.get_pos()
                        clicked_sprites = [s for s in self.__creatures if s.rect.collidepoint(click_pos)]

                # Handle dying creatures
                for creature in self.__creatures:
                    if creature.status == "dead":            
                        # Give up energy to the sun
                        self.__transferEnergy(creature, self.__sun, creature.energy)
                        #self.__creatures.remove(creature) # remove just removes from group
                        creature.kill()
                    if creature.status == "dying":
                        # Notify the creature that they are dying
                        creature.status = "dead"
                        creature.dying()

                # The sun never gets tired or damaged
                self.__sun.alertness = INITIAL_ALERTNESS
                self.__sun.damage = 0

                # Draw the main window
                self.__drawWindow(clicked_sprites)

                # Draw the creatures
                self.__creatures.draw(self.__display)

                # Call tick() on all creatures
                self.__tick()
                self.__tickCount += 1

                # Call update() on all creatures
                self.__creatures.update(False)

                # Update the display
                pygame.display.update()
                self.__clock.tick(FPS)

        pygame.quit()            


    # ---------------------------------------------------------------------------------------------
    # Setup
    #
    # Methods used to set up the creatures in the world.
    # ---------------------------------------------------------------------------------------------
 
    def __loadCreatureModules(self):
        '''Load all the modules in the creatures directory'''

        # Get all .py files in the creatures directory
        for creatures_file_name in(Path.cwd() / 'creatures' ).glob('*.py'):
            creature_name = PurePath(creatures_file_name).stem

            # Import each creature (ignoring creature.py)
            if creature_name != 'creature' and creature_name != 'sun' and not creature_name.startswith("#"):
                try:
                    module = importlib.import_module("creatures." + str(creature_name))
                    self.__modules.append(module)
                except Exception as e:
                    print("Failed to load module " + creature_name + " " + str(e))
                    log.logException("Failed to load module " + creature_name)


    def __createInitialCreatures(self):
        '''Create the initial set of creatures'''

        # Create the sun
        self.__creatures.add(self.__sun)

        # Foe each module, call the start() method to get the initial creatures
        for module in self.__modules:
            try:
                # Get the initial creatures from the module
                creatures = module.start()

                # Add them to the list of all creatures
                if isinstance (creatures, list): 
                    # start() returned a list of creatures

                    # Go through the list, adding each creature
                    for creature in creatures:
                        if isinstance (creature, Creature):
                            self.__creatures.add(creature)
                        else:
                            raise Exception(str(module) + "returned non creatures in start()")                      
                elif  isinstance (creatures, Creature): 
                    # start() returned a single creature

                    # Add the creature
                    self.__creatures.add(creatures)

                else:
                    raise Exception(str(module) + "returned non creatures in start()")
            except Exception as e:
                print("Failed to start " + str(module) + str(e))
                log.logException("Failed to start "+ str(module))

        # Now set the intial health data for the creatures created
        data = CreatureData()
        for creature in self.__creatures:
            creature.setData(data)


    # ---------------------------------------------------------------------------------------------
    # Drawing the World
    #
    # Methods to draw the window and info panel.
    # ---------------------------------------------------------------------------------------------


    def __drawWindow(self, clicked_sprites):
        '''Draw the main window'''

        # Background colour
        self.__display.fill(BLACK)

        # The world view itself (where the creatures live)
        pygame.draw.rect(self.__display, WORLD_COLOUR, [PADDING, PADDING, WORLD_WIDTH, WORLD_HEIGHT])

        # !! wall
        #for wall in self.walls:
        #    pygame.draw.rect(self.__display, wall.colour, wall.rect)

        # The info on the side
        y = INFO_PANEL_TOP
        y = self.__textAt("Py Creatures", INFO_PANEL_LEFT, y, self.__header_font)
        y += self.__font.get_height()  # Blank line

        y = self.__showTime(y)
        y = self.__showMousePos(y)       
        y += self.__font.get_height()  # Blank line
        y = self.__showCreatureSummary(y)
        y += self.__font.get_height()  # Blank line
        y = self.__showClickedCreature(clicked_sprites, y)


    def __showTime(self, y):
        '''Show the passage of time'''

        # Calculate number of milliseconds since start of game
        milliseconds = pygame.time.get_ticks() - self.__startTime
        seconds = round(milliseconds/1000)

        # Draw the time text
        y = self.__textAt("Time: "+str(seconds), INFO_PANEL_LEFT, y, self.__font)

        return y


    def __showMousePos(self, y):
        '''Show the mouse position'''

        # Get the mouse position
        pos = pygame.mouse.get_pos()

        # Draw the mouse position text
        y = self.__textAt("Mouse: "+str(pos), INFO_PANEL_LEFT, y, self.__font)

        return y


    def __showCreatureSummary(self, y):
        
        y = self.__textAt("Creatures:", INFO_PANEL_LEFT, y, self.__bold_font)

        summary = {}
        for creature in self.__creatures:
            if creature.type not in summary:
                summary[creature.type] = {}
                summary[creature.type]["count"] = 1
                summary[creature.type]["energy"] = creature.energy
            else:
                summary[creature.type]["count"] += 1
                summary[creature.type]["energy"] += creature.energy

        total_world_enery = 0 #self.__floating_energy
        
        for type, details in summary.items():
            text = "{0}: num={1} energy={2}".format(type, int(summary[type]["count"]), int(summary[type]["energy"]))
            y = self.__textAt(text, INFO_PANEL_LEFT, y, self.__font)
            total_world_enery += summary[type]["energy"]
        
        y = self.__textAt("World energy: " + str(int(total_world_enery)), INFO_PANEL_LEFT, y, self.__font)

        return y


    def __showClickedCreature(self, clicked_sprites, y):
        '''Show info about the creature clicked on'''
        
        # Clicked on a creature?
        if len(clicked_sprites)==0:
            return y

        # Just take the first one
        sprite = clicked_sprites[0]

        y = self.__textAt("Highlighted:",                                     INFO_PANEL_LEFT, y, self.__bold_font)

        # Draw the sprite info
        y = self.__textAt("Highlighted creature:",                            INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt(sprite.type,                                        INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Id="+str(sprite.id),                               INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Size="+str(sprite.size),                           INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Age="+str(round(sprite.age)),                      INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Alertness="+str(round(sprite.alertness)),          INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Damage="+str(round(sprite.damage)),                INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Energy="+str(round(sprite.energy)),                INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Battle power="+str(round(sprite.battlePower())),   INFO_PANEL_LEFT, y, self.__font)
        y = self.__textAt("Status="+sprite.status,                            INFO_PANEL_LEFT, y, self.__font)
        if sprite.last_action is not None:
            y = self.__textAt("Last action="+sprite.last_action,                  INFO_PANEL_LEFT, y, self.__font)
        if sprite.last_interaction is not None:
            y = self.__textAt("Last interaction="+sprite.last_interaction.action, INFO_PANEL_LEFT, y, self.__font)
        
        # Highlight it so we know which one was clicked on
        sprite.highlight = True

        return y



    def __textAt(self, text, x, y, font):
        '''Show text at the given coordinate'''

        text = font.render(text, True, WHITE)
        self.__display.blit(text,(x, y))
        y += font.get_height() - self.__font.get_descent()
        return y



    # ---------------------------------------------------------------------------------------------
    # Tick handling
    #
    # A tick is a single unit of time.  On each tick we need to get each creature to decide on its
    # "tick action" and then the World needs to handle this action.
    # ---------------------------------------------------------------------------------------------
    
    def __tick(self):
        '''Run one iteration of the world'''

        # Go through each creature
        for creature in self.__creatures:

            # Don't tick for dead creatures
            if creature.status not in ["awake","asleep"]:
                continue

            # Default interaction is to ignore
            interaction =  Interaction("ignore")

            # Handle interactions between creatures that collided
            all_except = [s for s in self.__creatures if s != creature]
            collisions = pygame.sprite.spritecollide(creature, all_except, False)       # Check if there are collisions with anything except the sprite itself
            if len(collisions)>0:
                for other_creature in collisions:
                    if other_creature.status in ["awake","asleep"]:
                        # Handle the interaction
                        self.__handleCollision(creature, other_creature)

            # Tell the creature that time has passed and get its desired tick action
            tickAction = None
            data = creature.getData()       # take a copy of the data in case student cheats
            try:
                tickAction = creature.tickHandler()
            except Exception as e:
                print("Exception in " + creature.type + ".tick() " + str(e))
                log.logException("Exception in " + creature.type + ".tick()")
            creature.setData(data)          # put data back

            # Carry out the tick action
            if tickAction is not None:
                self.__doTickAction(creature, tickAction)      

            # Kill anything that goes off screen
            if creature.rect.centerx < PADDING or creature.rect.centerx > WORLD_WIDTH+PADDING or creature.rect.centery < PADDING or creature.rect.centery > WORLD_HEIGHT+PADDING:
                #print("Dropped off world ", creature)
                creature.status = "dying"
                #self.__creatures.remove(creature)

                if LOG_DIED: self.__writeHistory(creature, "died", "", 0, 0, 0, "Fell off edge", None)           

            # Update time-based health
            creature.age += TICK_AGE_INCREASE
            creature.alertness -= TICK_ALERTNESS_REDUCTION
            self.__transferEnergy(from_creature=creature, to_creature=self.__sun, amount=TICK_ENERGY_REDUCTION)

            # Work out if creature has died
            if creature.damage >= creature.size:
                #print("Too much damage ", creature)
                creature.status = "dying"

                if LOG_DIED: self.__writeHistory(creature, "died", "", 0, 0, 0, "Too much damage", None)                   
                #self.__creatures.remove(creature)

            elif creature.energy <=0:
                #print("Out of energy ", creature)
                creature.status = "dying"
                #self.__creatures.remove(creature)
                if LOG_DIED: self.__writeHistory(creature, "died", "", 0, 0, 0, "Out of energy", None) 
            

    def __doTickAction(self, creature, action):
        '''Perform the action'''

        if action is None or action == "still":
            self.__still(creature)

        elif action == "move":
            self.__move(creature)

        elif action == "sleep":
            self.__sleep(creature)

        elif action == "divide":
            self.__divide(creature)

        else:
            print(creature.type, "cannot perform action", action, "during tick")


    def __still(self, creature):
        '''Creature wants to keep still'''

        creature.status = "awake"


    def __move(self, creature):
        '''Move'''
        
        creature.move()

        # Adjust energy based on velocity   
        energy_loss1 = creature.velocity.magnitude() * VELOCITY_MOVEMENT_ENERGY_LOSS_MULTIPLIER
        self.__transferEnergy(from_creature=creature, to_creature=self.__sun, amount=energy_loss1)

        # Adjust energy based on weapons and defence
        energy_loss2 = creature.battlePower() * BATTLE_POWER_MOVEMENT_ENERGY_LOSS_MULTIPLIER
        self.__transferEnergy(from_creature=creature, to_creature=self.__sun, amount=energy_loss2)

        creature.status = "awake"

        # Log the action
        if LOG_MOVE: self.__writeHistory(creature, "move", "", 0, energy_loss1+energy_loss2, 0, "moved", None)        


    def __sleep(self, creature):
        '''Sleep'''

        creature.alertness += SLEEP_ALERTNESS_INCREASE

        creature.status = "asleep"

        # Log the action
        if LOG_SLEEP: self.__writeHistory(creature, "sleep", "", SLEEP_ALERTNESS_INCREASE, 0, 0, "slept", None)


    def __divide(self, creature):
        '''Divide in two'''

        # Check if creature is responsive
        if not self.__isResponsive(creature):
            return           

        # Reduce energy from dividing
        energy_loss = creature.size * MATE_ATTEMPT_ENERGY_MULTIPLIER
        self.__transferEnergy(creature, self.__sun, energy_loss)

        new_creature = creature.createHandler()
        self.__creatures.add(new_creature)
        new_creature.energy = 0

        # Transfer half energy from parent to new creature
        self.__transferEnergy(from_creature=creature, to_creature=new_creature, amount=creature.energy / 2)

        # Log the action
        if LOG_DIVIDE: self.__writeHistory(creature, "divide", "", 0, energy_loss, 0, "divided", None)
    


    # ---------------------------------------------------------------------------------------------
    # Collision handling
    #
    # A collision is a meeting of creatures.  When creatures meet they can decide what they want to
    # do.  The World then executes the creature's wishes within the rules of the game.
    # ---------------------------------------------------------------------------------------------
    
    def __handleCollision(self, main_creature, other_creature):
        '''Deal with collision between creatures'''

        # Check if creature is responsive
        if not self.__isResponsive(main_creature):
            return             

        # Main creature to make first move
        data = main_creature.getData()                                                               # take a copy of the data in case student cheats
        main_action = main_creature.interactHandler(copy(other_creature.getData()))                  # give create a copy of opponent's data (so they can't change it)
        if main_action is None: main_action = Interaction("ignore")
        main_creature.setData(data)                                                                  # put data back
        
        if main_action.action == "attack" or main_action.action == "mate":
            # Allow other creature to respond            
            data = other_creature.getData()                                                              # take a copy of the data in case student cheats
            other_action = other_creature.responseHandler(copy(main_creature.getData()), main_action)    # give create a copy of opponent's data (so they can't change it)
            if other_action is None: other_action = Interaction("ignore")
            other_creature.setData(data)                                                                 # put data back

        if main_action.action == "ignore":
            pass 

        elif main_action.action == "mate":
            self.__mate(main_creature, other_creature, other_action)

        elif main_action.action == "eat":
            self.__eat(main_creature, other_creature)

        elif main_action.action == "attack":    
            self.__attack(main_creature, main_action, other_creature, other_action)

        elif main_action.action == "defend":
            self.__defend(main_creature, main_action, other_creature)
            pass # defence only comes into play in response to an attack



    def __isResponsive(self, creature):
        '''Check if creature is responsive.  Encodes whatever rules we want on alertness, sleepiness, etc'''

        # Chances of just doing nothing increase as alertness decreases
        if randint(0, INITIAL_ALERTNESS) > creature.alertness :
            return False # do nothing

        # Can't do anything if we are asleep
        if creature.status == "asleep":
            return False # do nothing      

        return True     


    def __defend(self, defender, action, other_creature):
        '''A pointless defence'''

        defence = defender.defence[action.details]
        energy_loss = defence.power * BATTLE_POWER_ENERGY_LOSS_MULTIPLIER

        self.__transferEnergy(defender, self.__sun, energy_loss)

        if LOG_ATTACK: 
            self.__writeHistory(defender, "defend", defence.type, 0, energy_loss, 0, "pointless defence", other_creature)


    def __mate(self, parent1, parent2, parent2_action):
        '''Make offspring'''

        # Reduce energy from mating attempt
        energy_loss = parent1.size * MATE_ATTEMPT_ENERGY_MULTIPLIER
        self.__transferEnergy(parent1, self.__sun, energy_loss)

        # Other creature wants to mate?
        if parent2_action.action == "mate":
            if randint(0,10) == 5: #only 1 in 10 change of success
                baby = parent1.createHandler()
                self.__creatures.add(baby)
                baby.energy = 0

                # Transfer energy of main parent to baby
                energy_loss1 =  parent1.energy * MATE_ENERGY_TRANSFER_MULTIPLIER
                self.__transferEnergy(parent1, baby, energy_loss1)

                # Transfer energy of other parent to baby
                energy_loss2 =  parent2.energy * MATE_ENERGY_TRANSFER_MULTIPLIER
                self.__transferEnergy(parent2, baby, energy_loss2)  

                # Write to history file
                if LOG_MATE:
                    self.__writeHistory(parent1, "mate", "", 0, energy_loss + energy_loss1, 0, "mated", parent2)
                    self.__writeHistory(parent2, "mate response", "", 0, energy_loss2, 0, "mated", parent1)
                  

    def __eat(self, eater, eaten):
        '''Eat'''

        # Have to stop to eat (unless it's the sun being eaten)
        if eaten.type != "Sun":
            eater.velocity = Vector2(0.0, 0.0) 

        # Can only bite off as much of the bitten as is available
        bite_size = min(eater.bite_size, eaten.size-eaten.damage)

        # Energy transfers from bitten to biter
        self.__transferEnergy(eaten, eater, bite_size)

        # Damage done to bitten
        eaten.damage += bite_size

        # Work out if any creature died
        eaten_will_die = False
        if eaten.damage >= eaten.size:
            eaten_will_die = True

        # Log result
        if LOG_EAT:
            self.__writeHistory(eater, "eat", "", 0, +bite_size, 0, "ate", eaten)
            self.__writeHistory(eaten, "", "", 0, -bite_size, bite_size, "eaten by", eater)                          


    def __attack(self, attacker,  attacker_action, defender, defender_action):
        '''Creature lauches attack'''

        # Attempts to attack the sun end in instant death by complete energy loss
        if defender.type == "Sun":
            self.__transferEnergy(attacker, self.__sun, attacker.energy)
            
            # Log attacker action
            self.__writeHistory(attacker, attacker_action.action, attacker_action.details, 0, attacker.energy, 0, "total energy drain", defender)   

        else:

            #print("Battle:", main_creature, main_action, other_creature, other_action)

            # Intialise battle result to "no changes"
            battle_result = BattleResult(0,0,0,0)

            # Handle main creature's action
            battle_result = self.__battle(attacker, attacker_action, defender, defender_action)

            # Apply result of the battle damage
            attacker.damage += battle_result.mainDamageChange
            defender.damage += battle_result.otherDamageChange

            # Transfer energy
            self.__transferEnergy(attacker, self.__sun, -battle_result.mainEnergyChange)
            self.__transferEnergy(defender, self.__sun, -battle_result.otherEnergyChange)
            
            # Battles always reduce alertness
            attacker.alertness -= 1      
            defender.alertness -= 1

            if LOG_ATTACK:
                # Log attacker action
                self.__writeHistory(attacker, attacker_action.action, attacker_action.details, 0, battle_result.mainEnergyChange, battle_result.mainDamageChange, "attacked", defender)   

                # Log defender action
                defender_action_action = "defend response" if defender_action.action=="defend" else ""
                defender_action_action_details = defender_action.details if defender_action.action=="defend" else ""
                self.__writeHistory(defender, defender_action_action, defender_action_action_details, 0, battle_result.otherEnergyChange, battle_result.otherDamageChange, "attacked by", attacker)                  


    def __battle(self, attacker, attacker_action, victim, victim_action):
        '''Handle an attack'''
        #print("Attack {0} ({1}) -> {2} ({3})".format(attacker, attackerAction, victim, victimAction))

        # Have to stop to attack or defend yourself
        attacker.velocity = Vector2(0.0, 0.0)
        victim.velocity = Vector2(0.0, 0.0)

        # Get the attacker's weapon
        weapon = attacker.weapons[attacker_action.details]

        # By default assume no defence
        has_effective_defence = False

        # See what sort of defence is put up in response to the weapon
        if victim_action.action == "defend":
            defence = victim.defence[victim_action.details]

            # Check if type of defence is effective against the type of weapon
            if weapon.type == "claw" or weapon.type == "jaws":
                if defence.type == "shell":
                    has_effective_defence = True

            elif weapon.type == "poison" or weapon.type == "venom":
                if defence.type == "antivenom":
                    has_effective_defence = True

        # Work out the maximum potential damage
        if has_effective_defence:
            # If victim has an effective defence, reduce the damage accordingly
            damage = max(0, weapon.power - defence.power)
        else:
            # If the victim has no defence their damage is the full power of the attack
            damage = weapon.power

        # Work out the actual damage by applying a minimum and random factor
        damage = int(damage * min(MIN_BATTLE_DAMAGE_MULTIPLIER, random()))

        # Subtract energy used for attack/defence
        attacker_energy_loss = weapon.power * BATTLE_POWER_ENERGY_LOSS_MULTIPLIER
        victim_energy_loss = 0
        if victim_action.action == "defend":
             victim_energy_loss = defence.power * BATTLE_POWER_ENERGY_LOSS_MULTIPLIER

        #print("\tAttack result: {1} damage={2}, {0} EnergyLoss={3}, {1} EnergyLoss={4}".format(attacker.type, victim.type, damage, attackerEnergyLoss, victimEnergyLoss))

        #print("attack\t{0}\t".format(self.__tickCount, attacker.type, attacker.id, attacker.age, attacker.alertness, attacker.energy, attacker.damage, attackerEnergyLoss, 0))
        #print("attacked\t{0}\t".format(self.__tickCount, victim.type, victim.id, victim.age, victom.alertness, victim.energy, victim.damage, victimEnergyLoss, damage))

        return BattleResult(mainEnergyChange=-attacker_energy_loss, mainDamageChange=0, otherEnergyChange=-victim_energy_loss, otherDamageChange=damage)


    # ---------------------------------------------------------------------------------------------
    # Utility functions
    # ---------------------------------------------------------------------------------------------
    
    def __transferEnergy(self, from_creature, to_creature, amount):
        '''Transfer energy from one creature to another'''

        from_creature.energy -= amount
        to_creature.energy += amount


    def __writeHistoryHeader(self):
        '''Write the header row for the history file'''

        self.__history.writerow([
                        "tick", 
                        "Type", "id",
                        "Action", "Action Details", 
                        "Age", "Alertness", "Energy", "Damage", 
                        "Alertness Change", "Energy Change", "Damage Change", 
                        "Result",  

                        "Direction",

                        "Other Type", "Other id"])        


    def __writeHistory(self, creature, action, action_details, alertness_change, energy_change, damage_change, result, other_creature):
        '''Write a data row to the history file'''

        if "All" in LOG_INCLUDE or creature.type in LOG_INCLUDE:
            if creature.type not in LOG_EXCLUDE:
                # If there is another creature involved, get its details
                if other_creature is None:
                    other_creature_type = ""
                    other_creature_id = ""
                else:
                    other_creature_type = other_creature.type
                    other_creature_id = other_creature.id

                # Write to the csv file
                self.__history.writerow([
                                    self.__tickCount, 
                                    creature.type, creature.id, 
                                    action, action_details, 
                                    creature.age, creature.alertness, creature.energy, creature.damage, 
                                    alertness_change, energy_change, damage_change,  
                                    result, "->" if other_creature is not None else "",
                                    other_creature_type, other_creature_id])         