import unittest
import logging

class PluginTests(unittest.TestCase):



def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(filename)-18s - %(message)s', filename="goodwe_test.log",level=logging.DEBUG)
    unittest.main()


if __name__ == "__main__":
    main()
