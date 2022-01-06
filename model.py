from mpl_toolkits.mplot3d import Axes3D

from matplotlib import pyplot as plt
from matplotlib import animation

import numpy as np
import copy


from boid import Boid

class BoidModel:
	def __init__(self, count, d_neighbour, d_crash, vmax, l):
		np.random.seed(19680801)

		# self.boids = np.array([Boid(vmax) for i in range(count)])
		self.boids = np.empty(0)

		for i in range(count):
			self.boids = np.append(self.boids, Boid(vmax))
			self.boids[i].set_position(np.random.uniform(low=-1.0, high=1.0, size=3))

		self.count = count
		self.d_neighbour = d_neighbour
		self.d_crash = d_crash
		self.vmax = vmax
		self.l = l

	def __str__(self):
		return str(self.boids)

	def update(self):
		new_boids = np.asarray(self.boids)

		for i in range(self.count):
			# TODO
			new_boids[i] = Boid(self.vmax)
			new_boids[i].set_position(self.boids[i].position.tolist())
			new_boids[i].velocity = np.asarray(self.boids[i].velocity)
			main = new_boids[i]

			w = np.zeros(shape=(4, 3))
			neighbour = 0
			crash = 0

			for j, boid in zip(range(self.count), self.boids):
				diff = main.position - boid.position
				dist = np.linalg.norm(diff)

				if i != j and dist < self.d_neighbour:
					neighbour += 1
					w[0] += boid.position
					w[1] += boid.velocity

					if dist < self.d_crash:
						crash += 1
						w[2] += diff

			if np.max(np.abs(main.position)) > 1:
				print('if 1')
				w[3] = -main.position

			if(neighbour > 0):
				print('if 2')
				w[0] /= neighbour
				w[1] /= neighbour

				if(crash > 0):
					w[2] /= crash

				w[0] -= main.position
			print(w)

			main.velocity = main.velocity * self.l[0] + w[0] * self.l[1] + w[1] * self.l[2] + w[2] * self.l[3] + w[3] * self.l[4]
			
			if np.linalg.norm(main.velocity) > self.vmax:
				print('if 3')
				# print(np.linalg.norm(main.velocity))
				# print(main.velocity)
				main.velocity = self.vmax * (main.velocity / np.linalg.norm(main.velocity))
				# print(main.velocity)

			print(main.velocity)
			print(main.position)
			main.position = main.position + main.velocity
			print(main.position)

		print(self.boids)
		self.boids = new_boids


	def animate(self):
		self.scats = []

		def draw_update(stuff):
			# for scat in self.scats:
			# 	scat.remove()
			self.scats = []
			self.update()
			pos = np.array([b.position for b in self.boids])
			print(pos)
			self.scats.append(ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2]))

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlim([-1, 1])
		ax.set_ylim([-1, 1])
		ax.set_zlim([-1, 1])
		pos = np.array([b.position for b in self.boids])
		self.scats.append(ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2]))

		ani = animation.FuncAnimation(fig, draw_update, 1, fargs=(), interval=10, blit=False)
		plt.show()


	def draw(self):
		pos = np.array([b.position for b in self.boids])
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlim([-1, 1])
		ax.set_ylim([-1, 1])
		ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2])
		plt.show()


