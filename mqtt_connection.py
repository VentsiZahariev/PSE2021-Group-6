#!/usr/bin/python3

# mqtt_connection.py
# Last edit made: 10-12-2021
# Version: 0.2
# Subject: Code to retrieve data from the things network and store it to the database
# Author: Tim ter Steege
# python version used: 3.9

import binascii
import sys
import mariadb as mariadb
import paho.mqtt.client as mqtt
import time
import base64
from datetime import datetime

import data_parser as parser
import logger

# global variable to hold temporarily 1 message from the broker, this will be the json line
json_data = None
# global variable flag for the status of a newly received message
message_flag = False
# global variable flag for connection status
connected_flag = False

try:
    host_db = "127.0.0.1"
    user_db = "PSEgroup6"
    password_db = "battlefield4"
    port_db = 3306
    db = "weather_log"
    mydb = mariadb.connect(user=user_db, password=password_db, host=host_db, port=port_db, database=db)
except mariadb.Error as err:
    logger.log.error_log("cant connect to database")
    sys.exit(1)
else:
    logger.log.debug_log("connected to database")
    myCursor=mydb.cursor()

# Global variables with credentials for login to mqtt-broker
host = "eu1.cloud.thethings.network"  # Broker address/host
# port = 1883  # Normal broker port
port = 8883  # Encrypted broker port
# Broker username
username = "project-software-engineering@ttn"
# Broker password
password = "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"


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
        logger.log.debug_log("Connected with result code")
        connected_flag = True
    else:
        logger.log.debug_log("Not connected with result code")
        connected_flag = False


def mqtt_connect():
    """
    A function to connect to the things network.
    With the subscribe call, a message will be retrieved and will do a callback to the on_message function

    :return: returns the client its connected to
    """
    client = mqtt.Client("Python")  # create new instance
    client.username_pw_set(username=username,
                           password=password)  # set username and password
    if port == 8883:
        client.tls_set()
        client.tls_insecure_set(False)
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback
    client.loop()
    client.connect(host=host, port=port, keepalive=60)  # connect to broker

    client.loop_start()  # start the loop
    while not connected_flag:  # Wait for connection
        time.sleep(0.1)

    client.subscribe("#")
    return client


def decode_payload(payload):
    """
    This function is used to decode the raw payload field for the pycom device.
    This function is used to decode the raw payload field for the Dragino LHT65 device.

    :param payload: This contains the raw payload retrieved from the json string
    :return: it will return "pycom", pressure, light, temperature when payload contains 4 bytes
            it will return "lht", pressure, light, temperature, batv when payload contains 11 bytes
            it will return None when otherwise or a binascii.Error (when the payload can not be decoded) happens
    """
    try:
        raw = base64.b64decode(payload)

        if len(raw) == 4:
            pressure = raw[0] / 2 + 950  # air pressure in mbar
            light = raw[1]  # ambient light in lux???
            temperature = ((raw[2] - 20) * 10 + raw[3]) / 10  # temperature in degree Celcius

            return "pycom", pressure, light, temperature

        elif len(raw) == 11:
            pressure = (raw[4] << 8 | raw[5]) / 10  # Humidity pressure in %

            light = (raw[7] << 8 | raw[8])  # Illumination in lux

            temperature = (raw[2] << 8 | raw[3])  # temperature in degree Celcius
            if raw[2] & 0x80:
                temperature = temperature - (1 << 16)
            temperature = temperature/100

            batv = ((raw[0] << 8 | raw[1]) & 0x3FFF) / 1000  # battery voltage in volt

            return "lht", pressure, light, temperature, batv

        else:
            return None

    except binascii.Error:
        return None


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
                payload, device_id = parser.data_parser.parse_datavalues(json_data)
                data_values = decode_payload(payload)  # [0] = device name, [1] = pressure, [2] = light, [3] = temperature, ([4] = batv)
                # check if decoded values are valid
                if data_values is not None:
                    split_device_id = device_id.split("-")
                    date_time = datetime.now()
                    metadata = parser.data_parser.parse_metadata(json_data)  # [0] = gateway id, [1] = gateway eui, [2] = rssi, [3] = crssi
                    try:
                        if split_device_id[0]=="py":
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
                        logger.log.error_log("not connected to database")  # logging to file
                    mydb.commit()
                else:
                    logger.log.debug_log("Device is not supported.") #logging to file

                message_flag = False
    except KeyboardInterrupt:
        logger.log.debug_log("Exiting") #logging to file
        client1.disconnect()
        client1.loop_stop()
        mydb.close()


if __name__ == '__main__':
    run()
