#!/usr/bin/python3

# mqtt_connection.py
# Last edit made: 10-12-2021
# Version: 0.2
# Subject: Code to retrieve data from the things network and store it to the database
# Author: Tim ter Steege
# python version used: 3.9


import paho.mqtt.client as mqtt
import time
from datetime import datetime
import sys
import mariadb as mariadb

import data_parser as parser
import log_message

# global variable to hold the json string received from
json_data = None
# global variable flag for the status of a newly received message
message_flag = False
# global variable flag for connection status
connected_flag = False

# Global variables with credentials to login to mqtt-broker
mqtt_host = "eu1.cloud.thethings.network"
mqtt_port = 8883
mqtt_username = "project-software-engineering@ttn"
mqtt_password = "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"

# Global variables with credentials to login to database
db_host = "127.0.0.1"
db_port = 3306
db_username = "PSEgroup6"
db_password = "battlefield4"
db_database = "weather_log"

# Global variable for the filename for logging messages
log_filename = "mqtt_log.out"

try:
    mydb = mariadb.connect(user=db_username, password=db_password, host=db_host, port=db_port, database=db_database)
except mariadb.Error as err:
    # logging critical error to output file to let the user now the connection to the database cant be established
    log_message.critical_log(("Can not connect to database: " + db_database), log_filename)
    log_message.critical_log("message: " + err)
    log_message.info_log("Exit system with reason: No database connection. ", log_filename)
    sys.exit(1)
else:
    # logging info to output file to let the user now the connection to the database has been made
    log_message.info_log(("connected to database: " + db_database), log_filename)
    myCursor = mydb.cursor()


def on_message(client, userdata, message):
    """
    A function to retrieve the message from the things network thats stored in the message buffer.
    If a messge is retrieved, it will set the message flag to True.

    :param client: The client to the things network/ connection
    :param userdata: ??
    :param message: The message buffer where the message is stored until it is retrieved by the program
    """
    # store the payload in a global variable
    global json_data
    global message_flag
    json_data = message.payload
    message_flag = True


def on_connect(client, userdata, flags, rc):
    """
    Function that will check if the program is connected to the things network.
    it will set the connected flag to True if it's connected and False otherwise.

    :param client: The client to the things network/ connection
    :param userdata: ??
    :param flags:
    :param rc: the connection code thats used to check if its conected to the things network
    """

    global connected_flag
    if rc == 0:
        # logging info to output file to let the user now the connection to the MQTT broker has been made
        log_message.info_log(message=("Connected to the MQTT broker: " + mqtt_host), filename=log_filename)
        connected_flag = True
    else:
        # logging critical error to output file to let the user now the connection to the MQTT broker cant be established
        log_message.info_log(message=("A missing connection to the MQTT broker: "+ mqtt_host), filename=log_filename)
        connected_flag = False


def mqtt_connect():
    """
    A function to connect to the things network.
    With the subscribe call, a message will be retrieved and will do a callback to the on_message function

    :return: returns the client its connected to
    """

    client = mqtt.Client("Python")  # create new instance
    client.username_pw_set(username=mqtt_username,
                           password=mqtt_password)  # set username and password
    if mqtt_port == 8883:
        client.tls_set()
        client.tls_insecure_set(False)
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback
    client.loop()
    client.connect(host=mqtt_host, port=mqtt_port, keepalive=60)  # connect to broker

    client.loop_start()  # start the loop
    while not connected_flag:  # Wait for connection
        time.sleep(0.1)

    client.subscribe("#")
    return client


def run():
    """
    This function runs the whole code

    it will exit the program when a keyboard interruptions happens.
    """

    global message_flag
    client1 = mqtt_connect()
    try:
        while True:
            time.sleep(1)
            if message_flag:
                payload, device_id = parser.parse_datavalues(json_data)
                data_values = parser.decode_payload(payload, device_id)  # [0] = device type, [1] = pressure, [2] = light, [3] = temperature, ([4] = batv)
                # check if decoded values are valid
                if data_values is not None:
                    split_device_id = device_id.split("-")
                    date_time = datetime.now()
                    metadata = parser.parse_metadata(json_data, device_id)  # [0] = gateway id, [1] = gateway eui, [2] = rssi, [3] = crssi
                    try:
                        if split_device_id[0] == "py":
                            #data_values, time, metadata
                            statement = "INSERT INTO pysense (log_time,location,temperature,pressure,light) VALUES (?,?,?,?,?)"
                            values = (date_time, split_device_id[1], data_values[3], data_values[1], data_values[2])
                            myCursor.execute(statement, values)
                            statement2 = "INSERT INTO py_metadata (py_log_id,gateway_id,eui,r_signalstrength) VALUES (?,?,?,?)"
                            values2 = ( myCursor.lastrowid, metadata[0], metadata[1], metadata[2])
                            myCursor.execute(statement2, values2)
                        elif split_device_id[0] == "lht":
                            statement = "INSERT INTO dragino(log_time,location,temperature,humidity,light) VALUES (?,?,?,?,?)"
                            values = (date_time,  split_device_id[1], data_values[3], data_values[1], data_values[2])
                            myCursor.execute(statement, values)
                            statement2 = "INSERT INTO dragino_metadata(dragino_id,gateway_id,eui,r_signalstrength) VALUES (?,?,?,?)"
                            values2 = (myCursor.lastrowid, metadata[0], metadata[1], metadata[2])
                            myCursor.execute(statement2, values2)
                    except mariadb.Error as e:
                        # logging a critical error to output file to let the user know a database connection has been lost
                        log_message.warning_log(("A missing connection to the database: " + db_database), log_filename)
                    mydb.commit()
                else:
                    # logging a warning reason to output file to let the user know a unvalid message has been transported over the things network
                    log_message.warning_log(("Payload field consist of unvalid bytes, device: " + device_id), log_filename)

                message_flag = False
    except KeyboardInterrupt:
        # logging exit info to output file to let the user now when system has been shutdown and all the connections are closed
        log_message.info_log("Exit system with reason: Keyboard Interruption.", log_filename)
        client1.disconnect()
        client1.loop_stop()
        log_message.info_log("MQTT connection closed...", log_filename)
        mydb.close()
        log_message.info_log("Database connection closed...", log_filename)
        log_message.info_log("System closed.", log_filename)


if __name__ == '__main__':
    run()
