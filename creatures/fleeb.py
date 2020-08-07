# Fleebs are quite basic
# They move slowly in straight lines and bounce off the edge of the world
# They will try to eat anything they see
# They won't fight.  They will try to mate with any other fleeb they encounter.

from .creature import *
from .actions.interaction import Interaction

# Create an empty list of Fleebs
fleebs = []

class Fleeb(Creature):
    """A simple, peaceful creature"""

    def __init__(self):
        """Called when your creature is created.  Set up the creature here"""

        super().__init__()

        # Load the creature image
        self.setImage('creatures/fleeb.png')

    def tick(self):
        """Called on each tick of the World clock"""

        # Update properties
        #self.steering = 0        # steering in degrees, positive is left, negative is right
        self.max_velocity = 5    # maximum speed of the creature in pixels per tick
        self.acceleration = 2    # acceleration in pixels per tick per tick

        # Take action if we reach the edge of the world
        if self.position.x <= WORLD_LEFT+20:
            self.angle = 0
        elif self.position.x > WORLD_RIGHT-20:
            self.angle = 180
        elif self.position.y <= WORLD_TOP+20:
            self.angle = 270
        elif self.position.y >= WORLD_BOTTOM-20:
            self.angle = 90       

        # Tell the creature to sleep or move
        if self.alertness < 10:
            action = "sleep"
        else:
            action = "move"

        return action


    def interact(self, other_creature_data):
        '''Interact with another creature'''

        if other_creature_data.type=="Fleeb":
            self.say = "hello"
        else:
            return Interaction("eat")


def start():
    """Called when the World starts.  Write your code to create the creatures here."""

    # Create a bunch of Fleebs
    for i in range(0):
        fleebs.append(Fleeb())
    return fleebs
