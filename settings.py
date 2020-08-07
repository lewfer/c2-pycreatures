# Size of display
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800
WORLD_WIDTH = 600
WORLD_HEIGHT = 600
PADDING = 10
WORLD_LEFT = PADDING
WORLD_RIGHT = PADDING + WORLD_WIDTH
WORLD_TOP = PADDING
WORLD_BOTTOM = PADDING + WORLD_HEIGHT

# Info panel
INFO_PANEL_LEFT = WORLD_WIDTH+PADDING*2
INFO_PANEL_TOP = PADDING

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
WORLD_COLOUR = (255,200,100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Intial health for all creatures
INITIAL_ENERGY = 5000
INITIAL_ALERTNESS = 100

# Changes to all creatures health on tick
TICK_AGE_INCREASE = 1
TICK_ALERTNESS_REDUCTION = 1
TICK_ENERGY_REDUCTION = 0.5

# Energy level below which creature starts to fade
FADE_ENERGY = INITIAL_ENERGY / 2

# Minimum fade level, to prevent invisible creatures
MIN_FADE = 10

# Multiplier applied to the velocity to calculate reduction in energy
VELOCITY_MOVEMENT_ENERGY_LOSS_MULTIPLIER = 1

# Multiplier applied to battle power to calculate reduction in energy
BATTLE_POWER_MOVEMENT_ENERGY_LOSS_MULTIPLIER = 0.02

# Increase in alertness when creature sleeps
SLEEP_ALERTNESS_INCREASE = 5

# Multiplier applied to creature size to get bit size
BITE_SIZE_MULTIPLIER = 0.2

# Smallest random damage multiplier when battle lost
MIN_BATTLE_DAMAGE_MULTIPLIER = 0.2

# Energy lost by weapons/defence mechanism usage
BATTLE_POWER_ENERGY_LOSS_MULTIPLIER = 0.1

# Multiplier applied to creature size to get energy lost when mating
MATE_ATTEMPT_ENERGY_MULTIPLIER = 0.05

# How much energy transferred to offspring
MATE_ENERGY_TRANSFER_MULTIPLIER = 0.2

# Logging options
LOG_MOVE = False
LOG_SLEEP = False
LOG_DIED = True
LOG_DIVIDE = True
LOG_MATE = True
LOG_EAT = True
LOG_ATTACK = True

# Which creatures to include and exclude from the log file
LOG_INCLUDE = ["All"] # "All" for all creatures
LOG_EXCLUDE = ["Sun"]

DEBUG = False


FPS = 5