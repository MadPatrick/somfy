import time
import logging
import json
import consolemenu
import tahoma
from tahoma_local import SomfyBox
import exceptions
from params import *

logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename='somfy_test.log',
                    level=logging.DEBUG)
logging.info("=== starting test run ===")

menuoptions = ['0 exit',"1 log in for local", "2 login for web", "3 check log in", "4 generate toke", "5 activate token", "6 get tokens", "7 delete token", "8 print token",
    "10 web register", "11 web get devices", "12 web get events", "13 web send command",
    "20 get local API version", "21 get local gateway", "22 get local devices", "23 register local listener", "24 get local events", "25 get local device state", "26 send local command"]
mymenu = consolemenu.SelectionMenu(menuoptions)

device_list = list()

#tahoma = tahoma()
tahoma = tahoma.Tahoma()
theBox = SomfyBox(p_pin, p_port)
print("=====")
if str(p_token) != '0':
    theBox.token = p_token
    print ("token loaded from params, no need to get from web")
else:
    print("No token loaded from param, first get it from web, steps <10")

if theBox.cookie is None:
    theBox.cookie = dict(JSESSIONID='F290EEAEC03B4838EBDA4B0CD0034BAB')

if True:
    while True:
        print("=====")
        for i in menuoptions:
            print(i) 
        x = int(input("Please Select:"))
        print(x)
        logging.info("selected menu option: "+str(x))
        if x == 0: 
            logging.info("== end test run ===")
            exit()
        if x == 1: #log in
            status = False
            try:
                status = theBox.tahoma_login(p_email, p_password)
            except exceptions.LoginFailure as exp:
                print("Failed to login: " + str(exp))
            if theBox.cookie is None:
                theBox.cookie = dict(JSESSIONID='F290EEAEC03B4838EBDA4B0CD0034BAB')
            print("login status: "+str(status))
        if x == 2: #log in
            status = False
            try:
                status = tahoma.tahoma_login(p_email, p_password)
            except exceptions.LoginFailure as exp:
                print("Failed to login: " + str(exp))
            if tahoma.cookie is None:
                tahoma.cookie = 'JSESSIONID=F290EEAEC03B4838EBDA4B0CD0034BAB; Path=/enduser-mobile-web; Secure; HttpOnly; SameSite=None'
            print("login status: "+str(status))
        if x == 3: print(str(theBox.logged_in)) #check log in
        if x == 4: #generate token
            try:
                response = theBox.generate_token(p_pin)
                print("you can store the token in params.py for later use")
                print(json.dumps(response, sort_keys = True, indent=4))
            except exceptions.LoginFailure as exp:
                print("Failed to login: " + str(exp))
            if theBox.token is None:
                print('not token generated, using default from file')
                theBox.token = str(p_token)
        if x == 5: #activate token
            response = theBox.activate_token(p_pin, theBox.token)
            #theBox.token = tahoma.token
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 6: #get list of tokens
            response = theBox.get_tokens(p_pin)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 7:#delete token
            uuid = input("Please enter uuid to delete:")
            response = theBox.delete_tokens(p_pin, uuid)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 8:
            print("token = " + str(theBox.token))
        if x == 10: # register listener
            tahoma.register_listener()
            if tahoma.listenerId is None:
                tahoma.listenerId = 'b4e62511-ac10-3e01-60e0-9b9f656aea77'
        if x == 11: print(tahoma.get_devices())
        if x == 12: print(tahoma.get_events())
        if x == 13: 
            device = str(input("enter deviceURL to command: "))
            command = str(input("enter command <open|close>: "))
            commando = {"actions":[{"commands":[{"name":command}], "deviceURL":device}], "label":"test command"}
            #data = '{"actions": [{"commands": [{"name": "open"}], "deviceURL": "io://1234-5678-9012/10464619"}], "label": "Domoticz - Somfy - test - open"}'
            print(tahoma.send_command(json.dumps(commando)))
        if x == 20: #get version of local API
            response = theBox.get_version()
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 21: #get version of local API
            response = theBox.get_gateways()
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 22: #get version of local API
            response = theBox.get_devices()
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 23: #get version of local API
            response = theBox.register_listener()
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 24: #get version of local API
            response = theBox.get_events()
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 25: #get device state on local API
            device = str(input("enter deviceurl to get state: "))
            response = theBox.get_device_state(device)
            print(json.dumps(response, sort_keys = True, indent=4))
        if x == 26: #send a command to the local API
            device = str(input("enter deviceURL to command: "))
            command = str(input("enter command <open|close>: "))
            commando = {"actions":[{"commands":[{"name":command}], "deviceURL":device}], "label":"test command"}
            response = theBox.send_command(commando)
            print(json.dumps(response, sort_keys = True, indent=4))
        input("Press Enter to continue...")
        # except (ValueError) as err:
            # print("error in menu keuze")
else:
    logging.error("initialisation failed")

