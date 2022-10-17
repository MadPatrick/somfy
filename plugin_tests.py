import unittest
import logging
import plugin
from tests.devicelist import *
from tests.devicelistWeb import *
from utils import *

class PluginTests(unittest.TestCase):
    def setUp(self):
        self.thePlug=plugin.BasePlugin()
        logging.info("===start unit test run===")

    def test_createDevicesWeb(self):
        logging.info("test: test_createDevicesWeb")
        self.assertEqual(self.thePlug.create_devices(filter_devices(deviceListWeb)), (2,2))

    def test_createDevicesLocal(self):
        logging.info("test: test_createDevicesLocal")
        self.assertEqual(self.thePlug.create_devices(filter_devices(deviceList)), (2,2))

    def test_updateDevicesLocal(self):
        logging.info("test: test_createDevicesLocal")
        self.assertEqual(self.thePlug.create_devices(filter_devices(deviceList)), (2,2))

def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename="somfy_unit_test.log",level=logging.DEBUG)
    unittest.main()


if __name__ == "__main__":
    main()
