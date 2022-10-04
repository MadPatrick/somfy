import logging
import exceptions

def filter_devices(Data):
    logging.debug("start filter devices")

    if (not "uiClass" in json.dumps(Data)):
        logging.error("filter_devices: missing uiClass in response")
        logging.debug(str(Data))
        return

    filtered_devices = list()
    for device in Data:
        logging.debug("filter_devices: Device name: "+device["label"]+" Device class: "+device["uiClass"])
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
            filtered_devices.append(device)
            logging.info("supported device found: "+ str(device))
        else:
            logging.debug("unsupported device found: "+ str(device))

    logging.debug("finished filter devices")
    return filtered_devices

def handle_response(response, action):
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
