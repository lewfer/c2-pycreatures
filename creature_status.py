# Package up create detail to pass to other creature during interaction
# We do this so we don't pass the actual Creature object, otherwise the opponent may just destroy them by changing attributes directly

#class CreatureStatus():
#    def __init__(self, type, size, health, action=None):
#        self.type = type
#        self.size = size
#        self.health = health
#        #self.action = action    # action that creature has chosen
