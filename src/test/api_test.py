import base64
import os
import traceback
import unittest
import requests
from requests.auth import HTTPBasicAuth
import yaml


class ApiTest(unittest.TestCase):

    def test_discovery(self):
        url = "http://localhost:6100/"
        response = requests.get(url)
        status_code = response.status_code
        self.assertEquals(status_code, 404)

    def test_discovery_no_auth_no_accept(self):
        url = "http://localhost:6100/taxii2"
        response = requests.get(url)
        status_code = response.status_code
        self.assertEquals(status_code, 401)

    def test_discovery_auth_only_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "http://localhost:6100/taxii2"
        response = requests.get(url, auth=HTTPBasicAuth(user,passwd))
        status_code = response.status_code

        self.assertEquals(status_code, 406)

    def test_discovery_auth_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "http://{}:{}/taxii2".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd), headers={'Accept':'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEquals(status_code, 200)

    def test_discovery_auth_accept_wrong_user_pass(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("BASE_URL")
        port = cf.get("PORT")
        user = "blabla"
        passwd = "blabla"

        url = "http://{}:{}/taxii2".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEquals(status_code, 401)

    def test_discovery_auth_accept_right_user_wrong_password(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("BASE_URL")
        port = cf.get("PORT")
        user = cf.get("USER")
        passwd = "blabla"
        url = "http://{}:{}/taxii2".format(base_url,port)

        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEquals(status_code, 401)







    def read_config_file(self, filepath):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        print(file_directory)
        try:
            with open('{}/{}'.format(file_directory, filepath)) as f:
                config = yaml.safe_load(f)
                return config
            # end with
        except Exception:
            print(traceback.format_exc())
            return None
