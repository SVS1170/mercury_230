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
# addr = struct.pack('B', address)
port = config["counter"]["port"]

m230c = m230(address, port)
m230c.connect()
print(m230c.get_P())
print(m230c.get_voltage_C())




def get_Q_A():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x05'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    QA = int(A, 16) / 100

    return QA


def get_Q_B():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x06'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    QB = int(A, 16) / 100

    return QB


def get_Q_C():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x07'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    QC = int(A, 16) / 100

    return QC


def get_S():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x08'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    S = int(A, 16) / 100

    return S


def get_S_A():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x09'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    SA = int(A, 16) / 100

    return SA


def get_S_B():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x0a'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    SB = int(A, 16) / 100

    return SB


def get_S_C():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x0b'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    SC = int(A, 16) / 100

    return SC


def get_PF():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x30'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    # za = list(outa)
    # lenga = len(za)
    # a1 = za[lenga - 3]
    # a2 = za[lenga - 4]
    # A = format(a1, 'x') + format(a2, 'x')
    # PF = int(A, 16) / 1000
    PF = outa
    return PF


def get_PF_A():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x31'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    # za = list(outa)
    # lenga = len(za)
    # a1 = za[lenga - 3]
    # a2 = za[lenga - 4]
    # A = format(a1, 'x') + format(a2, 'x')
    # PF_A = int(A, 16) / 1000
    PF_A = outa
    return PF_A


def get_PF_B():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x32'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    # za = list(outa)
    # lenga = len(za)
    # a1 = za[lenga - 3]
    # a2 = za[lenga - 4]
    # A = format(a1, 'x') + format(a2, 'x')
    # PF_B = int(A, 16) / 1000
    PF_B = outa
    return PF_B


def get_PF_C():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x33'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    # za = list(outa)
    # lenga = len(za)
    # a1 = za[lenga - 3]
    # a2 = za[lenga - 4]
    # A = format(a1, 'x') + format(a2, 'x')
    # PF_C = int(A, 16) / 1000
    PF_C = outa
    return PF_C


