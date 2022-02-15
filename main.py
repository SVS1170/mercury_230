#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser
from bitstring import BitArray



config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = int(config["counter"]["address"])
# address = chr(address)
addr = struct.pack('B', address)
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


def test_hex_to_bin():
    a = b"\xff"
    # a = b"\x80\x00\x40\xE7\x29\x00\x40\xE7\x29\x00\x00\x00\x00\x00\x00\x00\x0f"
    mybyte = bytes(a)
    # c = BitArray(hex=mbyte)
    # ab = c.bin[2:]
    binary_string = "{:08b}".format(int(mybyte.hex(), 16))
    bd = list(binary_string)
    print(bd)


def connection_test():
    chunk = addr
    chunk += b'\x00'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)


def search_counter():
    chunk = b'\x00'
    chunk += b'\x08'
    chunk += b'\x05'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100 / 1000)
    dat = ser.read_all()
    zdat = list(dat)
    lengzdat = len(zdat)
    a1 = zdat[lengzdat - 3]
    rs485addr = int(a1, 16)
    print(a1)
    print(rs485addr)
    return rs485addr



def disconnect():
    chunk = addr      # сетевой адрес
    chunk += b'\x02'     # код запроса
    chunk = crc16(chunk)
    # print("transmited : ",chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    # print("disconnect")
    return "ok"


def connect():
    chunk = addr   # сетевой адрес
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


def get_FW_version():
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x03'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100 / 1000)
    ver = ser.read_all()
    zver = list(ver)
    lengzver = len(zver)
    a1 = zver[lengzver - 3]
    a2 = zver[lengzver - 4]
    a3 = zver[lengzver - 5]
    ver1 = int(a1, 16)
    ver2 = int(a2, 16)
    ver3 = int(a3, 16)
    version = str(ver3) +"."+ str(ver2) +"."+ str(ver1)
    print(zver)
    print(version)
    return version

def get_time():
    chunk = addr    # сетевой адрес
    chunk += b'\x04'   # код запроса
    chunk += b'\x00'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    tim = ser.read_all()
    return tim

def get_fw_crc():
    chunk =addr    # сетевой адрес
    chunk += b'\x08'   # код запроса
    chunk += b'\x26'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    fw_crc = ser.read_all()
    return fw_crc

def get_porog():
    chunk = addr   # сетевой адрес
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
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x00'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(1)
    return


def get_temp():
    chunk = addr  # сетевой адрес
    chunk += b'\x08'  # код запроса
    chunk += b'\x11'  # № параметра
    chunk += b'\x70'  # BWRI (номер вспомогательного параметра)
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100 / 1000)
    temp = ser.read_all()
    za = list(temp)
    lenga = len(za)
    print(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    temp = int(A, 16)
    return temp


def get_frequency():
    chunk = addr  # сетевой адрес
    chunk += b'\x08'  # код запроса
    chunk += b'\x11'  # № параметра
    chunk += b'\x40'  # BWRI (номер вспомогательного параметра)
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100 / 1000)
    temp = ser.read_all()
    za = list(temp)
    lenga = len(za)
    a1 = za[lenga - 3]
    a2 = za[lenga - 4]
    A = format(a1, 'x') + format(a2, 'x')
    frequency = int(A, 16)/100
    return frequency


# запрос напряжения
def get_voltage_A():
    chunk = addr   # сетевой адрес
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
    chunk = addr
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
    chunk = addr
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
    chunk = addr
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
    chunk = addr
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
    chunk = addr
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
    chunk = addr
    chunk += b'\x08'
    chunk += b'\x11'
    chunk += b'\x04'
    chunk = crc16(chunk)
    ser.write(chunk)
    time.sleep(100/1000)
    outa = ser.read_all()
    # outa = b"\x80\x00\x40\xE7\x29\x00\x40\xE7\x29\x00\x00\x00\x70\xf1\xff\x00\x0f"
    za = list(outa)
    lenga = len(za)
    a2 = za[lenga - 3]
    a3 = za[lenga - 4]
    a1a = za[lenga - 5]
    mybyte = a1a
    binary_string = "{:08b}".format(int(mybyte))
    bd = list(binary_string)
    AR = bd[0]
    RR = bd[1]
    a1 = ''.join(bd[2:8])
    a1b = hex(int(a1, 2))
    A = a1b + format(a2, 'x') + format(a3, 'x')
    P = int(A, 16) / 100
    print(P)
    return P


def get_P_A():
    chunk = addr
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
    chunk = addr
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
    chunk = addr
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
    pf = get_PF()
    pfa = get_PF_A()
    pfb = get_PF_B()
    pfc = get_PF_C()
    fw = get_fw_crc()
    disconnect()
    ser.close()
    return va, vb, vc, fw, ia, ib, ic, p, pa, pb, pc, qa, qb, qc, s, sa, sb, sc, pf, pfa, pfb, pfc

connect()
get_P()
# print(find_all_voltages())
# print(get_temp())
# connection_test()
# print("Напряжение фазы А = ", get_voltage_A())
# print("Напряжение фазы В = ", get_voltage_B())
# print("Напряжение фазы С = ", get_voltage_C())
# disconnect()
# ser.close()
# test_hex_to_bin()


