from model import BoidModel
from boid import Boid

import copy
import numpy as np

b = BoidModel(100, 0.1, 0.05, 0.03, [0.31, 0.001, 1.2, 2, 0.01], area=0.1)
b.animate(save=False)