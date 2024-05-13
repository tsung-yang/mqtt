import json 
import matplotlib.pyplot as plt
import numpy as np
from map import map_data
from matplotlib import animation
from robot_plan import robot_planer
from map import drawer
class ROBOTSIMULATOR:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []  # Empty lists to store plot points dynamically
        self.line, = self.ax.plot(self.xdata, self.ydata, 'o-', markersize=5, color='blue')  # Line object

    def init(self):
        self.line.set_data([], [])  # Initialize with no data points
        return self.line,

    def animation(self, i):
        # Update data for animation based on current frame (i)
        self.xdata.append(interpolated_path[i][0])
        self.ydata.append(interpolated_path[i][1])
        self.line.set_data(self.xdata, self.ydata)  # Set new data for the line

        self.ax.set_xlim(0, 20)  # Set axis limits based on your map dimensions (adjust as needed)
        self.ax.set_ylim(0, 20)

        return self.line,

  
if __name__ == "__main__":
     data = map_data(20,20)
     loaded_data = data.map_load('/home/tsungyang/mqtt_com/client/map_data.json')
     plan=robot_planer(loaded_data)
     path_array=plan.plan_path()
     # Set desired number of steps for interpolation between segments
     num_steps = int(input("please set the number of steps"))
     interpolated_path = plan.interpolation(path_array, num_steps)


     
    # Create animation
     simulator = ROBOTSIMULATOR()  # Create an instance of ROBOTSIMULATOR
     #draw the map
     if loaded_data is not None:
        draw = drawer(loaded_data,)
        draw.map_draw(simulator.fig,simulator.ax)
     else:
        print("Error: Unable to load map data.")
     anim = animation.FuncAnimation(simulator.fig, simulator.animation, init_func=simulator.init,
                                   frames=len(interpolated_path), interval=100)     
     plt.title('Robot Path Animation')  # Set a title
     plt.show()

     
