# Berries are nutritious creatures that divide and grow

# Import the general Creature functionality
# The single dot means that the creature module is in the same directory as this file 
from .creature import *
from .actions.interaction import Interaction

# Create an empty list of Gnubs
berries = []
count_berries = 100

class Berry(Creature):
    """A nutritious creature"""
    global count_berries

    def __init__(self):
        '''Called when your creature is created.  Set up the creature here'''

        # Intialise the Creature class
        super().__init__()

        # Load the creature image
        self.setImage('creatures/berry.png')

    def tick(self):
        global count_berries

        if self.status=="asleep" and self.alertness < 100:
            # If we were asleep, keep sleeping until fully alert
            action = "sleep"

        elif self.alertness < 10:
            # If we are tired, go to sleep
            action = "sleep"        

        elif randint(0,100)==0 and count_berries<150:
            action = "divide"
            count_berries += 1
        
        else:
            # Otherwise keep still
            action = "still"

        return action


    def create(self):
        baby = Berry()
        berries.append(baby)
        return baby
        

    def interact(self, other_creature_data):
        '''Interact with another creature'''

        if other_creature_data.type=="Sun":
            self.say("*")
            return Interaction("eat")

    def dying(self):
        '''Called when the creature is dying'''
        global count_berries

        count_berries -= 1       


def start():
    '''Called when the World starts.  Write your code to create the creatures here.'''

    # Create a bunch of berries
    for i in range(count_berries):
        berries.append(Berry())

    # Return them to the world
    return berries
