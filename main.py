#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser
from mercury230 import Mercury230
from bitstring import BitArray

config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = int(config["counter"]["address"])
# address = chr(address)
addr = struct.pack('B', address)
port = config["counter"]["port"]

mercury_234 = Mercury230(address, port)
# print(m230c.search_counter())
# ser.close()
mercury_234.connect()
# print(m230c.get_S())
# m230.get_aux_fast()
print(mercury_234.get_voltage_A())
print(mercury_234.get_voltage_B())
print(mercury_234.get_voltage_C())
print(mercury_234.get_current_A())
print(mercury_234.get_current_B())
print(mercury_234.get_current_C())
print(mercury_234.search_counter())
# print(mercury_234.get_parametres())
print(mercury_234.get_caseopen())
mercury_234.disconnect()
