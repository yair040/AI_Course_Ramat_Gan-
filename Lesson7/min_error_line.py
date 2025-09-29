
import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Create 1000 points (x,y)
points = np.random.rand(1000, 2)

# Create a,b coefficients for y=ax + b. Both between 0 and 1.
coefficients = np.random.rand(100, 2)
# change the line slop (the "a" coefficient) to be uniform random. pi/2-0.017 is about 89 degrees.
coefficients[:,0] = coefficients[:,0]*(math.pi/2-0.017)
coefficients[:,0] = np.tan(coefficients[:,0])
a_array = coefficients[:,0].reshape(-1,1) # convert the "a" array from 1D to 2D with 1 column.
b_array = coefficients[:,1].reshape(-1,1) # convert the "b" array from 1D to 2D with 1 column.
x_array = points[:,0].reshape(1,-1) # convert the "x" array from 1D to 2D with 1 row.
y_array = points[:,1].reshape(1,-1) # convert the "y" array from 1D to 2D with 1 row.

# Save 2 loops by using muliply vector a(100x1) by vector x(1x1000) to get matrix 100x1000 of ai*xj.
# then do vector y_array(1x1000) adding and vector b_array(100x1) sbstruct.
errors = (y_array - a_array * x_array - b_array) ** 2
total_errors = np.sum(errors, axis=1)
    
index = np.argmin(total_errors) # find line index of minimum error.
print("line with minimum errors is at index ",index)
print("a (the slop) for the line is ",coefficients[index,0])
print("b is ",coefficients[index,1])
xline = np.linspace(0,1,2)
yline = coefficients[index,0]*xline + coefficients[index,1]

plt.scatter(points[:,0], points[:,1], color="red")  # x = first column, y = second
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Scatter plot of points")
plt.plot(xline,yline)
plt.show()

   
        
        
