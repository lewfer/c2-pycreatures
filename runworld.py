from world import *


import pycreatures_logging as log


# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------

log.setupLogging("pycreatures.log", log.INFO)

world = World()
world.run()