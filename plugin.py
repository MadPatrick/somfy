# Tahoma/Conexoon IO blind plugin
#
# Author: Nonolk, 2019-2020
# FirstFree function courtesy of @moroen https://github.com/moroen/IKEA-Tradfri-plugin
# All credits for the plugin are for Nonolk, who is the origin plugin creator
"""
<plugin key="tahomaIO" name="Somfy Tahoma or Conexoon plugin" author="MadPatrick" version="1.1.2" externallink="https://github.com/MadPatrick/somfy">
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
import exceptions
import time

class BasePlugin:
    enabled = False
    def __init__(self):
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
        
        logging.debug("starting to log in")
        self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        
    def onStop(self):
        logging.info("stopping plugin")
        self.heartbeat = False

    def onConnect(self, Connection, Status, Description):
        logging.debug("onConnect: Connection: '"+str(Connection)+"', Status: '"+str(Status)+"', Description: '"+str(Description)+"' self.logged_in: '"+str(self.logged_in)+"'")
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

    def onCommand(self, Unit, Command, Level, Hue):
        logging.debug("onCommand: Unit: '"+str(Unit)+"', Command: '"+str(Command)+"', Level: '"+str(Level)+"', Hue: '"+str(Hue)+"'")
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
        logging.debug("preparing command: # commands: "+str(len(commands)))
        logging.debug("preparing command: # actions_serialized: "+str(len(self.actions_serialized)))
        data = {"label": "Domoticz - "+Devices[Unit].Name+" - "+commands["name"], "actions": self.actions_serialized}
        self.json_data = json.dumps(data, indent=None, sort_keys=True)

        if (not self.logged_in):
            logging.info("Not logged in, must connect")
            self.command = True
            self.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        else:
            try:
                self.tahoma_command()
            except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
                Domoticz.Error("Failed to send command: " + str(exp))
                logging.error("Failed to send command: " + str(exp))
                return
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
                    try:
                        self.get_events()
                    except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
                        Domoticz.Error("Failed to request data: " + str(exp))
                        logging.error("Failed to request data: " + str(exp))
                        return
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

        Status = response.status_code 
        Data = response.json()
        logging.debug("Login respone: status_code: '"+str(Status)+"' reponse body: '"+str(Data)+"'")

        if (Status == 200 and not self.logged_in):
            self.logged_in = True
            logging.info("Tahoma authentication succeeded")
            #self.cookie = response.cookies
            self.cookie = response.headers["Set-Cookie"]
            logging.debug("login: cookies: '"+ str(response.cookies)+"', headers: '"+str(response.headers)+"'")
            self.register_listener()

        elif ((Status == 401) or (Status == 400)):
            strData = Data["error"]
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
        timeout = 4
        logging.debug("start command")
        Headers = { 'Host': self.srvaddr, "Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/exec/apply'
        logging.debug("onCommand: headers: '"+str(Headers)+"', data '"+str(self.json_data)+"'")
        logging.info("Sending command to tahoma api")
        try:
            response = requests.post(url, headers=Headers, data=self.json_data, timeout=timeout)
        except requests.exceptions.RequestException as exp:
            logging.error("Send command returns RequestException: " + str(exp))
            Domoticz.Error("Send command returns RequestException: " + str(exp))

        logging.debug("command response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("error during command, status: " + str(response.status_code))
            return
        self.executionId = response.json()['execId']
        self.get_events()
        return

    def register_listener(self):
        logging.debug("start register")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/events/register'
        response = requests.post(url, headers=Headers, timeout=self.timeout)
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
        self.listenerId = Data['id']
        logging.info("Tahoma listener registred")
        self.refresh = False
        logging.info("Checking setup status at startup")
        self.get_devices()

    def get_devices(self):
        logging.debug("start get devices")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/setup/devices'
        response = requests.get(url, headers=Headers, timeout=self.timeout)
        logging.debug("get device response: url '" + str(response.url) + "' response headers: '"+str(response.headers)+"'")
        logging.debug("get device response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("get_devices: error during get devices, status: " + str(response.status_code))
            return

        Data = response.json()

        if (not "uiClass" in response.text):
            logging.error("get_devices: missing uiClass in response")
            logging.debug(str(Data))
            return

        self.devices = Data

        self.filtered_devices = list()
        for device in self.devices:
            logging.debug("get_devices: Device name: "+device["label"]+" Device class: "+device["uiClass"])
            if (((device["uiClass"] == "RollerShutter") or (device["uiClass"] == "ExteriorScreen") or (device["uiClass"] == "Screen") or (device["uiClass"] == "Awning") or (device["uiClass"] == "Pergola") or (device["uiClass"] == "GarageDoor") or (device["uiClass"] == "Window") or (device["uiClass"] == "VenetianBlind") or (device["uiClass"] == "ExteriorVenetianBlind")) and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
                self.filtered_devices.append(device)

        logging.debug("get_devices: devices found: "+str(len(Devices))+" self.startup: "+str(self.startup))
        if (len(Devices) == 0 and self.startup):
            count = 1
            for device in self.filtered_devices:
                logging.info("get_devices: Creating device: "+device["label"])
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

                 logging.debug("get_devices: Must create device: "+device["label"])

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
        self.startup = False
        self.get_events()

    def get_events(self):
        logging.debug("start get events")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/events/'+self.listenerId+'/fetch'

        for i in range(1,4):
            try:
                response = requests.post(url, headers=Headers, timeout=self.timeout)
                logging.debug("get events response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
                logging.debug("get events: self.logged_in = '"+str(self.logged_in)+"' and self.heartbeat = '"+str(self.heartbeat)+"' and self.startup = '"+str(self.startup))
                if response.status_code != 200:
                    logging.error("error during get events, status: " + str(response.status_code) + ", " + str(response.text))
                    return
                elif (response.status_code == 200 and self.logged_in and (not self.startup)):
                    strData = response.json()

                    if (not "DeviceStateChangedEvent" in response.text):
                      logging.debug("get_events: no DeviceStateChangedEvent found in response: " + str(strData))
                      return

                    self.events = strData

                    if (self.events):
                        filtered_events = list()

                        for event in self.events:
                            if (event["name"] == "DeviceStateChangedEvent"):
                                logging.debug("get_events: add event: URL: '"+event["deviceURL"]+"' num states: '"+str(len(event["deviceStates"]))+"'")
                                filtered_events.append(event)

                        self.update_devices_status(filtered_events)

                # elif (response.status_code == 200 and (not self.heartbeat)):
                  # return
                else:
                  logging.info("Return status"+str(response.status_code))
            except requests.exceptions.RequestException as exp:
                logging.error("get_events RequestException: " + str(exp))
            time.sleep(i ** 3)
        else:
            raise exceptions.TooManyRetries

    def update_devices_status(self, Updated_devices):
        logging.debug("updating device status self.startup = "+str(self.startup)+"on data: "+str(Updated_devices))
        for dev in Devices:
           logging.debug("update_devices_status: checking Domoticz device: "+Devices[dev].Name)
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
                       logging.debug("update_devices_status: device['name'] != DeviceStateChangedEvent: "+str(device["name"])+": breaking out")
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

                      Domoticz.Status("Updating device:"+Devices[dev].Name)
                      logging.info("Updating device:"+Devices[dev].Name)
                      if (level == 0):
                        Devices[dev].Update(0,"0")
                      if (level == 100):
                        Devices[dev].Update(1,"100")
                      if (level != 0 and level != 100):
                        Devices[dev].Update(2,str(level))
        return


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

