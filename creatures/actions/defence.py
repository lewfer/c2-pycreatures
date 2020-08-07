# Could add camouflage based on colour / background - creature won't see other 

class Defence():
    def __init__(self, type, power):
        self.type = type        # shell, antipoison, antivenom 
        self.power = power      # integer value - power used is subtracted from energy
