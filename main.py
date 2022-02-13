#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import serial
import struct
import time

address = 85


def crc16(data):
    crc = 0xFFFF
    l = len(data)
    i = 0
    while i < l:
        j = 0
        crc = crc ^ data[i]
        while j < 8:
            if (crc & 0x1):
                mask = 0xA001
            else:
                mask = 0x00
            crc = ((crc >> 1) & 0x7FFF) ^ mask
            j += 1
        i += 1
    if crc < 0:
        crc -= 256
    result = data + chr(crc % 256).encode('latin-1') + chr(crc // 256).encode('latin-1')
    return result


# Open serial port
ser = serial.Serial("COM5", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
print('Connected:', ser.isOpen())


def connection_test():
    chunk = b'\x55'
    chunk += b'\x00'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)



def disconnect():
    chunk = b'\x55'      # сетевой адрес
    chunk += b'\x02'     # код запроса
    chunk = crc16(chunk)
    # print("transmited : ",chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    # print("disconnect")
    return "ok"


def connect():
    chunk = b'\x55'    # сетевой адрес
    chunk += b'\x01'   # код запроса
    chunk += b'\x01'   # код уровня доступа
    chunk += b'\x01'   # 1 символ пароля
    chunk += b'\x01'   # 2 символ пароля
    chunk += b'\x01'   # 3 символ пароля
    chunk += b'\x01'   # 4 символ пароля
    chunk += b'\x01'   # 5 символ пароля
    chunk += b'\x01'   # 6 символ пароля
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    # print("connect")


def get_time():
    chunk = b'\x55'    # сетевой адрес
    chunk += b'\x04'   # код запроса
    chunk += b'\x00'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    tim = ser.read_all()
    return tim

def get_fw_crc():
    chunk = b'\x55'    # сетевой адрес
    chunk += b'\x08'   # код запроса
    chunk += b'\x26'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    fw_crc = ser.read_all()
    return fw_crc


# def get_sn():
#     chunk = b'\x55'
#     chunk += b'\x08'
#     chunk += b'\x00'
#     chunk = crc16(chunk)
#     ser.write(chunk)
#     time.sleep(1)
#     return

# запрос напряжения
def get_voltage_A():
    chunk = b'\x55'   # сетевой адрес
    chunk += b'\x08'  # код запроса
    chunk += b'\x11'  # № параметра
    chunk += b'\x11'  # BWRI (номер вспомогательного параметра)
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    voltage_A = int(A, 16) / 100
    return voltage_A


def get_voltage_B():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x11'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    voltage_B = int(A, 16) / 100

    return voltage_B


def get_voltage_C():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x13'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    voltage_C = int(A, 16) / 100

    return voltage_C

def find_all_voltages():
    connect()
    va = get_voltage_A()
    vb = get_voltage_B()
    vc = get_voltage_C()
    fw = get_fw_crc()
    disconnect()
    ser.close()
    return va, vb, vc, fw


print(find_all_voltages())
# connect()
# print("Напряжение фазы А = ", get_voltage_A())
# print("Напряжение фазы В = ", get_voltage_B())
# print("Напряжение фазы С = ", get_voltage_C())
# disconnect()
# ser.close()


