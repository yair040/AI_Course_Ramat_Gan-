import matplotlib.pyplot as plt
import numpy as np

plt.ion()
fig = plt.figure()
# 111 means 1 row × 1 column, first subplot.
ax = fig.add_subplot(111)
plt.title("Rotate Rectangle", color='red')

line, = ax.plot([], [], 'b-')         # line connecting points print in Blue.
scatter = ax.scatter([], [], color='red')  # points print in Red.

# The last point is as the first point, the purpose is to draw the last line back to the first point.
points = np.array([[2,1],[2,-1],[-2,-1],[-2,1],[2,1]])

theta= np.pi/128 # The angle was choosen to be small enugh for smooth rotation.
# Matrix that rotates the rectangle (5 points vector) by theta.
R= np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

# Do 200 rotations
for i in range(200):   
    # update line and scatter
    # put all rows first column (x) and all rows second column (y).
    line.set_data(points[:,0], points[:,1])
    scatter.set_offsets(np.c_[points[:,0], points[:,1]])  # scatter uses set_offsets for new points
    ax.relim() # Ensures the axes scale correctly as points are added.
    ax.autoscale_view()
    plt.gca().set_aspect('equal') # define that scale of x and y is the same.
    ax.set_xlim(-2.5, 2.5)       # manually fix x-limits
    ax.set_ylim(-2.5, 2.5)       # manually fix y-limits
    plt.draw()
    # Pauses for 0.5 seconds to let the GUI refresh and to see the animation.
    # Also gives time for the window to respond to events (resize, move, close).
    plt.pause(0.01)
    # Calculate the new points by multiply the points matrix by transpose of the rotation matrix.
    # points is 5X2 matrix, R is 2X2 matrix. The result is 5X2 matrix, the new points.
    points = points @ R.T 

plt.ioff()
plt.show()
















