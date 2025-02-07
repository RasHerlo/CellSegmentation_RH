
import matplotlib.pyplot as plt
import numpy as np

class FreehandDrawer:
    def __init__(self, ax):
        self.ax = ax
        self.line, = ax.plot([], [], 'r-', linewidth=2)  # Line for drawing
        self.xdata = []
        self.ydata = []
        self.cid = ax.figure.canvas.mpl_connect('motion_notify_event', self.motion)
        self.cid2 = ax.figure.canvas.mpl_connect('button_press_event', self.button_press)
        self.completed = False # Flag to check if drawing is complete

    def motion(self, event):
        if event.inaxes == self.ax and not self.completed:
            if event.button == 1: # Left mouse button
                self.xdata.append(event.xdata)
                self.ydata.append(event.ydata)
                self.line.set_data(self.xdata, self.ydata)
                self.ax.relim()  # Rescale the axes
                self.ax.autoscale_view()
                self.ax.figure.canvas.draw()
    
    def button_press(self, event):
        if event.inaxes == self.ax and event.button == 3: # Right mouse button to finish
             self.completed = True
             self.line.set_data(self.xdata, self.ydata) # Finalize the line
             self.ax.relim()
             self.ax.autoscale_view()
             self.ax.figure.canvas.draw()
             self.ax.figure.canvas.mpl_disconnect(self.cid)
             self.ax.figure.canvas.mpl_disconnect(self.cid2)

from PIL import Image

img = Image.open('C:\\Users\\rasmu\\Projects\\MATLAB Repos\\Calsee\\ACtrial.tif')
img_array = np.array(img)

# Example usage:
fig, ax = plt.subplots()
# image = np.random.rand(256, 256) # Replace with your image data
ax.imshow(img_array)

drawer = FreehandDrawer(ax)
plt.show(block=False) # Important: non-blocking to allow interaction

# After the drawing is complete
while not drawer.completed:
    plt.pause(0.01) # Small pause to allow GUI updates

vertices = np.array([drawer.xdata, drawer.ydata]).T  # Get the vertices as a NumPy array
print(vertices)
mask = poly2mask(vertices[:, 0], vertices[:, 1], image.shape[0], image.shape[1]) # Create a mask
plt.imshow(mask)
plt.show()

from skimage.draw import polygon2mask as poly2mask # Function to create mask from polygon vertices