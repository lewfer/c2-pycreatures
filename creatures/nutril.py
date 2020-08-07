# Gnubs are the most basic creature
# They don't move, eat fight or reproduce
# They will inevitably die out

# Import the general Creature functionality
# The single dot means that the creature module is in the same directory as this file 
from .creature import *
from .actions.interaction import Interaction

# Create an empty list of Gnubs
nutrils = []

class Nutril(Creature):
    """A nutritious creature"""

    def __init__(self):
        '''Called when your creature is created.  Set up the creature here'''

        # Intialise the Creature class
        super().__init__()

        # Load the creature image
        self.setImage('creatures/nutril.png')

    def tick(self):

        if self.status=="asleep" and self.alertness < 100:
            # If we were asleep, keep sleeping until fully alert
            action = "sleep"

        elif self.alertness < 10:
            # If we are tired, go to sleep
            action = "sleep"        
        
        else:
            # Otherwise keep still
            action = "still"

        return action


    def create(self):
        baby = Nutril()
        nutrils.append(baby)
        return baby


    def interact(self, other_creature_data):
        '''Interact with another creature'''

        if other_creature_data.type=="Nutril":
            if self.age > 20:
                return Interaction ("mate")
        elif other_creature_data.type=="Sun":
            self.say("*")
            return Interaction("eat")


    def respond(self, other_creature_data, other_creature_action):
        '''Respond to another creature's interaction''' 

        if other_creature_data.type=="Nutril":
            if self.age > 20:
                return Interaction ("mate")        


def start():
    '''Called when the World starts.  Write your code to create the creatures here.'''

    # Create a bunch of nutrils
    for i in range(100):
        nutrils.append(Nutril())

    # Return them to the world
    return nutrils
