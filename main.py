#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import argparse
# import serial
import struct
import time
#import json
import configparser
import paho.mqtt.client as mqtt
from mercury230 import Mercury230
#import db_connector as db
# from bitstring import BitArray

config = configparser.ConfigParser()
config.read("config.ini")  # читаем конфиг
address = int(config["counter"]["address"])
#addr = struct.pack('B', address)
ipaddress = config["counter"]["ipaddress"]
ipport = config["counter"]["ipport"]
mqtt_ipaddress = config["mqtt"]["ipaddress"]
#mqtt_port = config["mqtt"]["port"]
mqtt_user = config["mqtt"]["user"]
mqtt_pass = config["mqtt"]["pass"]
mqtt_topic = config["mqtt"]["topic"]
r = True
mercury_234 = Mercury230(address, ipaddress, ipport)
#ser = open_port(self.ipaddress1, self.ipport1)
#ser.timeout = 0.1

def on_connect(client, userdata, flags, rc):
    if rc == 0:
#        client.loop_start()
#        client.loop_start()
        print("connected OK Returned code=", rc)
#        logging.info("connected OK Returned code=" + str(rc))
#        client.subscribe("gate1/reply", qos=1)
    else:
        print("Bad connection Returned code=", rc)
#        logging.info("Bad connection Returned code=" + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
#        client.loop_stop()
        print ("Unexpected MQTT disconnection. Will auto-reconnect")

#def on_subscribe(client, userdata, mid, granted_qos):
#    print("I've subscribed with QoS: {}".format(
#    granted_qos[0]))

#def on_message(client, userdata, msg):
#    global pingerror
#    print("Message received. Topic: {}. Payload: {}".format(
#        msg.topic,
#        str(msg.payload)))
#    if str(msg.payload) == "b'tx-end'":
#        bot.send_message(message_chat_id, 'Сигнал отправлен')
#    if str(msg.payload) == "b'ping-ok'":
#        pingerror = 0

client = mqtt.Client("counter") #create new instance
client.username_pw_set(mqtt_user, mqtt_pass)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
#client.on_subscribe = on_subscribe
#client.on_message = on_message
client.connect_async(mqtt_ipaddress) #connect to broker
#client.publish("test22","OFF")#publish
client.loop_start()


def cycle_read():
    Ua = 0
    Ub = 0
    Uc = 0
    fooUa = True
    fooUb = True
    fooUc = True
    Ia = 0
    Ib = 0
    Ic = 0
    fooIa = True
    fooIb = True
    fooIc = True
    while r == True:
        mercury_234.connect_user()
#        mercury_234.connection_test()
        lUa = mercury_234.get_voltage_A()
        lUb = mercury_234.get_voltage_B()
        lUc = mercury_234.get_voltage_C()
        lIa = mercury_234.get_current_A()
        lIb = mercury_234.get_current_B()
        lIc = mercury_234.get_current_C()
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
#        Tcase = mercury_234.get_temp()
        Pcd = mercury_234.get_active_energy_current_day()
        if abs(lUa - Ua) < 30:
                Ua = lUa
                fooUa = False
        else:
            if fooUa:
                Ua = lUa
                fooUa = False
            fooUa = True
        if abs(lUb - Ub) < 30:
                Ub = lUb
                fooUb = False
        else:
            if fooUb:
                Ub = lUb
                fooUb = False
            fooUb = True
        if abs(lUc - Uc) < 30:
                Uc = lUc
                fooUc = False
        else:
            if fooUc:
                Uc = lUc
                fooUc = False
            fooUc = True
        if abs(lIa - Ia) < 5:
                Ia = lIa
                fooIa = False
        else:
            if fooIa:
                Ia = lIa
                fooIa = False
            fooIa = True
        if abs(lIb - Ib) < 5:
                Ib = lIb
                fooIb = False
        else:
            if fooIb:
                Ib = lIb
                fooIb = False
            fooIb = True
        if abs(lIc - Ic) < 30:
                Ic = lIc
                fooIc = False
        else:
            if fooIc:
                Ic = lIc
                fooIc = False
            fooIc = True
            
#        print("Ua : ", Ua, ", Ub : ", Ub, ", Uc : ", Uc)
#        print("Ua : ", Ua)
#        print("Ia : ", Ia, ", Ib : ", Ib, ", Ic : ", Ic)
#        print("Pa : ", Pa, ", Pb : ", Pb, ", Pc : ", Pc)
#        print("Qa : ", Qa, ", Qb : ", Qb, ", Qc : ", Qc)
#        print("Sa : ", Sa, ", Sb : ", Sb, ", Sc : ", Sc)
#        print("Hz : ", Hz, ", Tcase : ", Tcase)
        # print("summPa,Pb,Pc :", mercury_234.get_active_energy_phases())
        # print(mercury_234.get_active_energy_current_day())
#        db.insert_data_data('data', Ua, Ub, Uc, Ia, Ib, Ic, P, Pa, Pb, Pc, Qa, Qb, Qc, Sa, Sb, Sc, Tcase)
        json_string1 = '"Ua": "' + str(Ua) + '", "Ub": "' + str(Ub) + '", "Uc": "' + str(Uc) + '"'
        json_string2 = '"Ia": "' + str(Ia) + '", "Ib": "' + str(Ib) + '", "Ic": "' + str(Ic) + '"'
        json_string3 = '"P": "' + str(P) + '", "Pa": "' + str(Pa) + '", "Pb": "' + str(Pb) + '", "Pc": "' + str(Pc) + '"'
        json_string4 = '"Qa": "' + str(Qa) + '", "Qb": "' + str(Qb) + '", "Qc": "' + str(Qc) + '"'
        json_string5 = '"Sa": "' + str(Sa) + '", "Sb": "' + str(Sb) + '", "Sc": "' + str(Sc) + '"'
        json_string6 = '"Hz": "' + str(Hz) + '"'
        json_string7 = '"Pcd": "' + str(Pcd) + '"'
        json_string_end = '{' + json_string1 + ',' + json_string2 + ',' + json_string3 + ',' + json_string4 + ',' + json_string5 + ',' + json_string6 + ',' + json_string7 + '}'
#        json_object = json.loads(json_string)
        print(json_string_end)
        client.publish(mqtt_topic, json_string_end, 1)
        mercury_234.disconnect()
        time.sleep(5)

cycle_read()