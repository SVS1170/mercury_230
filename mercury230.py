#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import serial
import struct
import time
import configparser
from bitstring import BitArray

#ser = open_port(self.ipaddress1, self.ipport1)
#ser.timeout = 0.1

class Mercury230:
    def __init__(self, address, ipaddress, ipport):
        self.addr = struct.pack('B', address)
        self.ipaddress1 = ipaddress
        self.ipport1 = ipport
#        ser = self.open_port(self.ipaddress1, self.ipport1)
#        ser.timeout = 0.1

    def open_port(self, ipaddress1, ipport1):
#        ser = serial.Serial(f"{port1}", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        ser = serial.serial_for_url("socket://" + ipaddress1 + ":" + ipport1)
        return ser

    def test_hex_to_bin(self):
        # a = addr
        a = b"\x80\x00\x40\xE7\x29\x00\x40\xE7\x29\x00\x00\x00\x00\x00\x00\x00\x0f"
        mybyte = bytes(a)
        d = self.crc16(mybyte)
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
        print(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        print ('Connected:', ser.isOpen())
        ser.write(chunk)
#        time.sleep(100 / 1000)
#        bytesToRead = ser.inWaiting()
        dat = ser.read(4)
        print(dat)

    def search_counter(self):
        # addr = self.addr
        chunk = b'\x00'
        chunk += b'\x08'
        chunk += b'\x05'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        return rs485addr, zdat

    def disconnect(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x02'  # код запроса
        chunk = self.crc16(chunk)
        # print("transmited : ",chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        # print("disconnect")
        return "ok"

    def connect_user(self):
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
#        time.sleep(100 / 1000)
        # print("connect")

    def connect_admin(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x01'  # код запроса
        chunk += b'\x02'  # код уровня доступа
        chunk += b'\x02'  # 1 символ пароля
        chunk += b'\x02'  # 2 символ пароля
        chunk += b'\x02'  # 3 символ пароля
        chunk += b'\x02'  # 4 символ пароля
        chunk += b'\x02'  # 5 символ пароля
        chunk += b'\x02'  # 6 символ пароля
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        # print("connect")

    def get_FW_version(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x03'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        zver = list(ver)
        lengzver = len(zver)
        a1 = zver[lengzver - 3]
        a2 = zver[lengzver - 4]
        a3 = zver[lengzver - 5]
        ver1 = int(a1)
        ver2 = int(a2)
        ver3 = int(a3)
        version = str(ver3) + "." + str(ver2) + "." + str(ver1)
        # print(zver)
        # print(version)
        return version

    def get_active_energy_current_day(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\xC0'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        za = list(ver)
        # print(za)
        lengza = len(za)
        a0 = za[lengza - 15]
        a1 = za[lengza - 16]
        a2 = za[lengza - 17]
        a3 = za[lengza - 18]
        A = format(a3, 'x') + format(a2, 'x') + format(a0, 'x') + format(a1, 'x')
        P = int(A, 16) / 1000
        return P

    def get_active_energy_last_day(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\xD0'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        za = list(ver)
        # print(za)
        lengza = len(za)
        a0 = za[lengza - 15]
        a1 = za[lengza - 16]
        a2 = za[lengza - 17]
        a3 = za[lengza - 18]
        A = format(a3, 'x') + format(a2, 'x') + format(a0, 'x') + format(a1, 'x')
        P = int(A, 16) / 1000
        return P

    def get_active_energy_phases(self):
        chunk = self.addr
        chunk += b'\x05'  # чтение массивов накопленной энергии
        chunk += b'\x60'  # на начало текущих суток
        chunk += b'\x00'  # по тарифу№ (по сумме тарифов - 0)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        za = list(ver)
        # print(za)
        lengza = len(za)
        a0 = za[lengza - 11]
        a1 = za[lengza - 12]
        a2 = za[lengza - 13]
        a3 = za[lengza - 14]
        A = format(a2, 'x') + format(a3, 'x') + format(a0, 'x') + format(a1, 'x')
        PA = int(A, 16) / 1000
        b0 = za[lengza - 7]
        b1 = za[lengza - 8]
        b2 = za[lengza - 9]
        b3 = za[lengza - 10]
        B = format(b2, 'x') + format(b3, 'x') + format(b0, 'x') + format(b1, 'x')
        PB = int(B, 16) / 1000
        c0 = za[lengza - 3]
        c1 = za[lengza - 4]
        c2 = za[lengza - 5]
        c3 = za[lengza - 6]
        C = format(c2, 'x') + format(c3, 'x') + format(c0, 'x') + format(c1, 'x')
        PC = int(C, 16) / 1000
        return PA, PB, PC

    def get_parametres(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x01'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        ver = ser.read_all()
        zver = list(ver)
        lengzver = len(zver)
        isp1 = zver[lengzver - 3]
        isp2 = zver[lengzver - 4]
        isp3 = zver[lengzver - 5]
        isp4 = zver[lengzver - 6]
        isp5 = zver[lengzver - 7]
        isp6 = zver[lengzver - 8]
        ver1 = zver[lengzver - 9]
        ver2 = zver[lengzver - 10]
        ver3 = zver[lengzver - 11]
        var1 = int(isp1)
        var2 = int(isp2)
        var3 = int(isp3)
        var4 = int(isp4)
        var5 = int(isp5)
        var6 = int(isp6)
        vers1 = int(ver1)
        vers2 = int(ver2)
        vers3 = int(ver3)
        # version = str(ver3) + "." + str(ver2) + "." + str(ver1)
        # print(zver)
        # print(version)
        return zver

    def get_time(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x04'  # код запроса
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        tim = ser.read_all()
        return tim

    def get_fw_crc(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x26'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        porog = ser.read_all()
        # print(porog)
        return porog

    def get_sn(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x00'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(1)
        sn = ser.read_all()
        sn = list(sn)
        lengsn = len(sn)
        a1 = sn[lengsn - 6]
        a2 = sn[lengsn - 7]
        a3 = sn[lengsn - 8]
        a4 = sn[lengsn - 9]
        a5 = sn[lengsn - 5]
        a6 = sn[lengsn - 4]
        a7 = sn[lengsn - 3]
        sn1 = int(a1)
        sn2 = int(a2)
        sn3 = int(a3)
        sn4 = int(a4)
        sn = str(sn4) + str(sn3) + str(sn2) + str(sn1)
        md1 = int(a5)
        md2 = int(a6)
        md3 = int(a7)
        manufacture_date = str(md1) + "." + str(md2) + "." + str(md3)
        return sn, manufacture_date

    def get_temp(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x70'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        temp = ser.read_all()
        za = list(temp)
        temp = int(za[2])
        return temp

    def get_caseopen(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x04'  # код запроса
        chunk += b'\x12'  # № параметра
        chunk += b'\x00'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        open = ser.read_all()
        open = list(open)
        lengopen = len(open)
        clYY = open[lengopen - 3]
        clYY = format(clYY, 'x')
        clMM = open[lengopen - 4]
        clMM = format(clMM, 'x')
        clDD = open[lengopen - 5]
        clDD = format(clDD, 'x')
        clhh = open[lengopen - 6]
        clhh = format(clhh, 'x')
        clmm = open[lengopen - 7]
        clmm = format(clmm, 'x')
        clss = open[lengopen - 8]
        clss = format(clss, 'x')
        openYY = open[lengopen - 9]
        openYY = format(openYY, 'x')
        openMM = open[lengopen - 10]
        openMM = format(openMM, 'x')
        openDD = open[lengopen - 11]
        openDD = format(openDD, 'x')
        openhh = open[lengopen - 12]
        openhh = format(openhh, 'x')
        openmm = open[lengopen - 13]
        openmm = format(openmm, 'x')
        openss = open[lengopen - 14]
        openss = format(openss, 'x')

        return "case opened : ", openhh, openmm, openss, openYY, openMM, openDD, "\rn", "case closed : ", clhh, clmm, clss, clYY, clMM, clDD

    def get_frequency(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x40'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        temp = ser.read_all()
        za = list(temp)
        lenga = len(za)
        a1 = za[lenga - 3]
        a2 = za[lenga - 4]
        f = format(a1, 'x') + format(a2, 'x')
        frequency = int(f, 16) / 100
        return frequency

    # for mercury 234
    def get_aux_fast(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'
        chunk += b'\x16'
        chunk += b'\xA0'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outdata = ser.read_all()
        print(outdata)

        # return outdata

    # запрос напряжения
    def get_voltage_A(self):
        chunk = self.addr  # сетевой адрес
        chunk += b'\x08'  # код запроса
        chunk += b'\x11'  # № параметра
        chunk += b'\x11'  # BWRI (номер вспомогательного параметра)
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
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
        chunk += b'\x12'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.timeout = 0.2
        ser.write(chunk)
#        time.sleep(100 / 1000)
        outa = ser.read(6)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        k = -1
        PA = int(A, 16) / 100
        if AR:
            PA = PA * k
        return PA

    def get_P_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x02'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        k = -1
        if AR:
            PB = PB * k
        return PB

    def get_P_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x03'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        k = -1
        if AR:
            PC = PC * k
        return PC

    def get_Q(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x04'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        Q = int(A, 16) / 100
        k = -1
        if RR:
            Q = Q * k
        return Q

    def get_Q_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x05'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        QA = int(A, 16) / 100
        k = -1
        if RR:
            QA = QA * k
        return QA

    def get_Q_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x06'
        # chunk = self.crc16(chunk)
        # ser = self.open_port(self.ipaddress1, self.ipport1)
        # time.sleep(100 / 1000)
        # outa = ser.read_all()
        # za = list(outa)
        # lenga = len(za)
        # a1 = za[lenga - 3]
        # a2 = za[lenga - 4]
        # A = format(a1, 'x') + format(a2, 'x')
        # QB = int(A, 16) / 100
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        QB = int(A, 16) / 100
        k = -1
        if RR:
            QB = QB * k
        return QB

    def get_Q_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x07'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        QC = int(A, 16) / 100
        k = -1
        if RR:
            QC = QC * k
        return QC

    def get_S(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x08'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        S = int(A, 16) / 100

        return S

    def get_S_A(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x09'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        SA = int(A, 16) / 100

        return SA

    def get_S_B(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x0a'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
        ser.write(chunk)
        time.sleep(100 / 1000)
        outa = ser.read_all()
        # za = list(outa)
        # lenga = len(za)
        # a1 = za[lenga - 3]
        # a2 = za[lenga - 4]
        # A = format(a1, 'x') + format(a2, 'x')
        # SB = int(A, 16) / 100
        # chunk = self.crc16(chunk)
        # ser = self.open_port(self.ipaddress1, self.ipport1)
        # ser.write(chunk)
        # time.sleep(100 / 1000)
        # outa = ser.read_all()
        # print(outa)
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
        SB = int(A, 16) / 100
        return SB

    def get_S_C(self):
        chunk = self.addr
        chunk += b'\x08'
        chunk += b'\x11'
        chunk += b'\x0b'
        chunk = self.crc16(chunk)
        ser = self.open_port(self.ipaddress1, self.ipport1)
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
        SC = int(A, 16) / 100
        return SC

    # def get_PF(self):
    #     chunk = b'\x55'
    #     chunk += b'\x08'
    #     chunk += b'\x11'
    #     chunk += b'\x30'
    #     chunk = self.crc16(chunk)
    #     ser = self.open_port(self.ipaddress1, self.ipport1)
    #     time.sleep(100/1000)
    #     outa = ser.read_all()
    #     # za = list(outa)
    #     # lenga = len(za)
    #     # a1 = za[lenga - 3]
    #     # a2 = za[lenga - 4]
    #     # A = format(a1, 'x') + format(a2, 'x')
    #     # PF = int(A, 16) / 1000
    #     PF = outa
    #     return PF
    #
    #
    # def get_PF_A(self):
    #     chunk = self.addr
    #     chunk += b'\x08'
    #     chunk += b'\x11'
    #     chunk += b'\x31'
    #     chunk = self.crc16(chunk)
    #     ser = self.open_port(self.ipaddress1, self.ipport1)
    #     time.sleep(100/1000)
    #     outa = ser.read_all()
    #     # za = list(outa)
    #     # lenga = len(za)
    #     # a1 = za[lenga - 3]
    #     # a2 = za[lenga - 4]
    #     # A = format(a1, 'x') + format(a2, 'x')
    #     # PF_A = int(A, 16) / 1000
    #     PF_A = outa
    #     return PF_A
    #
    #
    # def get_PF_B(self):
    #     chunk = self.addr
    #     chunk += b'\x08'
    #     chunk += b'\x11'
    #     chunk += b'\x32'
    #     chunk = self.crc16(chunk)
    #     ser = self.open_port(self.ipaddress1, self.ipport1)
    #     time.sleep(100/1000)
    #     outa = ser.read_all()
    #     # za = list(outa)
    #     # lenga = len(za)
    #     # a1 = za[lenga - 3]
    #     # a2 = za[lenga - 4]
    #     # A = format(a1, 'x') + format(a2, 'x')
    #     # PF_B = int(A, 16) / 1000
    #     PF_B = outa
    #     return PF_B
    #
    #
    # def get_PF_C(self):
    #     chunk = self.addr
    #     chunk += b'\x08'
    #     chunk += b'\x11'
    #     chunk += b'\x33'
    #     chunk = self.crc16(chunk)
    #     ser = self.open_port(self.ipaddress1, self.ipport1)
    #     time.sleep(100/1000)
    #     outa = ser.read_all()
    #     # za = list(outa)
    #     # lenga = len(za)
    #     # a1 = za[lenga - 3]
    #     # a2 = za[lenga - 4]
    #     # A = format(a1, 'x') + format(a2, 'x')
    #     # PF_C = int(A, 16) / 1000
    #     PF_C = outa
    #     return PF_C

# merc = Mercury230(address, port)
# m230a = Mercury230(91, 'COM3')
# m230a.connect_user()
# print(m230a.get_Q_A())
# print("Серийный номер : ", m230a.get_sn()[0])
# print("Дата изготовления : ", m230a.get_sn()[1])
# # print(m230a.get_FW_version())
# m230a.disconnect()
