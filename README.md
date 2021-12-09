# domoticz_tahoma_blind
Original script was written by Nonolk : https://github.com/nonolk/domoticz_tahoma_blind.git


Domoticz plugin writen in Python to first support Velux IO roller shutters using Tahoma/Connexoon, but now it support: blinds, windows, garagedoor, screens and pergolas. Basic support of RTS (Open/Close) is also included without return state (limitation due to RTS), it means for RTS the state of the device won't be updated if the device state is modified outside of domoticz.

To use this plugin you need to install the last stable release of Domoticz https://www.domoticz.com and to install the required python library.

The plugin currently support the following device types: roller Shutters, screens (interior/exterior), awning, pergolas, garage door, windows and blinds(postions only, no slats control).

## Somfy login

You need to register you Somfy products and add them to your Tahoma or Connexxoon box


https://www.somfy.nl/nieuw-account-aanmaken

https://www.tahomalink.com/enduser-mobile-web/steer-html5-client/tahoma/



## Installation
### Prerequisites
Python version 3.4 or higher required & Domoticz version 4.10717 or greater. 
To install:
```
sudo apt-get update
sudo apt-get install python3 libpython3-dev libpython3.7-dev
sudo apt-get install python3-requests
```

### plugin
Then go in your Domoticz directory using a command line and open the plugins directory.
```
cd domoticz/plugins
git clone https://github.com/MadPatrick/somfy
```
to update:
```
cd domoticz/plugins/somfy
git pull
```

Restart Domoticz with sudo systemctl restart domoticz.

In the web UI, navigate to the Hardware page. In the hardware dropdown list there will be an entry called "Tahoma or conexoon IO blind plugin".
