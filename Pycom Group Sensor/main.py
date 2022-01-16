from network import LoRa
import socket
import time
import ubinascii
import struct

import pycom
from pycoproc_1 import Pycoproc
import machine
import micropython
import math

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

py = Pycoproc(Pycoproc.PYSENSE)

pycom.heartbeat(False)

while True:
    # Initialise LoRa in LORAWAN mode.
    # Please pick the region that matches where you are using the device:
    # Europe = LoRa.EU868
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    # create an OTAA authentication parameters, change them to the provided credentials
    app_eui = ubinascii.unhexlify('6A54DF51AFD651A6')
    app_key = ubinascii.unhexlify('827AA9994E970D34A267BA21C5893DC5')
    #uncomment to use LoRaWAN application provided dev_eui
    #dev_eui = ubinascii.unhexlify('70B3D549938EA1EE')

    # join a network using OTAA (Over the Air Activation)
    #uncomment below to use LoRaWAN application provided dev_eui
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    #lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

    # wait until the module has joined the network
    while not lora.has_joined():
        pycom.rgbled(0xFF0000)
        time.sleep(2.5)
        print('Not yet joined...')

    print('Joined')
    pycom.rgbled(0x00FF00)
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    # print("MPL3115A2 temperature: " + str(mp.temperature()*0.75))
    # print("Altitude: " + str(mp.altitude()))
    mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    # print("Pressure: " + str(mpp.pressure()/1000))
    # send some data
    lt = LTR329ALS01(py)
    print("Light (channel Blue lux + channel Red lux): " + str(lt.light()))

    test_light = lt.light()[0] + lt.light()[1]
    print("Test light: ", test_light)
    test_lightVal = hex(test_light)
    test_press = int((mpp.pressure()/100)-950)
    # print("Test press: ", test_press)
    frac, whole = math.modf((mp.temperature()*0.75))
    test_temperature_frac = int(frac*100)
    test_temperature_whole = int(whole)
    print("whole:" ,test_temperature_whole)
    print("frac:" ,test_temperature_frac)
    # test_tempVal = hex(test_temperature_whole)
    # test_pressVal = hex(test_press)

    s.send(bytes([test_press,test_light,test_temperature_whole,test_temperature_frac]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
 
    s.setblocking(False)
    time.sleep(300)

