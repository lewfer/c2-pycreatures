# Gnubs are the most basic creature
# They don't move, eat, fight or reproduce
# They will inevitably die out

# Import the general Creature functionality
# The single dot means that the creature module is in the same directory as this file 
from .creature import *

# Create an empty list of Gnubs
gnubs = []

class Gnub(Creature):
    """A most simple creature"""

    def __init__(self):
        '''Called when your creature is created.  Set up the creature here'''

        # Intialise the Creature class
        super().__init__()

        # Load the creature image
        self.setImage('creatures/gnub.png')


def start():
    '''Called when the World starts.  Write your code to create the creatures here.'''

    # Create a bunch of gnubs
    for i in range(0):
        gnubs.append(Gnub())

    # Return them to the world
    return gnubs
