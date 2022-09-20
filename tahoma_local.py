import requests
import logging
import exceptions
import urllib.parse
import datetime
import time
import json

try:
	import DomoticzEx as Domoticz
except ImportError:
	import fakeDomoticz as Domoticz

class Tahoma:
    def __init__(self):
        self.srvaddr = "tahomalink.com"
        self.base_url = "https://ha101-1.overkiz.com"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.login_url = "/enduser-mobile-web/enduserAPI/login"
        self.timeout = 10
        self.__expiry_date = datetime.datetime.now()
        self.logged_in_expiry_days = 6
        self.pin = {"0000-0000-0000"}
        self.cookie = None
        self.token = None
        self.__logged_in = False

    @property
    def logged_in(self):
        logging.debug("checking logged in status: self.__logged_in = "+str(self.__logged_in)+" and self.__expiry_date >= datetime.datetime.now() = " + str(self.__expiry_date >= datetime.datetime.now()))
        if self.__logged_in and (self.__expiry_date >= datetime.datetime.now()):
            return True
        else:
            return False

    def tahoma_login(self, username, password):
        data = {"userId": username, "userPassword": password}
        response = requests.post(self.base_url + self.login_url, headers=self.headers, data=data, timeout=self.timeout)
        Data = response.json()
        logging.debug("Login respone: status_code: '"+str(response.status_code)+"' reponse body: '"+str(Data)+"'")

        if (response.status_code == 200 and not self.__logged_in):
            self.__logged_in = True
            self.__expiry_date = datetime.datetime.now() + datetime.timedelta(days=self.logged_in_expiry_days)
            logging.info("Tahoma authentication succeeded, login valid until " + self.__expiry_date.strftime("%Y-%m-%d %H:%M:%S"))
            #self.cookie = response.cookies
            self.cookie = response.cookies
            logging.debug("login: cookies: '"+ str(response.cookies)+"', headers: '"+str(response.headers)+"'")
            #self.register_listener()

        elif ((response.status_code == 401) or (response.status_code == 400)):
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

    def generate_token(self, pin):
        url_gen = "/enduser-mobile-web/enduserAPI/config/"+pin+"/local/tokens/generate"
        headers_gen = {"Content-Type": "application/json"}
        logging.debug("generate token: url_gen = '" + url_gen + "'")
        logging.debug("generate token: headers_gen = '" + str(headers_gen) + "'")
        logging.debug("generate token: cookie = '" + str(self.cookie) + "'")
        response = requests.get(self.base_url + url_gen, headers=headers_gen, cookies=self.cookie)
        
        if response.status_code == 200:
            logging.debug("succeeded to activate token: " + str(self.token))
        elif ((response.status_code == 401) or (response.status_code == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to generate token")
            raise exceptions.LoginFailure("failed to generate token")

    def activate_token(self, pin):
        url_act = "/enduser-mobile-web/enduserAPI/config/"+pin+"/local/tokens"
        headers_act = {"Content-Type": "application/json"}
        data_act = {"label": "Toto token", "token": self.token, "scope": "devmode"}
        respone = requests.post(self.base_url + url_act, headers=headers_act, json=data_act)

        if response.status_code == 200:
            self.token = response.json()['token']
            logging.debug("succeeded to generate token: " + str(self.token))
        elif ((Status == 401) or (Status == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to generate token")
            raise exceptions.LoginFailure("failed to generate token")

    def the_rest():
        ## Generate a token

        r_gen.status_code

        r_gen.text
        '{"token":"XXXXXXXXXXXXXXXX"}'

        ## Activate your token
        url_act = "https://ha101-1.overkiz.com/enduser-mobile-web/enduserAPI/config/MY_PIN/local/tokens"
        headers_act = {"Content-Type": "application/json"}
        data_act = {"label": "My token", "token": r_gen.json()['token'], "scope": "devmode"}
        r_act = s.post(url_act, headers=headers_act, json=data_act)

        r_act.status_code
