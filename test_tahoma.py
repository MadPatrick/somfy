import time
import logging
import json
import consolemenu
import tahoma
import exceptions

logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename='somfy_test.log',
                    level=logging.DEBUG)

menuoptions = ['0 exit',"1 log in", "2 register", "3 get devices", "4 get events", "5 send command", "6 check log in"]
mymenu = consolemenu.SelectionMenu(menuoptions)

device_list = list()

tahoma = tahoma.Tahoma()
if tahoma.cookie is None:
    tahoma.cookie = 'JSESSIONID=F290EEAEC03B4838EBDA4B0CD0034BAB; Path=/enduser-mobile-web; Secure; HttpOnly; SameSite=None'

if True:
    while True:
        for i in menuoptions:
            print(i) 
        x = int(input("Please Select:"))
        print(x)
        if x == 0: exit()
        if x == 1: 
            try:
                tahoma.tahoma_login('sinterklaas@gmail.com', "blabla")
            except exceptions.LoginFailure as exp:
                print("Failed to login: " + str(exp))
        if x == 2: 
            tahoma.register_listener()
            if tahoma.listenerId is None:
                tahoma.listenerId = 'b4e62511-ac10-3e01-60e0-9b9f656aea77'
        if x == 3: print(tahoma.get_devices(device_list))
        if x == 4: print(tahoma.get_events())
        if x == 5: 
            data = '{"actions": [{"commands": [{"name": "open"}], "deviceURL": "io://1237-2024-7920/10464619"}], "label": "Domoticz - Somfy - Kamer_Klein - open"}'
            print(tahoma.tahoma_command(json.dumps(data)))
        if x == 6: print(str(tahoma.logged_in))
        input("Press Enter to continue...")
        # except (ValueError) as err:
            # print("error in menu keuze")
else:
    logging.error("initialisation failed")

