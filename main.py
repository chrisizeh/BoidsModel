from model import BoidModel

b = BoidModel(10, 0.02, 0.01, 0.01, [0.31, 0.001, 1.2, 2, 0.01])
b.animate()

# for i in range(100):
# 	b.update()
# 	# print(b)
# 	b.draw()
