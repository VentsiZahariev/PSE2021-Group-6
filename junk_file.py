

# some really nice peaces of junk code





import base64
import binascii

import mariadb
import sys
from datetime import datetime
import json

#time_date = datetime.now()

#res = isinstance(time_date, datetime)

#print(res)


json_str = b'{"end_device_ids":{"device_id":"py-saxion","application_ids":{"application_id":"project-software-engineering"},"dev_eui":"70B3D5499ED96FBD","join_eui":"70B3D57ED00349D3","dev_addr":"260BB0C6"},"correlation_ids":["as:up:01FNX7WW84FGFK6WY1XNPBACVQ","ns:uplink:01FNX7WW1MRCMWYZRDD4KT9KPJ","pba:conn:up:01FNNEBPY4210J8TSQ8VHX2DN6","pba:uplink:01FNX7WW1JQP84XJJ5X15GJ548","rpc:/ttn.lorawan.v3.GsNs/HandleUplink:01FNX7WW1MATA9708N8NRPYMNC","rpc:/ttn.lorawan.v3.NsAs/HandleUplink:01FNX7WW83P3HJ7M39EZ4DYGDZ"],"received_at":"2021-12-02T09:34:06.596658678Z","uplink_message":{"session_key_id":"AX1riQ6lKOecKWG5/K5bTQ==","f_port":2,"f_cnt":1222,"frm_payload":"W7ErAg==","decoded_payload":{"light":177,"pressure":995.5,"temperature":23.2},"rx_metadata":[{"gateway_ids":{"gateway_id":"packetbroker"},"packet_broker":{"message_id":"01FNX7WW1JQP84XJJ5X15GJ548","forwarder_net_id":"000013","forwarder_tenant_id":"ttnv2","forwarder_cluster_id":"ttn-v2-eu-3","forwarder_gateway_eui":"AA555A000806053F","forwarder_gateway_id":"eui-aa555a000806053f","home_network_net_id":"000013","home_network_tenant_id":"ttn","home_network_cluster_id":"eu1.cloud.thethings.network"},"time":"2021-12-02T09:34:06.372269Z","rssi":-93,"channel_rssi":-93,"snr":5.2,"location":{"latitude":52.22121,"longitude":6.8857374,"altitude":66},"uplink_token":"eyJnIjoiWlhsS2FHSkhZMmxQYVVwQ1RWUkpORkl3VGs1VE1XTnBURU5LYkdKdFRXbFBhVXBDVFZSSk5GSXdUazVKYVhkcFlWaFphVTlwU2xsT2JYTXhUMFprV1ZKWGRHdFNNMnMxVFd4c01FbHBkMmxrUjBadVNXcHZhV1JZV2pST1JYQnVUVlZ2TUdSNlZsRmhWa0p5Vm1zNWVWUkZOV2xSVTBvNUxsTnBTRmg1TmtSdU1HUlFibEZsTm05Sk9EQnFXWGN1WVZCNFJEaG1RbTg0TlRoQk1UQmFWaTV2TkV4SmQwWTRiSGRqV0ZGWlMxZHdhV2x1T1RkTFptY3dNRmhqWW1wT2FEWm9TR2RyVDJremNFbFpZblEyUWxWUWNXVndhMWQ0VFdjeWJHaHZRWFYyTjJsdmQzTTNlVk5sTkVKU1VXUnZOMlkyZWxCWlNraHlaRmRNTlc0d1UzQkpPWFJPU0ZwZlUxOUlOa1oyZWpKdGJURnJZVk53ZG05WVl6Rm5OM3BWVm1wU1RFaFRkMjUzTWpSQ2JsWjJOMnMzYkZWb00xVmFTa2xzVEVOcWEzaFdWR2t3WDI1dFNsRkVTVXR0Ym5wTkxraGZiWEJZT0VwNk1GcFJTVTFPV0RsU01HeEVTbWM9IiwiYSI6eyJmbmlkIjoiMDAwMDEzIiwiZnRpZCI6InR0bnYyIiwiZmNpZCI6InR0bi12Mi1ldS0zIn19"},{"gateway_ids":{"gateway_id":"kerlink-awm-ut","eui":"0000024B080301BF"},"time":"2021-12-02T09:34:06.372273Z","timestamp":1282462044,"rssi":-114,"channel_rssi":-114,"snr":-6.5,"location":{"latitude":52.23997,"longitude":6.85014,"altitude":52,"source":"SOURCE_REGISTRY"},"uplink_token":"ChwKGgoOa2VybGluay1hd20tdXQSCAAAAksIAwG/ENyiw+MEGgwIjqaijQYQw6e2uQEg4J7Hxan6NyoMCI6moo0GEOjewbEB","channel_index":5}],"settings":{"data_rate":{"lora":{"bandwidth":125000,"spreading_factor":7}},"coding_rate":"4/5","frequency":"867500000"},"received_at":"2021-12-02T09:34:06.388945936Z","consumed_airtime":"0.051456s","network_ids":{"net_id":"000013","tenant_id":"ttn","cluster_id":"ttn-eu1"}}}'


#pressure = raw[0] / 2 + 950  # air pressure in mbar
#light = raw[1]  # ambient light in lux???
#temperature = ((raw[2] - 20) * 10 + raw[3]) / 10  # temperature in degree Celcius





#keys = data.keys()
#keys2 = data['uplink_message'].keys()
#keys3 = data['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id']

#newjson = json.loads(keys3[0])

#res = isinstance(data, dict)

#data2 = json.load(keys3)
#print(res)
#print(keys3)
#print(keys3[0]['channel_rssi'])
#print(keys3[0]['gateway_ids']['gateway_id'])
#print(keys3[0]['gateway_ids']['eui'])

#pressure = data['uplink_message']['decoded_payload']['pressure']
#light = data['uplink_message']['decoded_payload']['light']
#temperature = data['uplink_message']['decoded_payload']['temperature']

#gate_way = data[]
#    return pressure, light, temperature

# Decoder for the LHT:
# https://www.dragino.com/downloads/downloads/LHT65/UserManual/LHT65_Temperature_Humidity_Sensor_UserManual_v1.3.\


def decode_py(payload):
    """
    This function is used to decode the raw payload field for the pycom device.

    :param payload: This contains the raw payload retrieved from the json string
    :return: decode data pressure as integer number, light and temperature
    """
    try:
        raw = base64.b64decode(payload)

        if len(raw) == 4:
            pressure = raw[0] / 2 + 950  # air pressure in mbar
            light = raw[1]  # ambient light in lux???
            temperature = ((raw[2] - 20) * 10 + raw[3]) / 10  # temperature in degree Celcius

            return int(pressure), light, temperature
        else:
            return None

    except binascii.Error:
        return None


def decode_lht(payload):
    """
    This function is used to decode the raw payload field for the Dragino LHT65 device.

    :param payload: This contains the raw payload retrieved from the json string
    :return: decoded data pressure as integer number, light, temperature, battery voltage
    """
    try:
        raw = base64.b64decode(payload)

        if len(raw) == 11:
            pressure = (raw[4] << 8 | raw[5]) / 10  # Humidity pressure in %
            light = (raw[7] << 8 | raw[8])  # Illumination in lux
            temperature = (raw[2] << 8 | raw[3]) / 100  # temperature in degree Celcius
            batv = ((raw[0] << 8 | raw[1]) & 0x3FFF) / 1000  # battery voltage in volt

            return int(pressure), light, temperature, batv
        else:
            return None

    except binascii.Error:
        return None


def decode_payload(payload):
    try:
        raw = base64.b64decode(payload)

        if len(raw) == 4:
            pressure = raw[0] / 2 + 950  # air pressure in mbar
            light = raw[1]  # ambient light in lux???
            temperature = ((raw[2] - 20) * 10 + raw[3]) / 10  # temperature in degree Celcius

            payload = pressure, light, temperature

            return "pycom", payload

        elif len(raw) == 11:
            pressure = (raw[4] << 8 | raw[5]) / 10  # Humidity pressure in %
            light = (raw[7] << 8 | raw[8])  # Illumination in lux
            temperature = (raw[2] << 8 | raw[3]) / 100  # temperature in degree Celcius
            batv = ((raw[0] << 8 | raw[1]) & 0x3FFF) / 1000  # battery voltage in volt

            payload = pressure, light, temperature, batv
            return "lht", payload

        else:
            return None

    except binascii.Error:
        return None

payload8 = "y+UCXAN1BQRdf/8="
payload4 = "W7ErAg=="
payload1 = "ebfbe"

payload = decode_payload(payload1)


print(payload)