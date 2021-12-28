import numpy as np

class Boid:
	def __init__(self, vmax):
		self.vmax = vmax
		self.velocity = np.zeros(3)
		self.position = np.random.uniform(low=-1.0, high=1.0, size=3)

	def __str__(self):
		return "Position: {}, Velocity: {}".format(self.velocity, self.position)

	def __repr__(self):
		return "Position: {}, Velocity: {}".format(self.velocity, self.position)