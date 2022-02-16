#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser
from bitstring import BitArray

# config = configparser.ConfigParser()
# config.read("config.ini")  # читаем конфиг
# address = int(config["counter"]["address"])
# address = chr(address)
# addr = struct.pack('B', address)
# port = config["counter"]["port"]


class Mercury230:
    def __init__(self, address, port):
        self.addr = struct.pack('B', address)
        self.port1 = port

    # def open_port():
    #     ser = serial.Serial(f"{port}", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
    #     print('Connected:', ser.isOpen())
    #     return ser
    def open_port(self, port1):
        ser = serial.Serial(f"{port1}", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        # print('Connected:', ser.isOpen())
        return ser


    def test_hex_to_bin(self):
        # a = addr
        a = b"\x80\x00\x40\xE7\x29\x00\x40\xE7\x29\x00\x00\x00\x00\x00\x00\x00\x0f"
        mybyte = bytes(a)
        # c = BitArray(hex=mbyte)
        d = self.crc16(mybyte)
        # ab = c.bin[2:]
        binary_string = "{:08b}".format(int(mybyte.hex(), 16))
        bd = list(binary_string)

        print(bd, d)

    def crc16(self, data):
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

    def connection_test(self):
        chunk = self.addr
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)

    def search_counter(self):
        chunk = b'\x00'
        chunk += b'\x08'
        chunk += b'\x05'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        dat = ser.read_all()
        zdat = list(dat)
        lengzdat = len(zdat)
        a1 = zdat[lengzdat - 3]
        # rs485addr = int(a1, 16)
        rs485addr = a1
        # print(a1)
        # print(rs485addr)
        return rs485addr

    def disconnect(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x02'  # код запроса
        chunk = self.crc16(chunk)
        # print("transmited : ",chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        # print("disconnect")
        return "ok"

    def connect(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x01'  # код запроса
        chunk += b'\x01'  # код уровня доступа
        chunk += b'\x01'  # 1 символ пароля
        chunk += b'\x01'  # 2 символ пароля
        chunk += b'\x01'  # 3 символ пароля
        chunk += b'\x01'  # 4 символ пароля
        chunk += b'\x01'  # 5 символ пароля
        chunk += b'\x01'  # 6 символ пароля
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        # print("connect")

    def get_FW_version(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x03'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
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
        version = str(ver3) + "." + str(ver2) + "." + str(ver1)
        print(zver)
        print(version)
        return version

    def get_time(self):
        chunk = addr  # сетевой адрес
        chunk += b'\x04'  # код запроса
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        tim = ser.read_all()
        return tim

    def get_fw_crc(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x26'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        fw_crc = ser.read_all()
        return fw_crc

    def get_porog(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x21'  # № параметра
        chunk += b'\x03'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        porog = ser.read_all()
        # print(porog)
        return porog

    def get_sn(self):
        chunk = addr
        chunk += b'\x08'
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(1)
        return

    def get_temp(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x70'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
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

    def get_frequency(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x40'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        temp = ser.read_all()
        za = list(temp)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        frequency = int(A, 16) / 100
        return frequency

    # запрос напряжения
    def get_voltage_A(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x11'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        za = list(outa)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        voltage_A = int(A, 16) / 100
        return voltage_A

    def get_voltage_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x11'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        za = list(outa)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        voltage_B = int(A, 16) / 100
        return voltage_B

    def get_voltage_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x13'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        za = list(outa)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        voltage_C = int(A, 16) / 100
        return voltage_C

    def get_current_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x21'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        za = list(outa)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        current_A = int(A, 16) / 1000
        return current_A

    def get_current_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x22'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        za = list(outa)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        current_B = int(A, 16) / 1000
        return current_B

    def get_current_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x23'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        za = list(outa)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        A = format(a1, 'x') + format(a2, 'x')
        current_C = int(A, 16) / 1000
        return current_C

    def get_P(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
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
        return P

    def get_P_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x01'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
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
        PA = int(A, 16) / 100
        return PA

    def get_P_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x02'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
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
        PB = int(A, 16) / 100
        return PB

    def get_P_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x03'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.port1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
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
        PC = int(A, 16) / 100
        return PC



# merc = Mercury230(address, port)
# print(merc.search_counter())
# # mercury230.get_P()