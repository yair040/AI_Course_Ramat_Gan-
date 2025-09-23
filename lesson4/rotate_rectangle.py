import matplotlib.pyplot as plt
import numpy as np

plt.ion()
fig = plt.figure()
# 111 means 1 row × 1 column, first subplot.
ax = fig.add_subplot(111)
plt.title("Rotate Rectangle", color='red')

line, = ax.plot([], [], 'b-')         # line connecting points
scatter = ax.scatter([], [], color='red')  # points

points = np.array([[2,1],[2,-1],[-2,-1],[-2,1],[2,1]])

theta= np.pi/128
R= np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

for i in range(200):   
    line.set_data(points[:,0], points[:,1])
    scatter.set_offsets(np.c_[points[:,0], points[:,1]])  # scatter uses set_offsets for new points
    ax.relim()
    ax.autoscale_view()
    plt.gca().set_aspect('equal')
    ax.set_xlim(-2.5, 2.5)       # manually fix x-limits
    ax.set_ylim(-2.5, 2.5)       # manually fix y-limits
    plt.draw()
    plt.pause(0.01)
    points = points @ R.T 

plt.ioff()
plt.show()















