# Tahoma/Conexoon IO blind plugin
#
# Author: Nonolk, 2019-2020
# FirstFree function courtesy of @moroen https://github.com/moroen/IKEA-Tradfri-plugin
# All credits for the plugin are for Nonolk, who is the origin plugin creator
"""
<plugin key="tahomaIO" name="Somfy Tahoma or Conexoon plugin" author="MadPatrick" version="0.1.1" externallink="https://github.com/MadPatrick/somfy">
    <description>
	<br/><h2>Somfy Tahoma/Conexoon plugin</h2><br/>
        <ul style="list-style-type:square">
            <li>This plugin require internet connection at all time.</li>
            <li>It controls the Somfy for IO Blinds or Screens</li>
            <li>Please provide your email and password used to connect Tahoma/Conexoon</li>
        </ul>
</description>
    <params>
        <param field="Username" label="Username" width="200px" required="true" default=""/>
        <param field="Password" label="Password" width="200px" required="true" default="" password="true"/>
        <param field="Mode2" label="Refresh interval" width="75px">
            <options>
                <option label="20s" value="2"/>
                <option label="1m" value="6"/>
                <option label="5m" value="30" default="true"/>
                <option label="10m" value="60"/>
                <option label="15m" value="90"/>
            </options>
        </param>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import urllib.parse
import json
import sys
import requests
import logging

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.httpConn = None
        self.srvaddr = "tahomalink.com"
        self.base_url = "https://tahomalink.com:443"
        self.cookie = ""
        self.listenerId = None
        self.logged_in = False
        self.startup = True
        self.heartbeat = False
        self.devices = None
        self.filtered_devices = None
        self.events = None
        self.heartbeat_delay = 1
        self.con_delay = 0
        self.wait_delay = 30
        self.json_data = None
        self.command = False
        self.refresh = True
        self.actions_serialized = []
        self.timeout = 10
        self.logger = None
        return

    def onStart(self):
        Domoticz.Status("Starting Tahoma blind plugin, logging to file somfy.logs")
        self.logger = logging.getLogger('root')
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            DumpConfigToLog()
            logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename='somfy.log',level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename='somfy.log',level=logging.INFO)
        logging.info('started plugin')
        self.runCounter = int(Parameters['Mode2'])
        
        #self.httpConn = Domoticz.Connection(Name="Secure Connection", Transport="TCP/IP", Protocol="HTTPS", Address=self.srvaddr, Port="443")
        #self.httpConn.Connect()
        logging.debug("starting to log in")
        self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        
    def onStop(self):
        logging.info("stopping plugin")
        self.heartbeat = False
        #self.httpConn = None

    def onConnect(self, Connection, Status, Description):

        if (Status == 0 and not self.logged_in):
          self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        elif (self.cookie and self.logged_in and (not self.command)):
          self.get_events()

        elif (self.command):
          self.tahoma_command()
          self.command = False
          self.heartbeat = False
          self.actions_serialized = []
        else:
          logging.info("Failed to connect to tahoma api")


    def handle_response(self):
        #elif (Status == 200 and self.logged_in and (not self.listenerId)):
        if (Status == 200 and self.logged_in and (not self.listenerId)):
            #strData = Data["Data"].decode("utf-8", "ignore")
            if "Data" in Data:
                strData = Data["Data"]
            else:
                logging.error("Data expected in response but  not found")
                return
            #id = json.loads(strData)
            id = strData
            self.listenerId = id['id']
            Domoticz.Status("Tahoma listener registred")
            logging.info("Tahoma listener registred")
            self.refresh = False
            Domoticz.Status("Check setup status at statup")
            logging.info("Check setup status at statup")
            Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", "Cookie": self.cookie}
            self.httpConn.Send({'Verb':'GET', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/setup/devices'})
            

        #elif (Status == 200 and self.logged_in and self.startup and (not self.refresh)):
          # strData = Data["Data"].decode("utf-8", "ignore")

          # if (not "uiClass" in strData):
            # logging.debug(str(strData))
            # return

          # self.devices = json.loads(strData)

          # self.filtered_devices = list()
          # for device in self.devices:
             # logging.debug("Device name: "+device["label"]+" Device class: "+device["uiClass"])
             # if (((device["uiClass"] == "RollerShutter") or (device["uiClass"] == "ExteriorScreen") or (device["uiClass"] == "Screen") or (device["uiClass"] == "Awning") or (device["uiClass"] == "Pergola") or (device["uiClass"] == "GarageDoor") or (device["uiClass"] == "Window") or (device["uiClass"] == "VenetianBlind") or (device["uiClass"] == "ExteriorVenetianBlind")) and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
               # self.filtered_devices.append(device)

          # if (len(Devices) == 0 and self.startup):
            # count = 1
            # for device in self.filtered_devices:
               # Domoticz.Status("Creating device: "+device["label"])
               # swtype = None

               # if (device["deviceURL"].startswith("io://")):
                   # if (device["uiClass"] == "Awning"):
                    # swtype = 13
                   # else:
                    # swtype = 16
               # elif (device["deviceURL"].startswith("rts://")):
                    # swtype = 6

               # Domoticz.Device(Name=device["label"], Unit=count, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

               # if not (count in Devices):
                   # Domoticz.Error("Device creation not allowed, please allow device creation")
               # else:
                   # Domoticz.Status("Device created: "+device["label"])
                   # count += 1

          # if ((len(Devices) < len(self.filtered_devices)) and len(Devices) != 0 and self.startup):
            # self.logger.info("New device(s) detected")
            # found = False

            # for device in self.filtered_devices:
               # for dev in Devices:
                  # UnitID = Devices[dev].Unit
                  # if Devices[dev].DeviceID == device["deviceURL"]:
                    # found = True
                    # break
               # if (not found):
                 # idx = firstFree()
                 # swtype = None

                 # Domoticz.Status("Must create device: "+device["label"])

                 # if (device["deviceURL"].startswith("io://")):
                    # if (device["uiClass"] == "Awning"):
                     # swtype = 13
                    # else:
                     # swtype = 16
                 # elif (device["deviceURL"].startswith("rts://")):
                    # swtype = 6

                 # Domoticz.Device(Name=device["label"], Unit=idx, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

                 # if not (idx in Devices):
                     # Domoticz.Error("Device creation not allowed, please allow device creation")
                 # else:
                     # Domoticz.Status("New device created: "+device["label"])
               # else:
                  # found = False
          # update_devices_status(self,self.filtered_devices)
          # self.startup = False

        elif (Status == 200 and self.logged_in and self.heartbeat and (not self.startup)):
            strData = Data["Data"].decode("utf-8", "ignore")

            if (not "DeviceStateChangedEvent" in strData):
              self.logger.debug(str(strData))
              return

            self.events = json.loads(strData)

            if (self.events):
                filtered_events = list()

                for event in self.events:
                    if (event["name"] == "DeviceStateChangedEvent"):
                        filtered_events.append(event)

                update_devices_status(self,filtered_events)

        elif (Status == 200 and (not self.heartbeat)):
          return
        else:
          self.logger.info("Return status"+str(Status))
 
    # def onMessage(self, Connection, Data):
        # Status = int(Data["Status"])

        # if (Status == 200 and not self.logged_in):
          # self.logged_in = True
          # Domoticz.Status("Tahoma auth succeed")
          # tmp = Data["Headers"]
          # self.cookie = tmp["Set-Cookie"]
          # register_listener(self)

        # elif ((Status == 401) or (Status == 400)):
          # strData = Data["Data"].decode("utf-8", "ignore")
          # Domoticz.Error("Tahoma error must reconnect")
          # self.logged_in = False
          # self.cookie = None
          # self.listenerId = None

          # if ("Too many" in strData):
            # Domoticz.Error("Too much connexions must wait")
            # self.heartbeat = True
            # return
          # if ("Bad credentials" in strData):
            # Domoticz.Error("Bad credentials please update credentials and restart plugin")
            # self.heartbeat =  False
            # return

          # if (not self.logged_in):
            # self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
            # return

        # elif (Status == 200 and self.logged_in and (not self.listenerId)):
            # strData = Data["Data"].decode("utf-8", "ignore")
            # id = json.loads(strData)
            # self.listenerId = id['id']
            # Domoticz.Status("Tahoma listener registred")
            # self.refresh = False
            # Domoticz.Status("Check setup status at statup")
            # Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", "Cookie": self.cookie}
            # self.httpConn.Send({'Verb':'GET', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/setup/devices'})

        # elif (Status == 200 and self.logged_in and self.startup and (not self.refresh)):
          # strData = Data["Data"].decode("utf-8", "ignore")

          # if (not "uiClass" in strData):
            # self.logger.debug(str(strData))
            # return

          # self.devices = json.loads(strData)

          # self.filtered_devices = list()
          # for device in self.devices:
             # self.logger.debug("Device name: "+device["label"]+" Device class: "+device["uiClass"])
             # if (((device["uiClass"] == "RollerShutter") or (device["uiClass"] == "ExteriorScreen") or (device["uiClass"] == "Screen") or (device["uiClass"] == "Awning") or (device["uiClass"] == "Pergola") or (device["uiClass"] == "GarageDoor") or (device["uiClass"] == "Window") or (device["uiClass"] == "VenetianBlind") or (device["uiClass"] == "ExteriorVenetianBlind")) and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
               # self.filtered_devices.append(device)

          # if (len(Devices) == 0 and self.startup):
            # count = 1
            # for device in self.filtered_devices:
               # Domoticz.Status("Creating device: "+device["label"])
               # swtype = None

               # if (device["deviceURL"].startswith("io://")):
                   # if (device["uiClass"] == "Awning"):
                    # swtype = 13
                   # else:
                    # swtype = 16
               # elif (device["deviceURL"].startswith("rts://")):
                    # swtype = 6

               # Domoticz.Device(Name=device["label"], Unit=count, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

               # if not (count in Devices):
                   # Domoticz.Error("Device creation not allowed, please allow device creation")
               # else:
                   # Domoticz.Status("Device created: "+device["label"])
                   # count += 1

          # if ((len(Devices) < len(self.filtered_devices)) and len(Devices) != 0 and self.startup):
            # self.logger.info("New device(s) detected")
            # found = False

            # for device in self.filtered_devices:
               # for dev in Devices:
                  # UnitID = Devices[dev].Unit
                  # if Devices[dev].DeviceID == device["deviceURL"]:
                    # found = True
                    # break
               # if (not found):
                 # idx = firstFree()
                 # swtype = None

                 # Domoticz.Status("Must create device: "+device["label"])

                 # if (device["deviceURL"].startswith("io://")):
                    # if (device["uiClass"] == "Awning"):
                     # swtype = 13
                    # else:
                     # swtype = 16
                 # elif (device["deviceURL"].startswith("rts://")):
                    # swtype = 6

                 # Domoticz.Device(Name=device["label"], Unit=idx, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

                 # if not (idx in Devices):
                     # Domoticz.Error("Device creation not allowed, please allow device creation")
                 # else:
                     # Domoticz.Status("New device created: "+device["label"])
               # else:
                  # found = False
          # update_devices_status(self,self.filtered_devices)
          # self.startup = False

        # elif (Status == 200 and self.logged_in and self.heartbeat and (not self.startup)):
            # strData = Data["Data"].decode("utf-8", "ignore")

            # if (not "DeviceStateChangedEvent" in strData):
              # self.logger.debug(str(strData))
              # return

            # self.events = json.loads(strData)

            # if (self.events):
                # filtered_events = list()

                # for event in self.events:
                    # if (event["name"] == "DeviceStateChangedEvent"):
                        # filtered_events.append(event)

                # update_devices_status(self,filtered_events)

        # elif (Status == 200 and (not self.heartbeat)):
          # return
        # else:
          # self.logger.info("Return status"+str(Status))

    def onCommand(self, Unit, Command, Level, Hue):
        commands_serialized = []
        action = {}
        commands = {}
        params = []


        if (str(Command) == "Off"):
          commands["name"] = "close"
        elif (str(Command) == "On"):
          commands["name"] = "open"
        elif ("Set Level" in str(Command)):
          commands["name"] = "setClosure"
          tmp = 100 - int(Level)
          params.append(tmp)
          commands["parameters"] = params

        commands_serialized.append(commands)
        action["deviceURL"] = Devices[Unit].DeviceID
        action["commands"] = commands_serialized
        self.actions_serialized.append(action)
        data = {"label": "Domoticz - "+Devices[Unit].Name+" - "+commands["name"], "actions": self.actions_serialized}
        self.json_data = json.dumps(data, indent=None, sort_keys=True)

        #if (not self.httpConn.Connected()):
        if (not self.logged_in):
          logging.info("Not logged in, must connect")
          self.command = True
          self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        else:
          self.tahoma_command()
          self.heartbeat = False
          self.actions_serialized = []

    def onDisconnect(self, Connection):
        return

    def onHeartbeat(self):
        self.runCounter = self.runCounter - 1
        if self.runCounter <= 0:
            logging.debug("Poll unit")
            self.runCounter = int(Parameters['Mode2'])            

            if (self.cookie and self.logged_in and (not self.startup)):
              if (not self.logged_in):
                self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
              else:
                self.get_events()
              self.heartbeat = True

            elif (self.heartbeat and (self.con_delay < self.wait_delay) and (not self.logged_in)):
              self.con_delay +=1
              Domoticz.Status("Too many connections waiting before authenticating again")

            elif (self.heartbeat and (self.con_delay == self.wait_delay) and (not self.logged_in)):
              if (not self.logged_in):
                self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
              self.heartbeat =True
              self.con_delay = 0
        else:
            logging.debug("Polling unit in " + str(self.runCounter) + " heartbeats.")

    def tahoma_login(self, username, password):

        url = self.base_url + '/enduser-mobile-web/enduserAPI/login'
        headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = "userId="+urllib.parse.quote(username)+"&userPassword="+urllib.parse.quote(password)+""
        response = requests.post(url, data=data, headers=headers, timeout=self.timeout)
        logging.debug("login response: status code: '"+ str(response.status_code)+"'")

        # Login = str(Parameters["Username"])
        # pwd = str(Parameters["Password"])
        # postData = "userId="+urllib.parse.quote(Login)+"&userPassword="+urllib.parse.quote(pwd)+""
        # self.httpConn.Send({'Verb':'POST', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/login', 'Data': postData})
        Status = response.status_code #int(Data["Status"])
        Data = response.json()
        logging.debug("Respone: status_code: '"+str(Status)+"' reponse body: '"+str(Data)+"'")

        if (Status == 200 and not self.logged_in):
            self.logged_in = True
            logging.info("Tahoma auth succeed")
            self.cookie = response.cookies
            self.cookie = response.headers["Set-Cookie"]
            logging.debug("login: cookies: '"+ str(response.cookies)+"', headers: '"+str(response.headers)+"'")
            # if "Headers" in Data:
                # tmp = Data["Headers"]
                # self.cookie = tmp["Set-Cookie"]
            # else:
                # logging.error("Headers expected but not received")
                # return
            self.register_listener()

        elif ((Status == 401) or (Status == 400)):
            if "Data" in Data:
                strData = Data["Data"]
            elif "error" in Data:
                strData = Data["error"]
            else:
                logging.error("no usable response data found")
                return
            Domoticz.Error("Tahoma error: must reconnect")
            logging.error("Tahoma error: must reconnect")
            self.logged_in = False
            self.cookie = None
            self.listenerId = None

            if ("Too many" in strData):
                Domoticz.Error("Too much connexions must wait")
                logging.error("Too much connexions must wait")
                self.heartbeat = True
                return
            if ("Bad credentials" in strData):
                Domoticz.Error("Bad credentials please update credentials and restart plugin")
                logging.error("Bad credentials please update credentials and restart plugin")
                self.heartbeat =  False
                return

            if (not self.logged_in):
                self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
                return
        return self.logged_in

    def tahoma_command(self):
        logging.debug("start command")
        Headers = { 'Host': self.srvaddr, "Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/exec/apply'
        #self.httpConn.Send({'Verb':'POST', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/exec/apply', 'Data': self.json_data})
        logging.debug("onCommand: headers: '"+str(Headers)+"', data '"+str(self.json_data)+"'")
        response = requests.post(url, headers=Headers, data=self.json_data, timeout=self.timeout)
        logging.info("Sending command to tahoma api")
        logging.debug("command response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("error during command, status: " + str(response.status_code))
            return
        self.get_events()
        return

    def register_listener(self):
        logging.debug("start register")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/events/register'
        response = requests.post(url, headers=Headers, timeout=self.timeout)
        #self.httpConn.Send({'Verb':'POST', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/events/register', 'Data': None})
        logging.debug("register response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("error during register, status: " + str(response.status_code))
            return
        Data = response.json()
        if "id" in Data:
            strData = Data["id"]
        else:
            logging.error("Data expected in response but  not found")
            return
        # #id = json.loads(strData)
        # id = strData
        # self.listenerId = id['id']
        self.listenerId = Data['id']
        logging.info("Tahoma listener registred")
        self.refresh = False
        logging.info("Checking setup status at startup")
        self.get_devices()

    def get_devices(self):
        logging.debug("start get devices")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", "Cookie": self.cookie}
        #self.httpConn.Send({'Verb':'GET', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/setup/devices'})
        url = self.base_url + '/enduser-mobile-web/enduserAPI/setup/devices'
        response = requests.post(url, headers=Headers, timeout=self.timeout)
        logging.debug("get device response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("error during get devices, status: " + str(response.status_code))
            return

        #strData = Data["Data"].decode("utf-8", "ignore")
        Data = response.json()
        if "Data" in Data:
            strData = Data["Data"]

        if (not "uiClass" in strData):
            logging.error("missing uiClass in response")
            logging.debug(str(strData))
            return

        self.devices = strData

        self.filtered_devices = list()
        for device in self.devices:
            logging.debug("Device name: "+device["label"]+" Device class: "+device["uiClass"])
            if (((device["uiClass"] == "RollerShutter") or (device["uiClass"] == "ExteriorScreen") or (device["uiClass"] == "Screen") or (device["uiClass"] == "Awning") or (device["uiClass"] == "Pergola") or (device["uiClass"] == "GarageDoor") or (device["uiClass"] == "Window") or (device["uiClass"] == "VenetianBlind") or (device["uiClass"] == "ExteriorVenetianBlind")) and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
                self.filtered_devices.append(device)

        if (len(Devices) == 0 and self.startup):
            count = 1
            for device in self.filtered_devices:
                logging.info("Creating device: "+device["label"])
                swtype = None

                if (device["deviceURL"].startswith("io://")):
                    if (device["uiClass"] == "Awning"):
                        swtype = 13
                    else:
                        swtype = 16
                elif (device["deviceURL"].startswith("rts://")):
                    swtype = 6

                Domoticz.Device(Name=device["label"], Unit=count, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

                if not (count in Devices):
                    logging.error("Device creation not allowed, please allow device creation")
                    Domoticz.Error("Device creation not allowed, please allow device creation")
                else:
                    logging.info("Device created: "+device["label"])
                    count += 1

        if ((len(Devices) < len(self.filtered_devices)) and len(Devices) != 0 and self.startup):
            logging.info("New device(s) detected")
            found = False

            for device in self.filtered_devices:
                for dev in Devices:
                  UnitID = Devices[dev].Unit
                  if Devices[dev].DeviceID == device["deviceURL"]:
                    found = True
                    break
                if (not found):
                 idx = firstFree()
                 swtype = None

                 logging.debug("Must create device: "+device["label"])

                 if (device["deviceURL"].startswith("io://")):
                    if (device["uiClass"] == "Awning"):
                     swtype = 13
                    else:
                     swtype = 16
                 elif (device["deviceURL"].startswith("rts://")):
                    swtype = 6

                 Domoticz.Device(Name=device["label"], Unit=idx, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()

                 if not (idx in Devices):
                     logging.error("Device creation not allowed, please allow device creation")
                     Domoticz.Error("Device creation not allowed, please allow device creation")
                 else:
                     logging.info("New device created: "+device["label"])
                else:
                  found = False
        update_devices_status(self,self.filtered_devices)
        self.startup = False

    def get_events(self):
        logging.debug("start get events")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/events/'+self.listenerId+'/fetch'
        response = requests.post(url, headers=Headers, timeout=self.timeout)
        #self.httpConn.Send({'Verb':'POST', 'Headers': Headers, 'URL':'/enduser-mobile-web/enduserAPI/events/'+self.listenerId+'/fetch', 'Data': None})
        logging.debug("register response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("error during get events, status: " + str(response.status_code))
            return
        #elif (Status == 200 and self.logged_in and self.heartbeat and (not self.startup)):
        elif (Status == 200 and self.logged_in and self.heartbeat and (not self.startup)):
            #strData = Data["Data"].decode("utf-8", "ignore")
            strData = response.json()["Data"]

            if (not "DeviceStateChangedEvent" in strData):
              logging.debug("no DeviceStateChangedEvent found: " + str(strData))
              return

            #self.events = json.loads(strData)
            self.events = strData

            if (self.events):
                filtered_events = list()

                for event in self.events:
                    if (event["name"] == "DeviceStateChangedEvent"):
                        filtered_events.append(event)

                update_devices_status(self,filtered_events)

        elif (Status == 200 and (not self.heartbeat)):
          return
        else:
          logging.info("Return status"+str(Status))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    Domoticz.Debug("Parameters count: " + str(len(Parameters)))
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("Parameter: '" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
    return


def DumpHTTPResponseToLog(httpResp, level=0):
    if (level==0): Domoticz.Debug("HTTP Details ("+str(len(httpResp))+"):")
    indentStr = ""
    for x in range(level):
        indentStr += "----"
    if isinstance(httpResp, dict):
        for x in httpResp:
            if not isinstance(httpResp[x], dict) and not isinstance(httpResp[x], list):
                Domoticz.Debug(indentStr + ">'" + x + "':'" + str(httpResp[x]) + "'")
            else:
                Domoticz.Debug(indentStr + ">'" + x + "':")
                DumpHTTPResponseToLog(httpResp[x], level+1)
    elif isinstance(httpResp, list):
        for x in httpResp:
            Domoticz.Debug(indentStr + "['" + x + "']")
    else:
        Domoticz.Debug(indentStr + ">'" + x + "':'" + str(httpResp[x]) + "'")

def firstFree():
    for num in range(1, 250):
        if num not in Devices:
            return num
    return

def update_devices_status(self,Updated_devices):
    for dev in Devices:
       for device in Updated_devices:

         if (Devices[dev].DeviceID == device["deviceURL"]) and (device["deviceURL"].startswith("io://")):
           level = 0
           status_l = False
           status = None

           if (self.startup):
               states = device["states"]
           else:
               states = device["deviceStates"]
               if (device["name"] != "DeviceStateChangedEvent"):
                   break

           for state in states:
              status_l = False

              if ((state["name"] == "core:ClosureState") or (state["name"] == "core:DeploymentState")):
                level = int(state["value"])
                level = 100 - level
                status_l = True
                
              if status_l:
                if (Devices[dev].sValue):
                  int_level = int(Devices[dev].sValue)
                else:
                  int_level = 0
                if (level != int_level):

                  Domoticz.Info("Updating device:"+Devices[dev].Name)
                  if (level == 0):
                    Devices[dev].Update(0,"0")
                  if (level == 100):
                    Devices[dev].Update(1,"100")
                  if (level != 0 and level != 100):
                    Devices[dev].Update(2,str(level))
    return

