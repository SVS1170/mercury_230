#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import argparse
# import serial
import struct
import time
import configparser
from mercury230 import Mercury230
#import db_connector as db
# from bitstring import BitArray

config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = int(config["counter"]["address"])
#addr = struct.pack('B', address)
ipaddress = config["counter"]["ipaddress"]
ipport = config["counter"]["ipport"]
r = True
mercury_234 = Mercury230(address, ipaddress, ipport)
#ser = open_port(self.ipaddress1, self.ipport1)
#ser.timeout = 0.1

def cycle_read():
    while r == True:
        mercury_234.connect_user()
#        mercury_234.connection_test()
        Ua = mercury_234.get_voltage_A()
        Ub = mercury_234.get_voltage_B()
        Uc = mercury_234.get_voltage_C()
        Ia = mercury_234.get_current_A()
        Ib = mercury_234.get_current_B()
        Ic = mercury_234.get_current_C()
        P = mercury_234.get_P()
        Pa = mercury_234.get_P_A()
        Pb = mercury_234.get_P_B()
        Pc = mercury_234.get_P_C()
        Qa = mercury_234.get_Q_A()
        Qb = mercury_234.get_Q_B()
        Qc = mercury_234.get_Q_C()
        Sa = mercury_234.get_S_A()
        Sb = mercury_234.get_S_B()
        Sc = mercury_234.get_S_C()
        Hz = mercury_234.get_frequency()
        Tcase = mercury_234.get_temp()
        print("Ua : ", Ua, ", Ub : ", Ub, ", Uc : ", Uc)
#        print("Ua : ", Ua)
        print("Ia : ", Ia, ", Ib : ", Ib, ", Ic : ", Ic)
        print("Pa : ", Pa, ", Pb : ", Pb, ", Pc : ", Pc)
        print("Qa : ", Qa, ", Qb : ", Qb, ", Qc : ", Qc)
        print("Sa : ", Sa, ", Sb : ", Sb, ", Sc : ", Sc)
        print("Hz : ", Hz, ", Tcase : ", Tcase)
        # print("summPa,Pb,Pc :", mercury_234.get_active_energy_phases())
        # print(mercury_234.get_active_energy_current_day())
#        db.insert_data_data('data', Ua, Ub, Uc, Ia, Ib, Ic, P, Pa, Pb, Pc, Qa, Qb, Qc, Sa, Sb, Sc, Tcase)
        person_dict = {"Ua": Ua,
        "Ub": Ub, "Uc": Uc,
        "Ia": Ia
        }
        mercury_234.disconnect()
        time.sleep(5)

cycle_read()