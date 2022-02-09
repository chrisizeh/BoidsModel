from mpl_toolkits.mplot3d import Axes3D

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib import colors
import matplotlib.cm as cm
from matplotlib.colors import Normalize

from bisect import bisect_right

import numpy as np
import copy


from boid import Boid


class BoidModel:
	def __init__(self, count, d_neighbour, d_crash, vmax, l, area=1):
		np.random.seed(19680801)
		self.bound = 1

		self.area = area
		self.count = count
		self.d_neighbour = d_neighbour
		self.d_crash = d_crash
		self.vmax = vmax
		self.l = l

		# self.num_grids = 4
		self.num_grids = int((4 * area) / d_neighbour)
		self.grid_borders = np.linspace(-2 * self.area, 2 * self.area, self.num_grids, endpoint=False)

		self.boids = {}
		self.boids_grid = np.empty((self.num_grids, self.num_grids, self.num_grids), dtype=object)
		self.createBoids()

	def __str__(self):
		return str(self.boids)

	def createBoids(self):
		for x in range(self.num_grids):
			for y in range(self.num_grids):
				for z in range(self.num_grids):
					self.boids_grid[x, y, z] = np.empty(0)

		for i in range(self.count):
			boid = Boid(i, self.area, self.d_neighbour, self.d_crash, self.vmax, self.l)

			x_val = bisect_right(self.grid_borders, boid.position[0], lo=0, hi=self.num_grids-1) - 1
			y_val = bisect_right(self.grid_borders, boid.position[1], lo=0, hi=self.num_grids-1) - 1
			z_val = bisect_right(self.grid_borders, boid.position[2], lo=0, hi=self.num_grids-1) - 1

			self.boids[boid.id] = boid
			self.boids_grid[y_val, x_val, z_val] = np.append(self.boids_grid[y_val, x_val, z_val], boid.id)



	def update(self):
		new_boids = copy.deepcopy(self.boids)
		grid = copy.deepcopy(self.boids_grid)

		for y in range(0, self.num_grids):
			for x in range(0, self.num_grids):
				for z in range(0, self.num_grids):
					if(len(self.boids_grid[y, x, z]) >= 1):
						neighbours = np.hstack(self.boids_grid[max(0,y-1):min(y+2,self.num_grids-1), max(0,x-1):min(x+2,self.num_grids), max(0,z-1):min(z+2,self.num_grids)].flatten())
						
						i = 0
						for key in self.boids_grid[y, x, z]:
							new_boids[key].update(self.boids, neighbours)
							x_val = bisect_right(self.grid_borders, new_boids[key].position[0], lo=0, hi=self.num_grids-1) - 1
							y_val = bisect_right(self.grid_borders, new_boids[key].position[1], lo=0, hi=self.num_grids-1) - 1
							z_val = bisect_right(self.grid_borders, new_boids[key].position[2], lo=0, hi=self.num_grids-1) - 1

							if(x_val != x or y_val != y or z != z_val):
								grid[y_val, x_val, z_val] = np.append(grid[y_val, x_val, z_val], key)
								grid[y, x, z] = np.delete(grid[y, x, z], i)
							else:
								i += 1

		self.boids = new_boids
		self.boids_grid = grid

	def update_naiv(self):
		new_boids = copy.deepcopy(self.boids)

		for i in new_boids:
			new_boids[i].update(self.boids, self.boids.keys())

		self.boids = new_boids


	def animate(self, save=False, name='animation', naiv=False):
		self.scats = []
		norm = Normalize()
		colormap = cm.winter

		def draw_update(stuff):

			for scat in self.scats:
				scat.remove()
			self.scats = []

			if(naiv):
				self.update_naiv()
			else:
				self.update()

			pos = np.array([b.position for b in self.boids.values()])
			vel = np.array([b.velocity for b in self.boids.values()])
			vel = np.round(vel * 3, 3)
			
			zero_index = np.argwhere(np.sum(vel, axis=1) == 0).flatten()
			pos = np.delete(pos, zero_index, axis=0)
			vel = np.delete(vel, zero_index, axis=0)

			colors = np.linalg.norm(pos[:, :2] + 1, axis=1)
			colors = np.append(colors, np.repeat(colors, 2))

			self.scats.append(ax.quiver(pos[:, 0], pos[: , 1], pos[:, 2], vel[:, 0], vel[: , 1], vel[:, 2], color=colormap(norm(colors))))


		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		ax.set_xlim([-self.bound, self.bound])
		ax.set_ylim([-self.bound, self.bound])
		ax.set_zlim([-self.bound, self.bound])
		
		pos = np.array([b.position for b in self.boids.values()])
		vel = np.array([b.velocity for b in self.boids.values()])
		vel = np.round(vel * 3, 3)

		zero_index = np.argwhere(np.sum(vel, axis=1) == 0).flatten()
		pos = np.delete(pos, zero_index, axis=0)
		vel = np.delete(vel, zero_index, axis=0)

		colors = np.linalg.norm(pos[:, :2] + 1, axis=1)
		norm.autoscale(colors)
		colors = np.append(colors, np.repeat(colors, 2))

		self.scats.append(ax.quiver(pos[:, 0], pos[: , 1], pos[:, 2], vel[:, 0], vel[: , 1], vel[:, 2], color=colormap(norm(colors))))

		ani = animation.FuncAnimation(fig, draw_update, fargs=(), frames=500, blit=False)

		if(not save):
			plt.show()
		else: 
			writergif = animation.PillowWriter(fps=25)
			ani.save(name + '_N-' + str(self.count) +  '_vmax-' + str(self.vmax) + '_observ-' + str(self.d_neighbour) + '_crash-' + str(self.d_crash) + '_l-' + str(self.l) +
					 '.gif', writer=writergif)


	def draw(self):
		fig = plt.figure()
		norm = Normalize()
		colormap = cm.winter

		ax = fig.add_subplot(111, projection='3d')
		ax.set_xlim([-self.bound, self.bound])
		ax.set_ylim([-self.bound, self.bound])
		ax.set_zlim([-self.bound, self.bound])

		pos = np.array([b.position for b in self.boids.values()])
		vel = np.array([b.velocity for b in self.boids.values()])
		vel = np.round(vel * 3, 3)

		colors = np.linalg.norm(pos[:, :2] + 1, axis=1)
		norm.autoscale(colors)
		colors = np.append(colors, np.repeat(colors, 2))
		q = ax.quiver(pos[:, 0], pos[: , 1], pos[:, 2], vel[:, 0], vel[: , 1], vel[:, 2], color=colormap(norm(colors)))
		plt.show()


