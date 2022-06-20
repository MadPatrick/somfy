# Tahoma/Connexoon IO blind plugin
#
# Author: Nonolk, 2019-2020
# FirstFree function courtesy of @moroen https://github.com/moroen/IKEA-Tradfri-plugin
# All credits for the plugin are for Nonolk, who is the origin plugin creator
"""
<plugin key="tahomaIO" name="Somfy Tahoma or Connexoon plugin" author="MadPatrick" version="3.0.7" externallink="https://github.com/MadPatrick/somfy">
    <description>
	<br/><h2>Somfy Tahoma/Connexoon plugin</h2><br/>
        <ul style="list-style-type:square">
            <li>version: 3.0.6</li>
            <li>This plugin require internet connection at all time.</li>
            <li>It controls the Somfy for IO Blinds or Screens</li>
            <li>Please provide your email and password used to connect Tahoma/Connexoon</li>
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
        <param field="Mode5" label="Log file location" width="300px">
            <description>Enter a location for the logfile (omit final /), or leave empty to create logfile in the domoticz directory.
            <br/>Default directory: '/home/user/domoticz' for raspberry pi</description>
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

import DomoticzEx as Domoticz
import json
import sys
import logging
import exceptions
import time
import tahoma
import os

class BasePlugin:
    enabled = False
    heartbeat = False
    devices = None
    heartbeat_delay = 1
    con_delay = 0
    wait_delay = 30
    json_data = None
    command = False
    refresh = True
    actions_serialized = []
    logger = None
    log_filename = "somfy.log"
    
    def onStart(self):
        if os.path.exists(Parameters["Mode5"]):
            log_dir = Parameters["Mode5"] 
        else:
            Domoticz.Status("Location {0} does not exist, logging to default location".format(Parameters["Mode5"]))
            log_dir = ""
        log_fullname = os.path.join(log_dir, self.log_filename)
        Domoticz.Status("Starting Tahoma blind plugin, logging to file {0}".format(log_fullname))
        self.logger = logging.getLogger('root')
        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(2)
            DumpConfigToLog()
            logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename=log_fullname,level=logging.DEBUG)
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename=log_fullname,level=logging.INFO)
        Domoticz.Debug("os.path.exists(Parameters['Mode5']) = {}".format(os.path.exists(Parameters["Mode5"])))
        logging.info("starting plugin version "+Parameters["Version"])
        self.runCounter = int(Parameters['Mode2'])
        
        logging.debug("starting to log in")
        self.tahoma = tahoma.Tahoma()
        try:
            self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        except exceptions.LoginFailure as exp:
            Domoticz.Error("Failed to login: " + str(exp))
            return
        
        if self.tahoma.logged_in:
            self.tahoma.register_listener()

        if self.tahoma.logged_in and firstFree() < 249:
            self.tahoma.get_devices(Devices)
            
        
    def onStop(self):
        logging.info("stopping plugin")
        self.heartbeat = False

    def onConnect(self, Connection, Status, Description):
        logging.debug("onConnect: Connection: '"+str(Connection)+"', Status: '"+str(Status)+"', Description: '"+str(Description)+"' self.tahoma.logged_in: '"+str(self.tahoma.logged_in)+"'")
        if (Status == 0 and not self.tahoma.logged_in):
          self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
        elif (self.cookie and self.tahoma.logged_in and (not self.command)):
          event_list = self.tahoma.get_events()
          self.update_devices_status(event_list)

        elif (self.command):
          event_list = self.tahoma.tahoma_command(self.json_data)
          self.update_devices_status(event_list)
          self.command = False
          self.heartbeat = False
          self.actions_serialized = []
        else:
          logging.info("Failed to connect to tahoma api")

    def onMessage(self, Connection, Data):
        Domoticz.Error("onMessage called but not implemented")
        Domoticz.Debug("onMessage data: "+str(Data))

    def onCommand(self, DeviceId, Unit, Command, Level, Hue):
        logging.debug("onCommand: DeviceId: '"+str(DeviceId)+"' Unit: '"+str(Unit)+"', Command: '"+str(Command)+"', Level: '"+str(Level)+"', Hue: '"+str(Hue)+"'")
        commands_serialized = []
        action = {}
        commands = {}
        params = []
        
        if Unit == 1:
            # unit 1 used for up/down movement
            if (str(Command) == "Off"):
                commands["name"] = "close"
            elif (str(Command) == "On"):
                commands["name"] = "open"
            elif ("Set Level" in str(Command)):
                commands["name"] = "setClosure"
                tmp = 100 - int(Level)
                params.append(tmp)
                commands["parameters"] = params
        elif Unit == 2:
            # unit 2 used for orientation in venetian blinds
            if ("Set Level" in str(Command)):
                commands["name"] = "setOrientation"
                tmp = max(100 - int(Level), 1) #orientation does not accept 0
                params.append(tmp)
                commands["parameters"] = params
            else:
                logging.error("command "+str(Command)+" not supported")
                return
        else:
            logging.error("unit not supported")
            return

        commands_serialized.append(commands)
        action["deviceURL"] = DeviceId
        action["commands"] = commands_serialized
        self.actions_serialized.append(action)
        logging.debug("preparing command: # commands: "+str(len(commands)))
        logging.debug("preparing command: # actions_serialized: "+str(len(self.actions_serialized)))
        data = {"label": "Domoticz - "+Devices[DeviceId].Units[Unit].Name+" - "+commands["name"], "actions": self.actions_serialized}
        self.json_data = json.dumps(data, indent=None, sort_keys=True)
        logging.debug("preparing command: json data: "+str(self.json_data))

        if (not self.tahoma.logged_in):
            logging.info("Not logged in, must connect")
            self.command = True
            self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
            if self.tahoma.logged_in:
                self.tahoma.register_listener()

        event_list = []
        try:
            event_list = self.tahoma.tahoma_command(self.json_data)
        except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
            Domoticz.Error("Failed to send command: " + str(exp))
            logging.error("Failed to send command: " + str(exp))
            return
        if event_list is not None and len(event_list) > 0:
            self.update_devices_status(event_list)
        self.heartbeat = False
        self.actions_serialized = []

    def onCommand_legacy(self, Unit, Command, Level, Hue):
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

        if (not self.tahoma.logged_in):
            logging.info("Not logged in, must connect")
            self.command = True
            self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
            if self.tahoma.logged_in:
                self.tahoma.register_listener()

        event_list = []
        try:
            event_list = self.tahoma.tahoma_command(self.json_data)
        except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
            Domoticz.Error("Failed to send command: " + str(exp))
            logging.error("Failed to send command: " + str(exp))
            return
        if event_list is not None and len(event_list) > 0:
            self.update_devices_status(event_list)
        self.heartbeat = False
        self.actions_serialized = []

    def onDisconnect(self, Connection):
        return

    def onHeartbeat(self):
        self.runCounter = self.runCounter - 1
        if self.runCounter <= 0:
            logging.debug("Poll unit")
            self.runCounter = int(Parameters['Mode2'])            

            if (self.tahoma.logged_in and (not self.tahoma.startup)):
                if (not self.tahoma.logged_in):
                    self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
                    if self.tahoma.logged_in:
                        self.tahoma.register_listener()
                event_list = []
                try:
                    event_list = self.tahoma.get_events()
                except (exceptions.TooManyRetries, exceptions.FailureWithErrorCode, exceptions.FailureWithoutErrorCode) as exp:
                    Domoticz.Error("Failed to request data: " + str(exp))
                    logging.error("Failed to request data: " + str(exp))
                    return
                if event_list is not None and len(event_list) > 0:
                    self.update_devices_status(event_list)
                self.heartbeat = True

            elif (self.heartbeat and (self.con_delay < self.wait_delay) and (not self.tahoma.logged_in)):
                self.con_delay +=1
                Domoticz.Status("Too many connections waiting before authenticating again")

            elif (self.heartbeat and (self.con_delay == self.wait_delay) and (not self.tahoma.logged_in)):
                if (not self.tahoma.logged_in):
                    self.tahoma.tahoma_login(str(Parameters["Username"]), str(Parameters["Password"]))
                    if self.tahoma.logged_in:
                        self.tahoma.register_listener()
                self.heartbeat = True
                self.con_delay = 0
        else:
            logging.debug("Polling unit in " + str(self.runCounter) + " heartbeats.")

    def update_devices_status(self, Updated_devices):
        logging.debug("updating device status self.tahoma.startup = "+str(self.tahoma.startup)+" on num datasets: "+str(len(Updated_devices)))
        logging.debug("updating device status on data: "+str(Updated_devices))
        for dataset in Updated_devices:
            logging.debug("checking dataset for URL: "+str(dataset["deviceURL"]))
            if dataset["deviceURL"] not in Devices:
                #Domoticz.Error("device not found for URL: "+str(dataset["deviceURL"])+" called "+str(dataset["label"]))
                Domoticz.Error("device not found for URL: "+str(dataset["deviceURL"]))
                break #no deviceURL found that matches to domoticz Devices, skip to next dataset
                #return
            if (dataset["deviceURL"].startswith("io://")):
                dev = dataset["deviceURL"]
                level = 0
                status_num = 0
                status = None

                if (self.tahoma.startup):
                    states = dataset["states"]
                else:
                    states = dataset["deviceStates"]
                    if (dataset["name"] != "DeviceStateChangedEvent"):
                        logging.debug("update_devices_status: dataset['name'] != DeviceStateChangedEvent: "+str(dataset["name"])+": breaking out")
                        break #dataset does not contain correct event, skip to next dataset

                for state in states:
                    status_num = 0

                    if ((state["name"] == "core:ClosureState") or (state["name"] == "core:DeploymentState")):
                        level = int(state["value"])
                        level = 100 - level
                        status_num = 1
                      
                    if ((state["name"] == "core:SlateOrientationState")):
                        level = int(state["value"])
                        level = 100 - level
                        status_num = 2
                      
                    if status_num > 0:
                        if (Devices[dev].Units[status_num].sValue):
                            int_level = int(Devices[dev].Unit[status_num].sValue)
                        else:
                            int_level = 0
                        if (level != int_level):
                            Domoticz.Status("Updating device:"+Devices[dev].Units[status_num].Name)
                            logging.info("Updating device:"+Devices[dev].Units[status_num].Name)
                            if (level == 0):
                                Devices[dev].Units[status_num].nValue = 0
                                Devices[dev].Units[status_num].sValue = "0"
                                Devices[dev].Units[status_num].Update()
                            if (level == 100):
                                Devices[dev].Units[status_num].nValue = 1
                                Devices[dev].Units[status_num].sValue = "100"
                                Devices[dev].Units[status_num].Update()
                            if (level != 0 and level != 100):
                                Devices[dev].Units[status_num].nValue = 2
                                Devices[dev].Units[status_num].sValue = str(level)
                                Devices[dev].Units[status_num].Update()
                                #Devices[dev].Units[1].Update(2,str(level))

        return

    def onDeviceAdded(self, DeviceID, Unit):
        logging.debug("onDeviceAdded called for DeviceID {0} and Unit {1}".format(DeviceID, Unit))

    def onDeviceModified(self, DeviceID, Unit):
        logging.debug("onDeviceModified called for DeviceID {0} and Unit {1}".format(DeviceID, Unit))

    def onDeviceRemoved(self, DeviceID, Unit):
        logging.debug("onDeviceRemoved called for DeviceID {0} and Unit {1}".format(DeviceID, Unit))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onDeviceAdded(DeviceID, Unit):
    global _plugin
    _plugin.onDeviceAdded(DeviceID, Unit)

def onDeviceModified(DeviceID, Unit):
    global _plugin
    _plugin.onDeviceModified(DeviceID, Unit)

def onDeviceRemoved(DeviceID, Unit):
    global _plugin
    _plugin.onDeviceRemoved(DeviceID, Unit)

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(DeviceId, Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(DeviceId, Unit, Command, Level, Color)

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

