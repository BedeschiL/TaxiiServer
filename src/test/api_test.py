import base64
import json
import os
import traceback
import unittest
import requests
from requests.auth import HTTPBasicAuth
import yaml

from src.API.api import app


class ApiTest(unittest.TestCase):
    """
    TEST DISCOVERY
    """

    def test_discovery(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        url = "{}:{}/taxii2".format(base_url, port)
        response = requests.get(url)
        status_code = response.status_code
        self.assertEqual(status_code, 401)

    def test_discovery_no_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")

        url = "{}:{}/taxii2".format(base_url, port)
        response = requests.get(url)
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_discovery_auth_only_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/taxii2".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd))
        status_code = response.status_code

        self.assertEqual(status_code, 406)

    def test_discovery_auth_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/taxii2".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_discovery_auth_accept_wrong_user_pass(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        user = "blabla"
        passwd = "blabla"

        url = "{}:{}/taxii2".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_discovery_auth_accept_right_user_wrong_password(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        user = cf.get("USER")
        passwd = "blabla"
        url = "{}:{}/taxii2".format(base_url, port)

        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    """
    TEST API ROOT
    """

    def test_api_root(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        url = "{}:{}/example1".format(base_url, port)
        response = requests.get(url)
        status_code = response.status_code
        self.assertEqual(status_code, 401)

    def test_api_root_no_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")

        url = "{}:{}/example1".format(base_url, port)
        response = requests.get(url)
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_api_root_auth_only_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd))
        status_code = response.status_code

        self.assertEqual(status_code, 406)

    def test_api_root_auth_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_api_root_auth_accept_wrong_user_pass(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        user = "blabla"
        passwd = "blabla"

        url = "{}:{}/example1".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_api_root_auth_accept_right_user_wrong_password(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        user = cf.get("USER")
        passwd = "blabla"
        url = "{}:{}/example1".format(base_url, port)

        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    """
    TEST COLLECTION
    """

    def test_collections(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        url = "{}:{}/example1/collections".format(base_url, port)
        response = requests.get(url)
        status_code = response.status_code
        self.assertEqual(status_code, 401)

    def test_collections_no_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")

        url = "{}:{}/example1/collections".format(base_url, port)
        response = requests.get(url)
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_collections_auth_only_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd))
        status_code = response.status_code

        self.assertEqual(status_code, 406)

    def test_collections_auth_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_collections_auth_accept_wrong_user_pass(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        user = "blabla"
        passwd = "blabla"

        url = "{}:{}/example1/collections".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_collections_auth_accept_right_user_wrong_password(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        user = cf.get("USER")
        passwd = "blabla"
        url = "{}:{}/example1/collections".format(base_url, port)

        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    """
    TEST OBJECTS
    """

    def test_get_object_auth(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_object_no_auth_usr(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = "fail"
        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_no_auth_passwd(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = "Lol"
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = "Lol"
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    """
    TEST OBJECTS BY ID
    """

    def test_get_object_by_id_auth(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68" \
              "-a3e7-9ec7d755b4c3".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_object_by_id_no_auth_usr(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = "fail"
        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7" \
              "-9ec7d755b4c3".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_by_id_no_auth_passwd(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = "Lol"
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7-9ec7d755b4c3".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_by_id_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7-9ec7d755b4c3".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'aa': '/FAIL+json;version=2.1'})
        status_code = response.status_code
        self.assertEqual(status_code, 406)

    """
    TEST OBJECTS BY ID & VERSION
    """

    def test_get_object_by_id_version_auth(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68" \
              "-a3e7-9ec7d755b4c3/versions/".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_object_by_id_version_no_auth_usr(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = "fail"
        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7" \
              "-9ec7d755b4c3/versions/".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_by_id_version_no_auth_passwd(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = "Lol"
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68" \
              "-a3e7-9ec7d755b4c3/versions/".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_by_id_version_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68" \
              "-a3e7-9ec7d755b4c3/versions/".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'aa': '/FAIL+json;version=2.1'})
        status_code = response.status_code
        self.assertEqual(status_code, 406)

    """
    TEST OBJECT MANIFEST
    """

    def test_get_object_manifest_auth(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/manifest/".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_object_manifest_no_auth_usr(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = "fail"
        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/manifest/".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_manifest_no_auth_passwd(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = "Lol"
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68" \
              "-a3e7-9ec7d755b4c3/versions/".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_object_manifest_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/manifest/".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'aa': '/FAIL+json;version=2.1'})
        status_code = response.status_code
        self.assertEqual(status_code, 406)

    """
    TEST STATUS
    """

    def test_get_status_auth(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/status/212715e0-a2a0-4514-9afa-7670bc7f63b8".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_status_no_auth_usr(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = "fail"
        url = "{}:{}/example1/status/212715e0-a2a0-4514-9afa-7670bc7f63b8".format(base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_status_no_auth_passwd(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = "Lol"
        user = cf.get("USER")

        url = "{}:{}/example1/status/212715e0-a2a0-4514-9afa-7670bc7f63b8".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'Accept': 'application/taxii+json;version=2.1'})
        status_code = response.status_code

        self.assertEqual(status_code, 401)

    def test_get_status_auth_no_accept(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")

        url = "{}:{}/example1/status/212715e0-a2a0-4514-9afa-7670bc7f63b8".format(
            base_url, port)
        response = requests.get(url, auth=HTTPBasicAuth(user, passwd),
                                headers={'aa': '/FAIL+json;version=2.1'})
        status_code = response.status_code
        self.assertEqual(status_code, 406)

    """
    TEST POST/ADD OBJECT
    """

    def setUp(self):
        self.app = app.test_client()

    def test_add_api_root_collections_object(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")
        credentials = base64.b64encode(f'{user}:{passwd}'.encode('utf-8')).decode('utf-8')
        print(credentials)
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        object_to_add = {
            "objects": [
                {
                    "type": "bundle",
                    "id": "bundle--164fd1ad-4888-48bf-8eed-71605412b46f",
                    "objects": [
                        {
                            "type": "identity",
                            "spec_version": "2.1",
                            "id": "identity--15c02107-bd7a-479d-8c21-375e39f2ad63",
                            "created": "2023-04-14T13:30:46.000Z",
                            "modified": "2023-04-14T13:30:46.000Z",
                            "name": "KOR Labs",
                            "identity_class": "organization"
                        },
                        {
                            "type": "grouping",
                            "spec_version": "2.1",
                            "id": "grouping--164fd1ad-4888-48bf-8eed-71605412b46f",
                            "created_by_ref": "identity--15c02107-bd7a-479d-8c21-375e39f2ad63",
                            "created": "2023-04-14T13:30:46.000Z",
                            "modified": "2023-04-14T13:30:46.000Z",
                            "name": "Phishing URL findings",
                            "context": "suspicious-activity",
                            "object_refs": [
                                "x-misp-attribute--9a113c1e-f3dc-495d-9f03-c537d7076336",
                                "observed-data--e7c33a5b-f124-4b95-8de2-9e62c2cd986a",
                                "file--e7c33a5b-f124-4b95-8de2-9e62c2cd986a",
                                "artifact--e7c33a5b-f124-4b95-8de2-9e62c2cd986a",
                                "observed-data--de2f66f9-aa7a-44ea-a03f-cc27eceab47a",
                                "domain-name--de2f66f9-aa7a-44ea-a03f-cc27eceab47a",
                                "observed-data--66ed6682-9fe6-4d96-bdd1-00cfbf4e7bd5",
                                "domain-name--66ed6682-9fe6-4d96-bdd1-00cfbf4e7bd5",
                                "x-misp-attribute--6c2f6612-e725-45c4-8e94-5c82b0d10c94",
                                "x-misp-attribute--74727320-1c07-4312-b72d-7fc715d9694f",
                                "x-misp-attribute--23b7e1ef-5669-417b-aa5f-35f91c80e1af",
                                "x-misp-object--2328a4a2-d609-4aaf-a9c6-a09e99d95669",
                                "observed-data--a0265546-857f-4d76-94bf-b59cf7e14417",
                                "autonomous-system--a0265546-857f-4d76-94bf-b59cf7e14417",
                                "x-misp-object--871547d7-9726-46e0-b5f7-21379161c0ca",
                                "x-misp-object--12069eae-9ae0-412f-a3d5-116934757208",
                                "x-misp-object--dd176e66-2cc0-422d-9033-d22660cb5dd3"
                            ],
                            "labels": [
                                "Threat-Report",
                                "misp:tool=\"MISP-STIX-Converter\"",
                                "Phishing"
                            ],
                            "object_marking_refs": [
                                "marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"
                            ]
                        }
                    ]
                }
            ]

        }
        data = json.dumps(object_to_add)
        cf = self.read_config_file("../API/config/api_config.yaml")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")

        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects".format(
            base_url, port)
        response = requests.post(url, headers=headers, data=data)
        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': '',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        response = requests.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 406)

        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': ''
        }
        response = requests.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 415)

        credentials = base64.b64encode(f'{"blabla"}:{passwd}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        response = requests.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 401)

        credentials = base64.b64encode(f'{user}:{"bla"}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        response = requests.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 401)

    def test_delete_api_root_collections_object(self):
        cf = self.read_config_file("../API/config/api_config.yaml")
        passwd = cf.get("PASSWORD")
        user = cf.get("USER")
        base_url = cf.get("TEST_BASE_URL")
        port = cf.get("PORT")
        credentials = base64.b64encode(f'{user}:{passwd}'.encode('utf-8')).decode('utf-8')
        print(credentials)
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        url = "{}:{}/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--164fd1ad-4888-48bf-8eed-71605412b46f".format(
            base_url, port)
        response = requests.delete(url, headers=headers)
        self.assertEqual(200,response.status_code)
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': '',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 406)

        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code,200 )

        credentials = base64.b64encode(f'{"blabla"}:{passwd}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 401)

        credentials = base64.b64encode(f'{user}:{"bla"}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/taxii+json;version=2.1',
            'Content-Type': 'application/taxii+json;version=2.1'
        }
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 401)

    """
    TEST READ CONFIG
    """
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
