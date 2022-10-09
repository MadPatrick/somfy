#
#   Fake Domoticz - Domoticz Python plugin stub
#
#   With thanks to Frank Fesevur, 2017
#
#   Very simple module to make local testing easier
#   It "emulates" Domoticz.Log(), Domoticz.Error and Domoticz.Debug()
#   It also emulates the Device and Unit from the Ex framework
#
Devices = [""]

class myUnit:
    def __init__(self,Name="label", Unit=0, Type=0, Subtype=0, Switchtype="", DeviceID="deviceURL"):
        self.Name=Name
        self.Unit=Unit,
        self.Type=Type
        self.Subtype=Subtype
        self.Switchtype=Switchtype
        self.DeviceID=DeviceID
    def Create(self):
        print("Creating unit "+self.Name+" for deviceID "+self.DeviceID)

class Domoticz:
    def __init__(self):
        self.Units = []
        return

    def Log(self, s):
        print(s)

    def Status(self, s):
        print(s)

    def Error(self, s):
        print(s)

    def Debug(self, s):
        print(s)
    
    def Device(self, DeviceID=""):
        print("creating DeviceID: "+ DeviceID)

    def Unit(self, Name="label", Unit=0, Type=0, Subtype=0, Switchtype="", DeviceID="deviceURL"):
        newUnit = myUnit(Name, Unit, Type, Subtype, Switchtype, DeviceID)
        self.Units.append(newUnit)
        return newUnit
