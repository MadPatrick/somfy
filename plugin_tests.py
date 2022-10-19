import unittest
import logging
import plugin
from tests.devicelist import *
from tests.devicelistWeb import *
from tests.eventsLocal import *
from tests.eventsWeb import *
from utils import *
from params import *
from tahoma_local import SomfyBox
from tahoma import Tahoma

class PluginTestsLocal(unittest.TestCase):
    """test cases for local API"""
    def setUp(self):
        self.thePlug=plugin.BasePlugin()
        self.thePlug.local = True
        self.thePlug.tahoma = SomfyBox(p_pin, p_port)
        logging.info("===start unit test run===")

    def test_createDevices(self):
        logging.info("test: test_createDevices Local")
        self.assertEqual(self.thePlug.create_devices(filter_devices(deviceList)), (2,2))

    def test_updateDevicesLocal(self):
        logging.info("test: test_updateDevices Local")
        self.assertEqual(self.thePlug.update_devices_status(eventsLocal), 0)

class PluginTestsWeb(unittest.TestCase):
    """test cases for web API"""
    def setUp(self):
        self.thePlug=plugin.BasePlugin()
        self.thePlug.local = False
        self.thePlug.tahoma = Tahoma()
        logging.info("===start unit test run===")

    def test_createDevices(self):
        logging.info("test: test_createDevices Web")
        self.assertEqual(self.thePlug.create_devices(filter_devices(deviceListWeb)), (2,2))

    def test_updateDevices(self):
        logging.info("test: test_updateDevices Web")
        self.assertEqual(self.thePlug.update_devices_status(eventsWeb), 0)

def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename="somfy_unit_test.log",level=logging.DEBUG)
    unittest.main()


if __name__ == "__main__":
    main()
