from mpl_toolkits.mplot3d import Axes3D

from matplotlib import pyplot as plt
import numpy as np

from boid import Boid

class BoidModel:
	def __init__(self, count, d_neighbour, d_crash, vmax):
		np.random.seed(19680801)

		self.boids = np.array([Boid(vmax) for i in range(count)])
		self.d_neighbour = d_neighbour
		self.d_crash = d_crash

	def __str__(self):
		return str(self.boids)

	def draw(self):
		pos = np.array([b.position for b in self.boids])
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2])
		plt.show()


