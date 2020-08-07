# The sun
from .creature import *

class Sun(Creature):
    """An energy store"""

    def __init__(self):
        '''Called when your creature is created.  Set up the creature here'''

        # Intialise the Creature class
        super().__init__()

        # Load the creature image
        self.setImage('creatures/sun.png')

        self.velocity = Vector2(10,10)
        self.max_velocity = 5    # maximum speed of the creature in pixels per tick
        self.acceleration = 1    # acceleration in pixels per tick per tick



    def tick(self):
        """Called on each tick of the World clock"""

        # Take action if we reach the edge of the world
        if self.position.x <= WORLD_LEFT+self.rect.w/2:
            self.angle = randint(270,450)
        elif self.position.x > WORLD_RIGHT-self.rect.w/2:
            self.angle = randint(90,270)
        elif self.position.y <= WORLD_TOP+self.rect.h/2:
            self.angle = randint(180,359)
        elif self.position.y >= WORLD_BOTTOM-self.rect.h/2:
            self.angle = randint(0,180)    

        if self.angle<0:
            self.angle += 360

        #print(self.angle)  

        return "move"

def start():
    '''Called when the World starts.  Write your code to create the creatures here.'''

    # Return a sun
    return [Sun()]
