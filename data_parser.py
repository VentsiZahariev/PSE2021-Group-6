# Last edit made: 02-12-2021
# Version: 0.1
# Subject: This file will parse the json string retrieved from the things network
# Author: Tim ter Steege
# python version used: 3.9

import json


class data_parser:
    def parse_eui(self):
        try:
            gateway_eui = self['uplink_message']['rx_metadata'][0]['gateway_ids']['eui']

            return gateway_eui
        except KeyError:
            return None

    def parse_gatewayid(self):
        try:
            gateway_id = self['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id']

            return gateway_id
        except KeyError:
            return None

    def parse_rssi(self):
        try:
            gateway_rssi = self['uplink_message']['rx_metadata'][0]['rssi']

            return gateway_rssi
        except KeyError:
            return None

    def parse_crssi(self):
        try:
            gateway_crssi = self['uplink_message']['rx_metadata'][0]['channel_rssi']

            return gateway_crssi
        except KeyError:
            return None

    def parse_payload(self):
        try:
            payload = self['uplink_message']['frm_payload']

            return payload
        except KeyError:
            return None

    def parse_deviceid(self):
        try:
            device_id = self['end_device_ids']['device_id']
            return device_id
        except KeyError:
            return None

    def parse_metadata(self):
        """
        This function parse the json string received from the broker.
        it will get the some metadata from the thigs network message thats stored in the json string

        :return: returns the gateway_id, gateway_eui, gateway_rssi and gateway_channel-rssi as a tuple
        """
        data = json.loads(self)
        eui = data_parser.parse_eui(data)
        gateway_id = data_parser.parse_gatewayid(data)
        rssi = data_parser.parse_rssi(data)
        crssi = data_parser.parse_crssi(data)

        return gateway_id, eui, rssi, crssi

    def parse_datavalues(self):
        """
        This function parse the json string received from the broker.
        it will get the payload field within the json-string,
        wich contains the bytes with the data for the light, pressure and temperature for the py and lht.
        For the lht device, also the battery status.

        In the second part it is also parsing the device id field to retrieve the device id.

        :return: returns the payload field and the id as a tuple
        """

        data = json.loads(self)
        payload = data_parser.parse_payload(data)
        device_id = data_parser.parse_deviceid(data)
        return payload, device_id
