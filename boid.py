import numpy as np
import copy

class Boid:
	def __init__(self, area):
		self.velocity = np.zeros(3)
		self.position = np.random.uniform(low=-area, high=area, size=3)

	def __str__(self):
		return "Position: {}, Velocity: {}".format(self.position, self.velocity)

	def __repr__(self):
		return "Position: {}, Velocity: {}".format(self.position, self.velocity)