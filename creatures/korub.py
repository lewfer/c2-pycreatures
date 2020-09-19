# Korubs are vicious creatures that will eat or attack anything that gets in their way.

from .creature import *
from .actions.weapon import Weapon
from .actions.defence import Defence
from .actions.interaction import Interaction


korubs = []

class Korub(Creature):
    def __init__(self):
        super().__init__()

        # Load the creature image
        self.setImage('creatures/korub.png')

        # Maximum velocity in pixels per frame
        self.max_velocity = 10

        # Weapons
        self.weapons["big claw"] = Weapon("crush", power=100)
        self.weapons["acid"] = Weapon("venom", power=100)

        # Defence
        self.defence["shell"] = Defence("shell", power=10)


    def tick(self):
        # Move randomly left or right
        self.steering += randint(-1,1)  # positive is left, negative is right
        self.acceleration = 1

        # Take action if we reach the edge of the world
        if self.position.x <= WORLD_LEFT+20:
            self.angle = 0
        elif self.position.x > WORLD_RIGHT-20:
            self.angle = 180
        elif self.position.y <= WORLD_TOP+20:
            self.angle = 270
        elif self.position.y >= WORLD_BOTTOM-20:
            self.angle = 90

        if self.status=="asleep" and self.alertness < 100:
            # If we were asleep, keep sleeping until fully alert
            self.say("Zzz")
            action = "sleep"

        elif self.alertness < 10:
            # If we are tired, go to sleep
            self.say("Zzz")
            action = "sleep"

        else:
            # OK to move
            action = "move"

        return action

    def interact(self, other_creature_data):
        '''Interact with another creature'''

        # Randomly choose whether to eat, attack or ignore
        decision = randint(1,4)
        if decision==1:
            return Interaction("eat")
        elif decision==2:
            return Interaction("attack", "big claw") 
        elif decision==3:
            return Interaction("attack", "acid") 
        else:
            return Interaction("ignore")



def start():
    for i in range(5):
        korubs.append(Korub())
    korubs.append(1)
    return korubs
