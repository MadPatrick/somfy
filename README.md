# domoticz_tahoma_blind
Domoticz plugin writen in Python to first support Velux IO roller shutters using Tahoma/Connexoon, but now it support: blinds, windows, garagedoor, screens and pergolas. Basic support of RTS (Open/Close) is also included without return state (limitation due to RTS), it means for RTS the state of the device won't be updated if the device state is modified outside of domoticz.

This plugin also comply with Somfy's rules about /setup endpoint, **if you are using an old version (previous to 2.0.0) YOU MUST UPDATE, YOU HAVE BEEN WARNED**

To use this plugin you need to install the last stable release of Domoticz https://www.domoticz.com and to install the required python library.

The plugin currently support the following device types: roller Shutters, screens (interior/exterior), awning, pergolas, garage door, windows and blinds(postions only, no slats control).

This plugins use some code from https://github.com/moroen/IKEA-Tradfri-plugin, thanks @moroen for the first free function.

## Installation

Python version 3.4 or higher required & Domoticz version 4.10717 or greater. To install:

First: sudo apt-get install python3 libpython3-dev libpython3.7-dev

Then go in your Domoticz directory using a command line and open the plugins directory.

Run: git clone https://github.com/nonolk/domoticz_tahoma_blind.git

Restart Domoticz with sudo systemctl restart domoticz.

In the web UI, navigate to the Hardware page. In the hardware dropdown list there will be an entry called "Tahoma or conexoon IO blind plugin".

## Issues:

You may see the following error in Domoticz logs:  
*Async Secure Read Exception: 336151548, sslv3 alert bad record mac*
  
Do not open an issue for this, it's coming from corrupted packets received and I can nothing about it.
