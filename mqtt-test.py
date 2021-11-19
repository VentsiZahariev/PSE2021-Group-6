import paho.mqtt.client as mqttClient
import time
import json
#from database import Database as db

# Global variables with credentials for login to mqtt-broker
broker = "eu1.cloud.thethings.network"  # Broker address/host
port = 1883  # Port to the broker
user = "project-software-engineering@ttn"  # Connection username
password = "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"  # Connection password

# global variabvle to hold the json data
json_data = None
# global variable flag
received_message = False
# global variable for the state of the connection
connected_flag = False


def on_message(client, userdata, message):
    # store the payload in a global variable
    global json_data
    global received_message
    json_data = message.payload
    received_message = True


def mqtt_connect():
    def on_connect(client, userdata, flags, rc):
        global connected_flag
        if rc == 0:
            connected_flag = True
            print("Connected OK, Returned code =", rc)
        else:
            print("Bad connection, Returned code = ", rc)
            connected_flag = True

    client = mqttClient.Client("Python")  # create new instance
    client.username_pw_set(user, password=password)  # set username and password
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback
    client.loop()

    client.connect(broker, port=port)  # connect to broker
    client.loop_start()  # start the loop

    while not connected_flag:  # Wait for connection
        time.sleep(0.1)

    client.subscribe("#")


try:
    mqtt_connect()
    while True:
        time.sleep(1)
        was_closed = False

        if (received_message):
            print(json_data)
            received_message = False


except KeyboardInterrupt:
    print("exiting")
    #client.disconnect()
    #client.loop_stop()