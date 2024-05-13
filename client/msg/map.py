import json
import matplotlib.pyplot as plt
class map_data:
      def __init__(self,width,height):
          self.width = width
          self.height = height
      def map_load(self,file_path):
          try:
                
               with open(file_path,'r') as f:
                    data=json.load(f)
               data['width']= self.width
               data['height']=self.height
               data['obstacles'] = []
               num = int(input("please input the number of obstacles\n"))
               for i in range(num):
                        obstacle = {}
                        obstacle['x'] = float(input(f"please input the coordinates of the center position x of the {i+1}th obstacle\n"))
                        obstacle['y'] = float(input(f"please input the coordinates of the center position y of the {i+1}th obstacle\n"))
                        obstacle['width'] = float(input(f"please input the width of {i+1}th obstacle\n"))
                        obstacle['height'] = float(input(f"please input the height of {i+1}th obstacle\n"))
                        data["obstacles"].append(obstacle)
               with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
          except FileNotFoundError:
                raise FileNotFoundError(f"file not found:{file_path}")
          return data
class drawer:
    def __init__(self,data):
          self.data = data


    def map_draw(self,fig,ax):
          width = self.data['width']
          height = self.data['height']
          # Create the plot with appropriate limits
          ax.set_xlim(0, width)
          ax.set_ylim(0, height)
          ax.set_aspect('equal')  # Ensure equal aspect ratio
          # Draw the map boundaries (optional)
          ax.plot([0, width, width, 0, 0], [0, 0, height, height, 0], color='black', linestyle='-')
          # Draw obstacles as rectangles
          for obstacle in self.data['obstacles']:
               x_center, y_center, width, height = obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']
               x_min, y_min = x_center - width / 2, y_center - height / 2
               ax.add_patch(plt.Rectangle(xy=(x_min, y_min),
                                        width=width, height=height,
                                        color='red',
                                        alpha=0.7))  # Semi-transparent red

          plt.xlabel("X-axis")
          plt.ylabel("Y-axis")

if __name__ == "__main__":
    data=map_data(20,20)
    loaded_data = data.map_load('/home/tsungyang/mqtt_com/client/map_data.json')

    if loaded_data is not None:
        draw = drawer(loaded_data)
        draw.map_draw()
    else:
        print("Error: Unable to load map data.")