#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser



config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = config["counter"]["address"]
port = config["counter"]["port"]

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
ser = serial.Serial(f"{port}", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
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

def get_porog():
    chunk = b'\x55'   # сетевой адрес
    chunk += b'\x08'  # код запроса
    chunk += b'\x21'  # № параметра
    chunk += b'\x03'  # BWRI (номер вспомогательного параметра)
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    porog = ser.read_all()
    # print(porog)
    return porog


def get_sn():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x00'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(1)
    return

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


def get_current_A():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x21'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    current_A = int(A, 16) / 1000

    return current_A


def get_current_B():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x22'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    current_B = int(A, 16) / 1000

    return current_B


def get_current_C():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x23'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    current_C = int(A, 16) / 1000

    return current_C


def get_P():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x04'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    P = int(A, 16) / 100

    return P


def get_P_A():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x01'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    PA = int(A, 16) / 100

    return PA


def get_P_B():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x02'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    PB = int(A, 16) / 100

    return PB


def get_P_C():
    chunk = b'\x55'
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x03'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    za = list(outa)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    PC = int(A, 16) / 100

    return PC


def get_Q_A():
    chunk = b'\x55'
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
    chunk = b'\x55'
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
    chunk = b'\x55'
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
    chunk = b'\x55'
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
    chunk = b'\x55'
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
    chunk = b'\x55'
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
    chunk = b'\x55'
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


def find_all_voltages():
    connect()
    va = get_voltage_A()
    vb = get_voltage_B()
    vc = get_voltage_C()
    ia = get_current_A()
    ib = get_current_B()
    ic = get_current_C()
    p = get_P()
    pa = get_P_A()
    pb = get_P_B()
    pc = get_P_C()
    qa = get_Q_A()
    qb = get_Q_B()
    qc = get_Q_C()
    s = get_S()
    sa = get_S_A()
    sb = get_S_B()
    sc = get_S_C()
    fw = get_fw_crc()
    disconnect()
    ser.close()
    return va, vb, vc, fw, ia, ib, ic, p, pa, pb, pc, qa, qb, qc, s, sa, sb, sc


print(find_all_voltages())
# connect()
# print("Напряжение фазы А = ", get_voltage_A())
# print("Напряжение фазы В = ", get_voltage_B())
# print("Напряжение фазы С = ", get_voltage_C())
# disconnect()
# ser.close()


