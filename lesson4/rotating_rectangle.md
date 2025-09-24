# Rotating Rectangle Python Program - Help

## Project Overview
The Rotating Rectangle program visualizes a 2x4 rectangle centered at the origin rotating around its center. Lines are displayed in blue, corner points in red, and the title of the plot is displayed in red as "Rotate Rectangle".

## Prerequisites
- Python 3.x
- NumPy
- Matplotlib

## How to Run
1. Ensure Python 3.x is installed.
2. Install dependencies:
   ```bash
   pip install numpy matplotlib
   ```
3. Run the Python script containing the rectangle rotation implementation.

## Features
- Rectangle dimensions: Width = 4, Height = 2.
- Centered at the origin (0,0).
- Rotation angle: π/128 radians per step.
- 200 animation steps with 10ms delay per step.
- Lines connecting corners in blue, corner points in red.
- Equal axes for correct visualization.
- Plot title: "Rotate Rectangle" in red.

## Tasks (Summary)
1. **Environment Setup**: Install Python and required packages.
2. **Define Rectangle**: Set rectangle dimensions and compute corner points.
3. **Define Rotation**: Create a 4x4 rotation matrix for the animation.
4. **Plot Setup**: Initialize Matplotlib, plot rectangle and points, configure axes and title.
5. **Animation Loop**: Rotate rectangle in steps, update plot, and pause between steps.
6. **Finalization**: Turn off interactive mode and show final plot.
7. **Testing & Validation**: Verify rotation, point storage, colors, axes, and title.
8. **Documentation**: Comment code and provide instructions for usage.

## Notes
- Each step should be verified before proceeding to the next.
- Ensure version control is maintained for the code files.

## Additional Information
- The rectangle is stored in a NumPy array with the first point repeated as the last to close the shape.
- The 4x4 rotation matrix uses homogeneous coordinates to rotate points around the origin.
- Use `plt.pause(0.01)` for smooth animation.

