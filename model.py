from mpl_toolkits.mplot3d import Axes3D

from matplotlib import pyplot as plt
from matplotlib import animation

import numpy as np
import copy


from boid import Boid


class BoidModel:
	def __init__(self, count, d_neighbour, d_crash, vmax, l, area=1):
		np.random.seed(19680801)

		self.boids = np.array([Boid(area) for i in range(count)])

		self.area = area
		self.count = count
		self.d_neighbour = d_neighbour
		self.d_crash = d_crash
		self.vmax = vmax
		self.l = l

	def __str__(self):
		return str(self.boids)


	def update(self):
		new_boids = copy.deepcopy(self.boids)

		for i in range(self.count):
			w = np.zeros(shape=(4, 3))
			neighbour = 0
			crash = 0

			for j, boid in zip(range(self.count), self.boids):
				diff = new_boids[i].position - boid.position
				dist = np.linalg.norm(diff)

				if dist < self.d_neighbour:

					neighbour += 1
					w[0] += boid.position
					w[1] += boid.velocity

					if dist < self.d_crash:
						crash += 1
						w[2] += diff

			if np.max(np.abs(new_boids[i].position)) > self.area:
				w[3] = -new_boids[i].position

			if(neighbour > 0):
				w[0] /= neighbour
				w[1] /= neighbour

				if(crash > 0):
					w[2] /= crash

				w[0] -= new_boids[i].position

			new_boids[i].velocity = new_boids[i].velocity * self.l[0] + w[0] * self.l[1] + w[1] * self.l[2] + w[2] * self.l[3] + w[3] * self.l[4]
			if np.linalg.norm(new_boids[i].velocity) > self.vmax:
				new_boids[i].velocity = self.vmax * (new_boids[i].velocity / np.linalg.norm(new_boids[i].velocity))

			new_boids[i].position = new_boids[i].position + new_boids[i].velocity

		self.boids = new_boids


	def animate(self, save=False):
		self.scats = []

		def draw_update(stuff):
			for scat in self.scats:
				scat.remove()
			self.scats = []
			self.update()
			pos = np.array([b.position for b in self.boids])
			self.scats.append(ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2]))

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlim([-self.area * 3, self.area * 3])
		ax.set_ylim([-self.area * 3, self.area * 3])
		ax.set_zlim([-self.area * 3, self.area * 3])
		pos = np.array([b.position for b in self.boids])
		self.scats.append(ax.scatter(pos[:, 0], pos[: , 1], pos[:, 2]))

		ani = animation.FuncAnimation(fig, draw_update, fargs=(), interval=60, blit=False)

		if(not save):
			plt.show()
		else:
			writergif = animation.PillowWriter(fps=15) 
			ani.save('animation.gif', writer=writergif)


	def draw(self):
		pos = np.array([b.position for b in self.boids])
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlim([-self.area * 3, self.area * 3])
		ax.set_ylim([-self.area * 3, self.area * 3])
		ax.set_zlim([-self.area * 3, self.area * 3])

		ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2])
		plt.show()


