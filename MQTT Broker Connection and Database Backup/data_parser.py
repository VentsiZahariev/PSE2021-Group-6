#!/usr/bin/python3

# data_parser.py
# Last edit made: 13-01-2022
# Version: 0.2
# Description: This file will parse the json string retrieved from the things network
# Author: Tim ter Steege
# python version used: 3.9

# Import required python libraries
import json
import base64
import binascii
import log_message

# Global variable for the filename for logging messages
log_filename = "mqtt_log.out"

def parse_eui(json, device):
    """
    parse the eui/gateway id value from the json string

    :return: returns the eui/gateway id or None if value does not exists in the json string
    """

    try:
        gateway_eui = json['uplink_message']['rx_metadata'][0]['gateway_ids']['eui']

        return gateway_eui
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Gateway eui is not in string, device_id: " + device))
        return None


def parse_gatewayid(json, device):
    """
    parse the gateway id value from the json string

    :return: returns the gateway id or None if value does not exists in the json string
    """
    try:
        gateway_id = json['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id']

        return gateway_id
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Gateway id is not in string, device_id: " + device))
        return None


def parse_rssi(json, device):
    """
    parse the rssi value from the json string

    :return: returns the rssi or None if value does not exists in the json string
    """
    try:
        gateway_rssi = json['uplink_message']['rx_metadata'][0]['rssi']

        return gateway_rssi
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Gateway rssi is not in string, device_id: " + device))
        return None


def parse_crssi(json, device):
    """
    parse the crssi value from the json string

    :return: returns the crssi or None if value does not exists in the json string
    """
    try:
        gateway_crssi = json['uplink_message']['rx_metadata'][0]['channel_rssi']

        return gateway_crssi
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Gateway channel rssi is not in string, device_id: " + device))
        return None


def parse_payload(json, device):
    """
    parse the encoded payload field that contains the values for temperature, light and pressure/humidity value from the json string

    :return: returns the encooded payload or None if value does not exists in the json string
    """
    try:
        payload = json['uplink_message']['frm_payload']

        return payload
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Payload field is not in string, device_id: " + device))
        return None


def parse_deviceid(json):
    """
    parse the device id value from the json string

    :return: returns the device id or None if value does not exists in the json string
    """
    try:
        device_id = json['end_device_ids']['device_id']
        return device_id
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Device id is not in string, with json:"))
        return None

def parse_latitude(json_str, device):
    """
    parse the latitude value from the json string

    :return: returns the latitude or None if value does not exists in the json string
    """
    try:
        data = json.loads(json_str)
        latitude = data['uplink_message']['rx_metadata'][0]['location']['latitude']
        return latitude
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Device id is not in string, with json: " + device))
        return None


def parse_longitude(json_str, device):
    """
    parse the longitude value from the json string

    :return: returns the longitude or None if value does not exists in the json string
    """
    try:
        data = json.loads(json_str)
        longitude = data['uplink_message']['rx_metadata'][0]['location']['longitude']
        return longitude
    except KeyError:
        # log to file a field is not in string
        log_message.warning_log(("Device id is not in string, with json: " + device))
        return None


def parse_metadata(json_str, device):
    """
    This function parse the json string received from the broker.
    it will get the some metadata from the thigs network message thats stored in the json string

    :return: returns the gateway_id, gateway_eui, gateway_rssi and gateway_channel-rssi as a tuple
    """
    data = json.loads(json_str)

    eui = parse_eui(data, device)
    gateway_id = parse_gatewayid(data, device)
    rssi = parse_rssi(data, device)
    crssi = parse_crssi(data, device)

    return gateway_id, eui, rssi, crssi


def parse_datavalues(json_str):
    """
    This function parse the json string received from the broker.
    it will get the payload field within the json-string,
    wich contains the bytes with the data for the light, pressure and temperature for the py and lht.
    For the lht device, also the battery status.

    In the second part it is also parsing the device id field to retrieve the device id.

    :return: returns the payload field and the id as a tuple
    """

    data = json.loads(json_str)
    device_id = parse_deviceid(data)
    payload = parse_payload(data, device_id)

    return payload, device_id


def decode_payload(payload, device):
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
            light = raw[1]  # ambient light in lux
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
            log_message.warning_log(("Payload field does not contain the correct byte representation, device_id: " + device))
            return None

    except binascii.Error:
        log_message.warning_log(("Payload field does not contain the correct byte representation, device_id: " + device))
        return None