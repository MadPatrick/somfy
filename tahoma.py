import requests
import logging
import exceptions
import urllib.parse
import datetime
import time

try:
	import DomoticzEx as Domoticz
except ImportError:
	import fakeDomoticz as Domoticz

class Tahoma:
    """class to interface with tahoma web API"""
    def __init__(self):
        self.srvaddr = "tahomalink.com"
        self.base_url = "https://tahomalink.com:443"
        self.login_url = "/enduser-mobile-web/enduserAPI/login"
        self.cookie = None
        self.listenerId = None
        self.__logged_in = False
        self.startup = True
        #self.heartbeat = False
        self.devices = None
        self.filtered_devices = None
        self.events = None
        self.heartbeat_delay = 1
        self.con_delay = 0
        self.wait_delay = 30
        self.json_data = None
        self.refresh = True
        self.timeout = 10
        self.__expiry_date = datetime.datetime.now()
        self.logged_in_expiry_days = 6
        self.execId = None

    @property
    def logged_in(self):
        logging.debug("checking logged in status: self.__logged_in = "+str(self.__logged_in)+" and self.__expiry_date >= datetime.datetime.now() = " + str(self.__expiry_date >= datetime.datetime.now()))
        if self.__logged_in and (self.__expiry_date >= datetime.datetime.now()):
            return True
        else:
            return False

    def tahoma_login(self, username, password):

        #url = self.base_url + '/enduser-mobile-web/enduserAPI/login'
        url = self.base_url + self.login_url 
        headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded"}
        data = "userId="+urllib.parse.quote(username)+"&userPassword="+urllib.parse.quote(password)+""
        response = requests.post(url, data=data, headers=headers, timeout=self.timeout)

        Status = response.status_code
        Data = response.json()
        logging.debug("Login respone: status_code: '"+str(Status)+"' reponse body: '"+str(Data)+"'")

        if (Status == 200 and not self.__logged_in):
            self.__logged_in = True
            self.__expiry_date = datetime.datetime.now() + datetime.timedelta(days=self.logged_in_expiry_days)
            logging.info("Tahoma authentication succeeded, login valid until " + self.__expiry_date.strftime("%Y-%m-%d %H:%M:%S"))
            #self.cookie = response.cookies
            self.cookie = response.headers["Set-Cookie"]
            logging.debug("login: cookies: '"+ str(response.cookies)+"', headers: '"+str(response.headers)+"'")
            #self.register_listener()

        elif ((Status == 401) or (Status == 400)):
            strData = Data["error"]
            #logging.error("Tahoma error: must reconnect")
            self.__logged_in = False
            self.cookie = None
            self.listenerId = None

            if ("Too many" in strData):
                logging.error("Too many connections, must wait")
                #self.heartbeat = True
                raise exceptions.LoginFailure("Too many connections, must wait")
            elif ("Bad credentials" in strData):
                logging.error("login failed: Bad credentials, please update credentials and restart plugin")
                #self.heartbeat =  False
                raise exceptions.LoginFailure("Bad credentials, please update credentials and restart plugin")
            else:
                logging.error("login failed, unhandled reason: "+strData)
                raise exceptions.LoginFailure("login failed, unhandled reason: "+strData)

            if (not self.__logged_in):
                self.tahoma_login(username, password)
                return
        return self.__logged_in

    def get_devices(self, Devices):
        logging.debug("start get devices")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/x-www-form-urlencoded", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/setup/devices'
        response = requests.get(url, headers=Headers, timeout=self.timeout)
        logging.debug("get device response: url '" + str(response.url) + "' response headers: '"+str(response.headers)+"'")
        logging.debug("get device response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("get_devices: error during get devices, status: " + str(response.status_code))
            Domoticz.Error("get_devices: error during get devices, status: " + str(response.status_code))
            return

        Data = response.json()

        if (not "uiClass" in response.text):
            logging.error("get_devices: missing uiClass in response")
            Domoticz.Error("get_devices: missing uiClass in response")
            logging.debug(str(Data))
            return

        self.devices = Data

        self.filtered_devices = list()
        for device in self.devices:
            logging.debug("get_devices: Device name: "+device["label"]+" Device class: "+device["uiClass"])
            if (((device["uiClass"] == "RollerShutter") 
                or (device["uiClass"] == "LightSensor") 
                or (device["uiClass"] == "ExteriorScreen") 
                or (device["uiClass"] == "Screen") 
                or (device["uiClass"] == "Awning") 
                or (device["uiClass"] == "Pergola") 
                or (device["uiClass"] == "GarageDoor") 
                or (device["uiClass"] == "Window") 
                or (device["uiClass"] == "VenetianBlind") 
                or (device["uiClass"] == "ExteriorVenetianBlind")) 
                and ((device["deviceURL"].startswith("io://")) or (device["deviceURL"].startswith("rts://")))):
                self.filtered_devices.append(device)
                logging.info("supported device found: "+ str(device))
            else:
                logging.debug("unsupported device found: "+ str(device))

        logging.debug("get_devices: devices found, domoticz: "+str(len(Devices))+" API: "+str(len(self.filtered_devices))+", self.startup: "+str(self.startup))

        if ((len(Devices) <= len(self.filtered_devices)) or self.startup):
            #Domoticz devices already present but less than from API or starting up
            logging.debug("New device(s) detected")

            for device in self.filtered_devices:
                found = False
                logging.debug("check if need to create device: "+device["label"])
                if device["label"] in Devices:
                    logging.debug("get_devices: step 1, do not create new device: "+device["label"]+", device already exists")
                    found = True
                    #break
                for domo_dev in Devices:
                    if domo_dev == device["deviceURL"]:
                        logging.debug("get_devices: step 2, do not create new device: "+device["label"]+", device already exists")
                        found = True
                        break
                if (found==False):
                    #DeviceID not found, create new one
                    swtype = None

                    logging.debug("get_devices: Must create new device: "+device["label"])

                    if (device["deviceURL"].startswith("io://")):
                        deviceType = 244
                        swtype = 13
                        subtype2 = 73
                        if (device["uiClass"] == "Awning"):
                            swtype = 13
                        elif (device["uiClass"] == "RollerShutter"):
                            swtype = 21
                            deviceType = 244
                            subtype2 = 73                    
                        elif (device["uiClass"] == "LightSensor"):
                            swtype = 12
                            deviceType = 246
                            subtype2 = 1
                    elif (device["deviceURL"].startswith("rts://")):
                        swtype = 6

                    # extended framework: create first device then unit? or create device+unit in one go?
                    Domoticz.Device(DeviceID=device["deviceURL"]) #use deviceURL as identifier for Domoticz.Device instance
                    if (device["uiClass"] == "VenetianBlind" or device["uiClass"] == "ExteriorVenetianBlind"):
                        #create unit for up/down and open/close for venetian blinds
                        Domoticz.Unit(Name=device["label"] + " up/down", Unit=1, Type=deviceType, Subtype=subtype2, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()
                        Domoticz.Unit(Name=device["label"] + " orientation", Unit=2, Type=244, Subtype=73, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()
                    else:
                        #create a single unit for all other device types
                        Domoticz.Unit(Name=device["label"], Unit=1, Type=deviceType, Subtype=subtype2, Switchtype=swtype, DeviceID=device["deviceURL"]).Create()
                     
                    logging.info("New device created: "+device["label"])
                else:
                    found = False
        self.startup = False
        logging.debug("finished get devices")
        self.get_events()

    def get_events(self):
        logging.debug("start get events")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/events/'+self.listenerId+'/fetch'

        for i in range(1,4):
            #do several retries on reaching events end point before going to time out error
            try:
                response = requests.post(url, headers=Headers, timeout=self.timeout)
                logging.debug("get events response: status '" + str(response.status_code) + "' response body: '"+str(response)+"'")
                #logging.debug("get events response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
                if response.status_code != 200:
                    logging.error("error during get events, status: " + str(response.status_code) + ", " + str(response.text))
                    self.__logged_in = False
                    return
                elif (response.status_code == 200 and self.__logged_in and (not self.startup)):
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

                        return filtered_events
                        #self.update_devices_status(filtered_events)

                # elif (response.status_code == 200 and (not self.heartbeat)):
                  # return
                else:
                  logging.info("Return status " + str(response.status_code))
            except requests.exceptions.RequestException as exp:
                logging.error("get_events RequestException: " + str(exp))
            #wait increasing time before next try
            time.sleep(i ** 3)
        else:
            raise exceptions.TooManyRetries
        logging.debug("finished get events")

    def register_listener(self):
        logging.debug("start register")
        Headers = { 'Host': self.srvaddr,"Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        response = requests.post(self.base_url + '/enduser-mobile-web/enduserAPI/events/register', headers=Headers, timeout=self.timeout)
        logging.debug("register response: status '" + str(response.status_code) + "' response body: '"+str(response)+"'")
        if response.status_code != 200:
            self.handle_response(response, "register listener")
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
        #self.get_devices()

    def send_command(self, json_data):
        timeout = 4
        logging.debug("start command")
        Headers = { 'Host': self.srvaddr, "Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        logging.info("Sending command to tahoma api")
        logging.debug("onCommand: headers: '"+str(Headers)+"', data '"+str(json_data)+"'")
        try:
            response = requests.post(self.base_url + '/enduser-mobile-web/enduserAPI/exec/apply', headers=Headers, data=json_data, timeout=timeout)
        except requests.exceptions.RequestException as exp:
            logging.error("Send command returns RequestException: " + str(exp))
            return ""

        logging.debug("command response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code == 200:
            logging.debug("succeeded to post command: " + str(response.json()))
            self.execId = response.json()['execId']
        else:
            self.__logged_in = False
            self.handle_response(response, "send command")
        #event_list = self.get_events()
        return response.json()

    def handle_response(self, response, action):
        """handle faulty responses"""
        if response.status_code >= 300 and response.status_code < 400:
            logging.error("status code " + str(response.status_code) + " this is likely a bug")
            raise exceptions.TahomaException("failed request during "+ action + ": " + str(response.status_code))
        elif response.status_code == 400:
            logging.error("status code " + str(response.status_code) + " this is a bug, bad request made, url or body needs to be checked")
            raise exceptions.TahomaException("failed request during "+ action + ", check url or body: " + str(response.status_code))
        elif response.status_code == 401:
            logging.error("status code " + str(response.status_code) + " authorisation failed, check credentials")
            raise exceptions.TahomaException("failed request during "+ action + ", check credentials: " + str(response.status_code))
        elif response.status_code == 404:
            logging.error("status code " + str(response.status_code) + " server not found")
            raise exceptions.TahomaException("failed request during "+ action + ", server not found: " + str(response.status_code))
        elif response.status_code >= 500:
            logging.error("status code " + str(response.status_code) + " a server sided problem")
            raise exceptions.TahomaException("failed request during "+ action + ": " + str(response.status_code))
        else:
            logging.error("status code " + str(response.status_code))
            raise exceptions.TahomaException("failed request during "+ action + ": " + str(response.status_code))        
        return
