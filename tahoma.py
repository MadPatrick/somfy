import requests
import logging
import exceptions
import urllib.parse
import datetime

class Tahoma:
    def __init__(self):
        self.srvaddr = "tahomalink.com"
        self.base_url = "https://tahomalink.com:443"
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

    @property
    def logged_in(self):
        logging.debug("checking logged in status: self.__logged_in = 3"+str(self.__logged_in)+" and self.__expiry_date <= datetime.datetime.now() = " + str(self.__expiry_date <= datetime.datetime.now()))
        if self.__logged_in and (self.__expiry_date <= datetime.datetime.now()):
            return True
        else:
            return False
    
    def tahoma_login(self, username, password):

        url = self.base_url + '/enduser-mobile-web/enduserAPI/login'
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

    def tahoma_command(self, json_data):
        timeout = 4
        logging.debug("start command")
        Headers = { 'Host': self.srvaddr, "Connection": "keep-alive","Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Content-Type": "application/json", "Cookie": self.cookie}
        url = self.base_url + '/enduser-mobile-web/enduserAPI/exec/apply'
        logging.debug("onCommand: headers: '"+str(Headers)+"', data '"+str(json_data)+"'")
        logging.info("Sending command to tahoma api")
        try:
            response = requests.post(url, headers=Headers, data=json_data, timeout=timeout)
        except requests.exceptions.RequestException as exp:
            logging.error("Send command returns RequestException: " + str(exp))

        logging.debug("command response: status '" + str(response.status_code) + "' response body: '"+str(response.json())+"'")
        if response.status_code != 200:
            logging.error("error during command, status: " + str(response.status_code) + ", possible cause:" + str(response.json()))
            self.__logged_in = False
            return ""
        self.executionId = response.json()['execId']
        event_list = self.get_events()
        return event_list

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
        #self.get_devices()

    def get_devices(self, Devices):
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
                #logging.debug("get events: self.__logged_in = '"+str(self.__logged_in)+"' and self.heartbeat = '"+str(self.heartbeat)+"' and self.startup = '"+str(self.startup))
                if response.status_code != 200:
                    logging.error("error during get events, status: " + str(response.status_code) + ", " + str(response.text))
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
                  logging.info("Return status"+str(response.status_code))
            except requests.exceptions.RequestException as exp:
                logging.error("get_events RequestException: " + str(exp))
            time.sleep(i ** 3)
        else:
            raise exceptions.TooManyRetries
