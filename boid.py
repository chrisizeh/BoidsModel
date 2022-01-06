import numpy as np
import copy

class Boid:
	def __init__(self, vmax):
		self.vmax = vmax
		self.velocity = np.zeros(3)
		self.position = np.zeros(3)
		# self.position = np.random.uniform(low=-1.0, high=1.0, size=3)

	def set_position(self, pos):
		self.position = np.array(copy.deepcopy(pos))

	def __str__(self):
		return "Position: {}, Velocity: {}".format(self.position, self.velocity)

	def __repr__(self):
		return "Position: {}, Velocity: {}".format(self.position, self.velocity)