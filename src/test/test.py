import binascii
import os
import traceback
import unittest
import yaml
from flask import app

from src import *
from src.database.data_handling import *


class Test(unittest.TestCase):

    def test_data_handling(self):
        with self.assertRaises(TypeError):
            p = DataHandler(0, 0, 0)

        with self.assertRaises(TypeError):
            p = DataHandler('', '', '')

        with self.assertRaises(TypeError):
            p = DataHandler('blabla.com', '1', '1')

    def test_db(self):
        pass

    def test_config(self):
        pass

    def test_communication_db_api(self):
        pass

    def test_online_avaibility(self):
        pass

    def user_auth_api(self):
        pass
