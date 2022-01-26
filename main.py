from model import BoidModel
from boid import Boid
import time


import copy
import numpy as np


N=500
observationradius=0.2
crashradius=0.05
vmax=0.01
l=[0.31, 0.001, 1.2, 2, 0.01]

b = BoidModel(N, observationradius, crashradius, vmax, l, area=1)

start_time = time.time()
b.animate(save=True, naiv=True, name="naiv_animation")
print("Naiv: --- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
b.animate(save=True, naiv=False)
print("Grids: --- %s seconds ---" % (time.time() - start_time))