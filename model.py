from mpl_toolkits.mplot3d import Axes3D

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import colors
import seaborn as sns

import numpy as np
import copy


from boid import Boid


class BoidModel:
	def __init__(self, count, d_neighbour, d_crash, vmax, l, area=1):
		np.random.seed(19680801)
		self.bound = 0.3

		self.boids = np.array([Boid(area, d_neighbour, d_crash, vmax, l) for i in range(count)])

		self.area = area
		self.count = count
		self.d_neighbour = d_neighbour
		self.d_crash = d_crash
		self.vmax = vmax
		self.l = l

	def __str__(self):
		return str(self.boids)


	#  Move Update to Boid itself with parameter boids of interest
	def update(self):
		new_boids = copy.deepcopy(self.boids)

		for i in range(self.count):
			new_boids[i].update(self.boids)

		self.boids = new_boids


	def animate(self, save=False):
		self.scats = []

		def draw_update(stuff):
			for scat in self.scats:
				scat.remove()
			self.scats = []
			self.update()
			pos = np.array([b.position for b in self.boids])
			vel = np.array([b.velocity for b in self.boids])

			# Fix this
			self.scats.append(ax.scatter(pos[:, 0], pos[: , 1], pos[:, 2], c=np.linalg.norm(vel, axis=1), vmin=0, vmax=self.vmax, depthshade=True, cmap='winter'))

			# import matplotlib.markers as mmarkers
			# print(np.arctan2(vel[:, 0], vel[:, 1]))
			# for i in np.arctan2(vel[:, 0], vel[:, 1]):
			# 	print(i)
			# m = [(3, 0, v  * 180 / np.pi) for v in np.arctan2(vel[:, 0], vel[:, 1])]
			# paths = []
			# for marker in m:
			# 	if isinstance(marker, mmarkers.MarkerStyle):
			# 		marker_obj = marker
			# 	else:
			# 		marker_obj = mmarkers.MarkerStyle(marker)
			# 	path = marker_obj.get_path().transformed(marker_obj.get_transform())
			# 	paths.append(path)
			# self.scats[-1].set_paths(paths)


		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		ax.set_xlim([-self.bound, self.bound])
		ax.set_ylim([-self.bound, self.bound])
		ax.set_zlim([-self.bound, self.bound])
		
		pos = np.array([b.position for b in self.boids])
		vel = np.array([b.velocity for b in self.boids])
		self.scats.append(ax.scatter(pos[:, 0], pos[: , 1], pos[:, 2], c=np.linalg.norm(vel, axis=1), vmin=0, vmax=self.vmax, depthshade=True, cmap='winter'))
		plt.colorbar(self.scats[0])

		ani = animation.FuncAnimation(fig, draw_update, fargs=(), interval=60, blit=False)

		if(not save):
			plt.show()
		else: 
			writergif = animation.PillowWriter(fps=15) 
			ani.save('animation.gif', writer=writergif)


	def draw(self):
		pos = np.array([b.position for b in self.boids])
		vel = np.array([b.velocity for b in self.boids])
		fig = plt.figure()

		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlim([-self.bound, self.bound])
		ax.set_ylim([-self.bound, self.bound])
		ax.set_zlim([-self.bound, self.bound])
		q = ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c=np.linalg.norm(vel, axis=1), depthshade=True, cmap='winter')
		plt.colorbar(q)
		plt.show()


