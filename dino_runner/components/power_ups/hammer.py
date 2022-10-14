from dino_runner.utils.constants import HAMMER, HAMMER_TYPE
from .power_up import PowerUp

class Hammer(PowerUp):
    def __init__(self):
        super().__init__(HAMMER,HAMMER_TYPE)