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

        return "move"


def start():
    """Called when the World starts.  Write your code to create the creatures here."""

    # Create a bunch of Fleebs
    for i in range(0):
        fleebs.append(Fleeb())
    return fleebs
