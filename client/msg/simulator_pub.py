import json
import random
import time
import paho.mqtt.client as mqtt_client
from msg_robot_state import MsgRobotState
from robot_plan import robot_planer
from map import map_data
from map import drawer
from robot_simulator import ROBOTSIMULATOR



def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 1000:
            break
def publish_msg(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

    
if __name__ == "__main__":
     broker = 'localhost'
     port = 1883
     topic = "robot/simulator"
     client_id = "robot" + str(random.randint(0, 1000))
     data = map_data(20,20)
     loaded_data = data.map_load('/home/tsungyang/mqtt_com/client/map_data.json')
     plan=robot_planer(loaded_data)
     path_array=plan.plan_path()
     num_steps = int(input("please set the number of steps\n"))
     interpolated_path = plan.interpolation(path_array, num_steps)
     simulator = ROBOTSIMULATOR()
     path_json = simulator.to_json(interpolated_path)

     #battery = plan.battery()
     msg_robot_state = MsgRobotState(robot_id=client_id)
     client = connect_mqtt()
     client.loop_start()
     while True:
        #msg_robot_state.battery = battery
        path_json = simulator.to_json(interpolated_path)
        publish_msg(client, topic, path_json)
        time.sleep(1)

     client.loop_stop()
     # 创建 MQTT 客户端并发布数据
     
