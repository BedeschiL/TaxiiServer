import os
import traceback

import yaml
from bson import ObjectId
from pymongo import MongoClient


class MongoHandler:
    def __init__(self, url, username, password):
        self.dbClient = MongoClient(url, username=username, password=password, authSource='admin',
                                    authMechanism='SCRAM-SHA-256')

    def drop_db_and_collection(self):
        dblist = self.dbClient.list_database_names()

        # A°)
        # 1°) TEST FOR DATABASES EXIST
        db_name = "discovery_database"
        if db_name in dblist:
            print("The database  {} exists.".format(db_name))
            self.dbClient.drop_database(db_name)
            print("The database {} is dropped.".format(db_name))

        db_name = "example1"
        if db_name in dblist:
            print("The database {} exists.".format(db_name))
            self.dbClient.drop_database(db_name)
            print("The database {} is dropped.".format(db_name))

    def build_db_and_collection(self):
        # Creation discovery DB :
        db = self.dbClient["discovery_database"]
        mycol = db["discovery_information"]
        mydict = {
            "title": "Louis's Taxi Server",
            "description": "First version of louis's taxii Server",
            "contact": "louis.bedeschi@gmail.com",
            "default": "dafault path of api (it's an url)",
            "api_roots": ["https://localhost:6100/example1/"]
        }
        x = mycol.insert_one(mydict)

        api_root_info = db["api_root_information"]
        api_root_info.insert_one({
            "_url": "https://localhost:6100/example1/",
            "_name": "example1",
            "title": "example1",
            "description": "first API of LOUIS'S TAXII SERVER",
            "versions": "taxii-2.0",
            "max_content_length": "600",
        })

        # Creation collections DB :
        db = self.dbClient["example1"]
        file_directory = os.path.dirname(os.path.abspath(__file__))
        try:
            with open("{}/stixExample.json".format(file_directory)) as f:
                example = yaml.safe_load(f)
                print(example)
            # end with
        except Exception:
            print(traceback.format_exc())
            return None

        mycol = db["objects"]
        x = mycol.insert_one(example)

        mycol = db["status"]
        mydict = {
          "_id": ObjectId("647f1c0a2b8d3e4f5b8b4567"),
          "_queryable": 1,
          "id": "e3d65437-9630-4138-8851-ae94d8c9a8c1",
          "status": "success",
          "request_timestamp": "2023-06-02T08:43:24.500040+00:00",
          "total_count": 1,
          "success_count": 1,
          "failure_count": 0,
          "pending_count": 0,
          "timestamp": "2023-06-02T08:43:24.504530+00:00"
        }
        x = mycol.insert_one(mydict)

        mycol = db["collections"]
        mydict = {
            "id": "91a7b528-80eb-42ed-a74d-c6fbd5a26116",
            "title": "High Value Indicator Collection",
            "description": "This data collection is for collecting high value IOCs",
            "can_read": True,
            "can_write": False,
            "media_types": [
                "application/vnd.oasis.stix+json; version=2.0"
            ]
        }

        x = mycol.insert_one(mydict)
        mydict = {
            "id": "52892447-4d7e-4f70-b94d-d7f22742ff63",
            "title": "Indicators from the past 24-hours",
            "description": "This data collection is for collecting current IOCs",
            "can_read": True,
            "can_write": False,
            "media_types": [
                "application/vnd.oasis.stix+json; version=2.0"
            ]
        }
        x = mycol.insert_one(mydict)

        return db


if __name__ == '__main__':
    p = MongoHandler("mongodb://127.0.0.1:27017/", "mongo", "password")
    #p.drop_db_and_collection()
    db = p.build_db_and_collection()
    dblist = p.dbClient.list_database_names()
