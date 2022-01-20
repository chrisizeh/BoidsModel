import numpy as np
import copy

class Boid:
	def __init__(self, key, area, d_neighbour, d_crash, vmax, l):
		# self.velocity = np.zeros(3)

		# To allow fewer boids on more area to start moving
		self.velocity = np.random.uniform(low=-vmax, high=vmax, size=3)
		self.position = np.random.uniform(low=-area, high=area, size=3)

		self.id = key
		self.area = area
		self.d_neighbour = d_neighbour
		self.d_crash = d_crash
		self.vmax = vmax
		self.l = l

	def update(self, boids, ids):
		w = np.zeros(shape=(4, 3))
		neighbours = 0
		crash = 0

		for i in ids:
			boid = boids[i]
			diff = self.position - boid.position
			dist = np.linalg.norm(diff)

			if self.id != boid.id and dist < self.d_neighbour:

				neighbours += 1
				w[0] += boid.position
				w[1] += boid.velocity

				if dist < self.d_crash:
					crash += 1
					w[2] += diff

		if np.max(np.abs(self.position)) > self.area:
			w[3] = -self.position

		if(neighbours > 0):
			w[0] /= neighbours
			w[1] /= neighbours

			if(crash > 0):
				w[2] /= crash

			w[0] -= self.position

		self.velocity = self.velocity * self.l[0] + w[0] * self.l[1] + w[1] * self.l[2] + w[2] * self.l[3] + w[3] * self.l[4]
		if np.linalg.norm(self.velocity) > self.vmax:
			self.velocity = self.vmax * (self.velocity / np.linalg.norm(self.velocity))

		self.position = self.position + self.velocity

	def __str__(self):
		return "Position: {}, Velocity: {}".format(self.position, self.velocity)

	def __repr__(self):
		return "Position: {}, Velocity: {}".format(self.position, self.velocity)