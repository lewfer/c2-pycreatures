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

# Creature.py
#
# The base class for a creature

# Pygame will handle the graphics for us
import pygame
from pygame.math import Vector2

# A bit of maths required
from math import sin, radians, degrees, copysign
from random import randint

#from abc import ABC, abstractmethod

# Creatures
from creature_data import CreatureData

# General settings
from settings import *


class Creature(pygame.sprite.Sprite): #, ABC):
    """The base class for all creatures.  Creature itself is based on a Pygame sprite.
       This means we can get Pygame to draw and manage our creatures."""

    def __init__(self):
        '''Set up the creature'''

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Current X and Y coordinates of the creature
        self.position = Vector2(randint(PADDING,WORLD_WIDTH+PADDING), randint(PADDING,WORLD_HEIGHT+PADDING))        

        # Current angle of rotation - 0 means going right, 90 up 180 left, 270 down
        self.angle = randint(0,360)
        
        # Current speed of the creature in pixels per tick
        self.velocity = Vector2(0.0, 0.0)

        # Current acceleration in pixels per tick per tick
        self.acceleration = 1

        # Current steering in degrees.  Positive is left, negative is right
        self.steering = 0.0
        
        # Maximum allowable acceleration in pixels per tick per tick
        self.max_acceleration = 30

        # Maximum steering in degrees
        self.max_steering = 5

        # Maximum velocity in pixels per frame
        self.max_velocity = 1

        # Battle devices
        self.weapons = {}
        self.defence = {}

        # Flag to indicate if we should fade as health deteriorates
        self.fade = True

        #self.history = []

        # Key creature properties
        # These are managed by the World and will be restored if changed
        self.type = type(self).__name__     # type of creature
        self.id = id(self)                  # unique id of creature
        self.size = 0                       # will be set to the size of the image
        self.age = 0                        # increases with every tick
        self.energy = INITIAL_ENERGY        # increases when you eat, decreases when you move, mate or use weapons.  Movement energy decrease depends on distance, speed and what you are carrying (weapons, armour)
        self.damage = 0                     # amount of damage sustained
        self.alertness = INITIAL_ALERTNESS  # decreases with lack of sleep

        # Message to say when next drawn
        self.say_text = None

        # True if we want to draw a highlight box around the creature
        self.highlight = False

        # Current status of the creature
        self.status = "awake"               # awake, asleep, dying, dead

        self.last_action = None
        self.last_interaction = None


    def __str__(self):
        '''String representation (when you print the Creature)'''

        return type(self).__name__ + ":" + str(self.id)


    def getData(self):
        '''Get the key creature properties and position/movement info'''

        data = CreatureData()
        data.type = self.type
        data.id = self.id
        data.size = self.size
        data.age = self.age
        data.energy = self.energy
        data.damage = self.damage 
        data.alertness = self.alertness
        data.bite_size = self.bite_size

        data.position = self.position
        data.angle = self.angle
        data.velocity = self.velocity
        data.acceleration = self.acceleration

        return data

    def __calculateSize(self):
        '''Calculate the size of the creature'''

        rect = self.originalImage.get_rect()
        self.size = int(rect.w * rect.h)
        self.bite_size = self.size * BITE_SIZE_MULTIPLIER


    def setData(self, data):
        '''Set the key creature properties.  Used to reset the data following a tick to prevent creatures cheating and fixing their status'''

        # Type and size and bit_size
        self.type = type(self).__name__
        self.__calculateSize()

        # Set data relating to health 
        self.age = data.age
        self.energy = data.energy
        self.damage = data.damage 
        self.alertness = data.alertness   

    def say(self, message):
        '''Display the message'''

        self.say_text = message

    def setImage(self, imageFile):
        ''' Set the image displayed for the creature.'''

        # Store original image (rotated to starting orientation)
        self.originalImage = pygame.image.load(imageFile)
        self.originalImage = pygame.transform.rotozoom(self.originalImage, 270, 1)

        # Set current image to original image
        self.image = self.originalImage     

        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

        # Compute size of creature
        self.__calculateSize()

    def tickHandler(self):
        '''Handle tick'''

        # Call subclass 
        result = self.tick()

        self.last_action = result

        return result

    def interactHandler(self, other_creature_data):
        '''Handle interaction with another creature'''

        # Call subclass 
        result = self.interact(other_creature_data)

        self.last_interaction = result

        return result


    def responseHandler(self, other_creature_data, other_creature_action):
        '''Handle response to another creature interaction'''

        # Call subclass 
        result = self.respond(other_creature_data, other_creature_action)

        self.last_interaction = result

        return result


    def createHandler(self):
        '''Create a new creature'''

        # Call subclass to create creature
        baby = self.create()

        # Apply new position, a little bit away from the parent and facing in a random direction
        baby.position = self.position
        dist = baby.rect.w
        baby.position += Vector2(dist,dist).rotate(randint(0,360))
        baby.rect.centerx = baby.position.x
        baby.rect.centery = baby.position.y

        return baby


    def tick(self):
        '''Virtual function - can be implemented by the subclass'''
        pass
    
    def interact(self, other_creature_data):
        '''Virtual function - can be implemented by the subclass'''
        pass

    def respond(self, other_creature_data, other_creature_action):
        '''Virtual function - can be implemented by the subclass'''
        pass

    def draw(self):
        '''Virtual function - can be implemented by the subclass'''
        pass

    def dying(self):
        '''Virtual function - can be implemented by the subclass'''
        pass

    def create(self):
        '''Virtual function - can be implemented by the subclass'''
        pass

    def move(self):
        '''Move the creature.'''

        # See here for details of how this works
        # http://rmgi.blog/pygame-2d-car-tutorial.html

        # Can only move if some alertness
        if self.alertness>0:
            # Amount to move
            dt = 0.5

            # Adjust the velocity based on the acceleration, keeping to the max velocity
            self.velocity += (self.acceleration * dt, 0)
            self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

            # Compute the angular velocity (speed of rotation)
            if self.steering:
                turning_radius = self.rect.height / sin(radians(self.steering))
                angular_velocity = self.velocity.x / turning_radius
            else:
                angular_velocity = 0

            # Use the velocity and angular velocity to compute the new position and angle
            self.position += self.velocity.rotate(-self.angle) * dt
            self.angle += degrees(angular_velocity) * dt      

            #print(self.position, self.angle)      

            # Apply new position
            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y


    def update(self, hide_asleep=False):
        '''Update the creature'''

        # Make a copy of the original image
        img = self.originalImage.copy()

        # Add a fade (alpha) according to the creature health
        # Alpha is from 0 (completely faded) to 255 (not faded)
        alpha = 255
        if self.fade:
            alpha_damage = (self.size-self.damage)*255/self.size                                # compute alpha from the amount of damage
            alpha_energy = 255 if self.energy > FADE_ENERGY else self.energy*255/FADE_ENERGY    # compute alpha from the amount of energy
            alpha = min(alpha_damage, alpha_energy)                                             # set energy to lowest of the above 2
            alpha = max(alpha, MIN_FADE)                                                        # make sure we don't go below MIN_FADE
        #if DEBUG: alpha=30

        if hide_asleep and self.status=="asleep": #!! control through checkbox
            alpha = 0

        img.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)

        # Rotate according to the angle and put the copy back
        self.image = pygame.transform.rotozoom(img, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)            # get the new rect for the image centred where the old rect was

        # If the creature wants to speak, display the text
        if self.say_text is not None:
            font = pygame.font.SysFont(None, 15)
            offset = 0
            self.image.blit(font.render(self.say_text, True, WHITE), (0,offset)) 
            self.say_text = None

        # Call the subclass for any custom drawing
        self.draw()

        # If we want a highlight box around the creature
        if self.highlight:
            pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 2)
            self.highlight = False

        # Debug - draw white rect and text
        if DEBUG:
            #pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 2)
            font = pygame.font.SysFont(None, 15)
            offset = 0
            #self.image.blit(font.render(str(self.id)[-3:], True, WHITE), (0,offset))  
            #offset += 12
            #self.image.blit(font.render(str(self.age), True, pygame.Color("cadetblue")), (0,offset))  
            #offset += 12
            #self.image.blit(font.render(str(self.energy), True, pygame.Color("darkgreen")), (0, offset)) 
            #offset += 12 
            #self.image.blit(font.render(str(self.damage), True, pygame.Color("orangered")), (0,offset))  
            #offset += 12
            self.image.blit(font.render(str(self.alertness), True, pygame.Color("orangered")), (0,offset)) 
            offset += 12

    def battlePower(self):
        '''Sum of power of all weapons and defence mechanisms'''

        power = 0
        for name,weapon in self.weapons.items():
            power += weapon.power
        for name,defence in self.defence.items():
            power += defence.power
        return power