#action: attack, ignore, avoid, sleep, eat, look, defend, move
# attack has details of weapon
# defend has details of defence mechanism

class Interaction():
    def __init__(self, action, details=None):
        self.action = action        # name of action to take
        self.details = details      # details, depending on action

    def __str__(self):
        return self.action + ":" + str(self.details)