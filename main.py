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
# print(mercury_234.get_S())
print("Ua : ", mercury_234.get_voltage_A(), ", Ub : ", mercury_234.get_voltage_B(), ", Uc : ", mercury_234.get_voltage_C())
# print()
# print()
print("Ia : ", mercury_234.get_current_A(), ", Ib : ", mercury_234.get_current_B(), ", Ic : ", mercury_234.get_current_C())
# print()
# print()
# print(mercury_234.search_counter())
# print(mercury_234.get_parametres())
# print(mercury_234.get_caseopen())
print("summPa,Pb,Pc :", mercury_234.get_active_energy_phases())
# print(mercury_234.get_active_energy_last_day())
# print(mercury_234.get_active_energy_current_day())
mercury_234.disconnect()
