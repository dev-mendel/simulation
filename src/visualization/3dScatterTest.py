from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = list(range(10))
Y = [5, 6, 2, 3, 13, 4, 1, 2, 4, 8]
Z = [3, 5, 2, 6, 7, 3, 14, 3, 2, 9]

ax.scatter(X, Y, Z, c='r', marker='o')

plt.show()
