import random
from msg.msg_robot_state import MsgRobotState
from paho.mqtt import client as mqtt_client



def connect_mqtt(client_id, broker, port) -> mqtt_client:
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

def subscribe_robot_state(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        # Decode the message payload (assuming UTF-8 encoding for JSON)
        json_data = msg.payload.decode()
        robot_state = MsgRobotState.from_json(json_data)
        # print(f"Robot ID: {robot_state.robot_id}")
        print(json_data)

    client.subscribe(topic)
    client.on_message = on_message


def run():

    broker = 'localhost'
    port = 1883
    topic = "robot/state"
    # Generate a Client ID with the subscribe prefix.
    client_id = f'subscribe-{random.randint(0, 100)}'
    # username = 'emqx'
    # password = 'public'

    client = connect_mqtt(client_id, broker, port)
    subscribe_robot_state(client, topic)  # Store returned messages
    client.loop_forever()



if __name__ == '__main__':
    run()
