import time
import logging
import json
import consolemenu
#import tahoma
import tahoma_local as tahoma
import exceptions
from params import *

logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename='somfy_test.log',
                    level=logging.DEBUG)
logging.info("=== starting test run ===")

menuoptions = ['0 exit',"1 log in", "2 register", "3 check log in", "4 generate toke", "5 activate token", "6 get tokens", "7 delete token", "10 get devices", "11 get events", "12 send command"]
mymenu = consolemenu.SelectionMenu(menuoptions)

device_list = list()

tahoma = tahoma.Tahoma()
if tahoma.cookie is None:
    tahoma.cookie = dict(JSESSIONID='F290EEAEC03B4838EBDA4B0CD0034BAB')

if True:
    while True:
        for i in menuoptions:
            print(i) 
        x = int(input("Please Select:"))
        print(x)
        if x == 0: 
            logging.info("== end test run ===")
            exit()
        if x == 1:
            status = False
            try:
                status = tahoma.tahoma_login(p_email, p_password)
            except exceptions.LoginFailure as exp:
                print("Failed to login: " + str(exp))
            if tahoma.cookie is None:
                tahoma.cookie = dict(JSESSIONID='F290EEAEC03B4838EBDA4B0CD0034BAB')
            print("login status: "+str(status))
        if x == 2: 
            tahoma.register_listener()
            if tahoma.listenerId is None:
                tahoma.listenerId = 'b4e62511-ac10-3e01-60e0-9b9f656aea77'
        if x == 3: print(str(tahoma.logged_in))
        if x == 4: 
            response = tahoma.generate_token(p_pin)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 5:
            repsonse = tahoma.activate_token(p_pin)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 6:
            repsonse = tahoma.get_tokens(p_pin)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 7:
            uuid = input("Please enter uuid to delete:")
            repsonse = tahoma.delete_tokens(p_pin, uuid)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 10: print(tahoma.get_devices(device_list))
        if x == 11: print(tahoma.get_events())
        if x == 12: 
            data = '{"actions": [{"commands": [{"name": "open"}], "deviceURL": "io://1237-2024-7920/10464619"}], "label": "Domoticz - Somfy - Kamer_Klein - open"}'
            print(tahoma.tahoma_command(json.dumps(data)))
        input("Press Enter to continue...")
        # except (ValueError) as err:
            # print("error in menu keuze")
else:
    logging.error("initialisation failed")

