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

class TahomaWebApi:
    def __init__(self):
        self.base_url = "https://ha101-1.overkiz.com"
        self.headers_url = {"Content-Type": "application/x-www-form-urlencoded"}
        self.headers_json = {"Content-Type": "application/json"}
        self.login_url = "/enduser-mobile-web/enduserAPI/login"
        self.timeout = 10
        self.__expiry_date = datetime.datetime.now()
        self.logged_in_expiry_days = 6
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
        response = requests.post(self.base_url + self.login_url, headers=self.headers_url, data=data, timeout=self.timeout)
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
        logging.debug("generate token: url_gen = '" + url_gen + "'")
        logging.debug("generate token: cookie = '" + str(self.cookie) + "'")
        response = requests.get(self.base_url + url_gen, headers=self.headers_json, cookies=self.cookie)
        
        if response.status_code == 200:
            self.token = response.json()['token']
            logging.debug("succeeded to activate token: " + str(self.token))
        elif ((response.status_code == 401) or (response.status_code == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to generate token")
            raise exceptions.LoginFailure("failed to generate token")
        return response.json()

    def activate_token(self, pin):
        url_act = "/enduser-mobile-web/enduserAPI/config/"+pin+"/local/tokens"
        data_act = {"label": "Domoticz token", "token": self.token, "scope": "devmode"}
        response = requests.post(self.base_url + url_act, headers=self.headers_json, json=data_act, cookies=self.cookie)

        if response.status_code == 200:
            #self.token = response.json()['token']
            logging.debug("succeeded to activate token: " + str(self.token))
        elif ((response.status_code == 401) or (response.status_code == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to activate token")
            raise exceptions.LoginFailure("failed to activate token")
        return response.json()

    def get_tokens(self, pin):
        url_act = "/enduser-mobile-web/enduserAPI/config/"+pin+"/local/tokens/devmode"
        response = requests.get(self.base_url + url_act, headers=self.headers_json, cookies=self.cookie)

        if response.status_code == 200:
            #self.token = response.json()['token']
            logging.debug("succeeded to get tokens: " + str(response.json()))
        elif ((response.status_code == 401) or (response.status_code == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to get tokens")
            raise exceptions.LoginFailure("failed to get tokens")
        return response.json()

    def delete_tokens(self, pin, uuid):
        url_del = "/enduser-mobile-web/enduserAPI/config/"+pin+"/local/tokens/"+str(uuid)
        response = requests.delete(self.base_url + url_del, headers=self.headers_json, cookies=self.cookie)

        if response.status_code == 200:
            logging.debug("succeeded to delete token: " + str(response.json()))
        elif ((response.status_code == 401) or (response.status_code == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to delete token")
            raise exceptions.LoginFailure("failed to delete tokens")
        return response.json()

class SomfyBox:
    def __init__(self, pin, port):
        self.base_url = "https://gateway-" + str(pin) + ".local:" + str(port) + "/enduser-mobile-web/1/enduserAPI"
        self.headers_json = {"Content-Type": "application/json", "Authorization": "Bearer "}

    def set_token(self, token):
        self.headers_json["Authorization"] = "Bearer " + str(token)

    def get_version(self):
        response = requests.get(self.base_url + "/apiVersion", headers=self.headers_json)
        if response.status_code == 200:
            logging.debug("succeeded to get API version: " + str(response.json()))
        elif ((response.status_code == 401) or (response.status_code == 400)):
            self.__logged_in = False
            self.cookie = None
            logging.error("failed to get API version")
            raise exceptions.LoginFailure("failed to get API version")
        return response.json()


