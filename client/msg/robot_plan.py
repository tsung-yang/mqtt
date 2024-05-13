import matplotlib.pyplot as plt
import numpy as np
from map import map_data
from matplotlib import animation
from msg_robot_state import MsgRobotState
class robot_planer:
    def __init__(self,data):
        self.data = data
    
    def plan_path(self):
        pos=[]
        width=[]
        height=[]
        for obstacle in self.data["obstacles"]:
            x_center, y_center, width, height = obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']
            x_1_min,y_1_min = float(x_center - width/2 - 0.5),float(y_center - height/2-0.5)
            x_2_min,y_2_min = float(x_center - width/2 - 0.5),float(y_center + height/2 + 0.5)
            x_3_max,y_3_max = float(x_center + width/2 + 0.5),float(y_center + height/2 + 0.5)
            x_4_max,y_4_max = float(x_center + width/2 + 0.5),float(y_center - height/2-0.5)
            pos.append((x_1_min,y_1_min))
            pos.append((x_2_min,y_2_min))
            pos.append((x_3_max,y_3_max))
            pos.append((x_4_max,y_4_max))

        path_array = np.array(pos)
        return path_array
    def interpolation(self,path_array, num_steps):
        if int(num_steps) <= 0:
            raise ValueError("Number of steps per segment must be positive.")
        interpolated_path = []
        interpolated_path.append(path_array[0])
        for i in range(len(path_array)-1):
            start_point = path_array[i]
            end_point = path_array[i + 1]

            # Linear interpolation
            step_size = (end_point - start_point) / (num_steps + 1)
            
            for step in range(1, num_steps + 1):
                interpolated_point = start_point + step * step_size
                interpolated_path.append(interpolated_point)
        # Append the last point to ensure complete path
        interpolated_path.append(path_array[-1])

        return np.array(interpolated_path)

        
    


if __name__ == "__main__":
    data = map_data(20,20)
    loaded_data = data.map_load('/home/tsungyang/mqtt_com/client/map_data.json')
    plan=robot_planer(loaded_data)
    path_array=plan.plan_path()
    # Set desired number of steps for interpolation between segments
    num_steps = int(input("please set the number of steps"))

    interpolated_path = plan.interpolation(path_array, num_steps)
    print(interpolated_path)




