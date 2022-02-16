#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser
from mercury230 import Mercury230 as m230
from bitstring import BitArray

config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = int(config["counter"]["address"])
# address = chr(address)
addr = struct.pack('B', address)
port = config["counter"]["port"]

m230c = m230(address, port)
# print(m230c.search_counter())
m230c.connect()
print(m230c.get_S())
# print(m230c.get_voltage_C())



