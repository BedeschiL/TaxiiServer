import datetime
import os
import traceback
import uuid

import yaml
from pymongo import MongoClient


class DataHandler:
    def __init__(self, url, username, password):
        print(url)
        self.config = self.read_config_file()
        self.server_limit = self.config.get("SERVER_LIMIT")
        self.client = MongoClient(url, username=username, password=password, authSource='admin',
                                  authMechanism='SCRAM-SHA-256')

    def api_root_exist(self, api_root):
        """
            This function check if the API root exist in the db. It returns false if the API root doesn't exist
            it'll return true if the APi root exist.

            **Input params**

            * api_root (string)(required): name of the API root targeted

            **Returns**

            * False (boolean) :  if the API root doesn't exist
            * True (boolean) :   if the APi root exist
        """
        db_list = self.client.list_database_names()
        if api_root in db_list:
            return True
        else:
            return False

    def taxii_col_exist(self, api_root, id_col):
        """
            This function check if the collection exist in the database. it'll return false is the collection doesn't
            exist or true if the collection it must be tested after API_ROOT exist

            I'll surely merge this function with the api_roost_exist one.

            **Input params**

            * api_root (string)(required): name of the API root targeted
            * id_col (string)(required): id of the collection, it's commonly an UUID

            **Returns**

            * False (boolean) :  if the API root doesn't exist
            * True (boolean) :   if the APi root exist
        """
        db = self.client[api_root]
        col = db["collections"]
        count = col.count_documents({"id": id_col})
        if count == 0:
            return False
        else:
            return True

    def get_database_names(self):
        """
            This function get a list of the database name. It'll be useful to test if a database exist or not.

            **Input params**

            **Returns**

            * x (list)(string) :  A list with whole databases names from mongoDB
        """
        x = self.client.list_database_names()
        return x

    def get_collections_names(self):
        """
            This function get a list of the collection name. It'll be useful to test if a collection exist or not.
            **Returns**

            * x (list)(string) :  A list with whole databases names from mongoDB
        """
        x = None
        db_names = self.get_database_names()
        for name in db_names:
            db = self.client[name]
            x = db.list_collection_names()

        return x

    def discovery(self):
        """
            This function is call by the API to return the information about the whole taxii server. It's the main
            function to learn about this server. It'll be called when you enter the path "/taxii2".

            Example :

                - title         : "Louis's Taxi Server"
                - description   : "First version of louis's taxii Server"
                - contact       :"louis.bedeschi@gmail.com"
                - default       : "default path of api (it's an url)"
                - api_roots     : ["https://localhost:6100/example1/", "https://localhost:6100/example2/"]

            Cf : Section 4.1 Discovery of the specification

            **Input params**

            **Returns**

            * x (CommandCursor)(MongoClient) :  A cursor containing one row.
        """
        db = self.client['discovery_database']
        col = db['discovery_information']
        pipeline = [
            {
                '$lookup': {
                    'from': 'api_root_information',
                    'localField': 'api_roots',
                    'foreignField': '_url',
                    'as': '_roots',
                },
            },
            {
                '$addFields': {
                    'api_roots': '$_roots._url',
                },
            },
            {
                '$project': {
                    '_roots': 0,
                    '_id': 0,
                }
            }
        ]
        x = col.aggregate(pipeline).next()
        return x

    def get_root_information(self, root_api: str):
        """
            This function is call by the API to get information about a specific root_api, a root API is simply a base
            url and correspond to a whole new database. In fact our API can be linked to multiple databases.
            In our example we only have one API_ROOT (example1) which is the base url for the whole docker
            But you can add everything you need.

            I'll try to implement a client side asap. If you read this and the client is still not made. You can
            Check my init_database.py and get inspiration from this to create and handle mongoDB databases and
            collections

            Take care of one thing : Taxii2 got a collection (in the Mongo universe) called "collection" it might be
            confusing. In fact there is a collection (a table in relational DB) called "collection".

            It contains :

            Cf : Section 4.2 of the specification

            **Input params**

            * root_api (string)(required) :  A name of the API root you want to get information about

            **Returns**

            * x (CommandCursor)(MongoClient) :  A cursor containing one row.
        """
        db = self.client['discovery_database']
        col = db['api_root_information']
        x = col.find_one({'_name': root_api}, {'_id': 0, '_url': 0, '_name': 0})

        return x

    def get_api_root_status_by_id(self, api_root, id_status: str):
        """
        This function get a status from a previous (POST) add object call. The call of add object will return an
        envelope with the current status_id, you can query it ONLY once to know the query status.

            Example :

                - _queryable        : 1,
                - failure_count     : 0,
                - id                : "c3453dbb-c1cd-4765-9d64-24bcb0a61035",
                - pending_count     : 0,
                - request_timestamp : "2023-05-10T09:16:08.755587+00:00",
                - status            : "success",
                - success_count     : 1,
                - timestamp         : "2023-05-10T09:16:08.757312+00:00",
                - total_count       : 1

            Cf : Section 4.3 of the specification

            **Input params**

            * api_root (string)(required) :   A name of the API root you want to get the status object from
            * id_status (string)(required) :  The id of the previous get by the ADD OBJECT API CALL you

            **Returns**

            * x (dict) :  Return a dict with values inside (see example)
        """
        db = self.client[api_root]
        col = db['status']
        x = col.find_one({'id': id_status}, {'_id': 0})
        if x is None:
            return ' Deleted'
        if x.get('_queryable') >= 2:
            col.delete_one({'id': id_status})
            return 'Deleted'
        else:
            count = x['_queryable']
            count += 1
            filter_update = {'id': id_status}
            new_values = {
                '$set': {'_queryable': count}
            }
            db['status'].update_one(filter_update, new_values)

        return x

    def get_api_root_collections(self, api_root: str):
        """
            This function get all collection from an API_ROOT and display it

            Example :

                - id            : "91a7b528-80eb-42ed-a74d-c6fbd5a26116"
                - title         : "High Value Indicator Collection"
                - description   : "This data collection is for collecting high value IOCs"
                - can_read      : true
                - can_write     : false
                - media_types   : ["application/vnd.oasis.stix+json; version=2.0"]

            Cf : Section 5.1 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collections from

            **Returns**

            * x (list)(dict) :  Return a list of dict containing all collections with their information
        """
        db = self.client[api_root]
        col = db['collections']
        x = col.find({}, {'_id': 0})
        collection = []
        for document in x:
            collection.append(document)
        x = collection

        return x

    def get_api_root_collection_by_id(self, api_root: str, id_col: str):
        """
            This function get a specific collection by the giving ID

            Example :

                - id            : "91a7b528-80eb-42ed-a74d-c6fbd5a26116"
                - title         : "High Value Indicator Collection"
                - description   : "This data collection is for collecting high value IOCs"
                - can_read      : true
                - can_write     : false
                - media_types   : ["application/vnd.oasis.stix+json; version=2.0"]

            Cf : Section 5.2 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from
            * id_col (string)(required) : The id of the specific collection you want to get information about

            **Returns**

            * x (dict) :  Return a dict containing the targeted collection information
        """
        db = self.client[api_root]
        col = db['collections']
        x = col.find_one({'id': id_col}, {'_id': 0})

        return x

    def get_api_root_collections_manifest(self, api_root: str, id_col: str, list_filter: dict) -> dict:
        """
            This function get all the manifest of a specific collection, a manifest is linked to ONE and ONLY ONE object

            Example :

                - media_type: "application/stix+json;version2.1",
                - version   : "2014-11-19T23:39:03.893Z",
                - id        : "bundle--2faceb47-5187-4710-8ba7-89b87720d213",
                - date_added: "2023-05-10T09:16:08.756725+00:00"

            Cf : Section 5.3 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from
            * id_col (string)(required) : The id of the specific collection you want to get information about
            * list_filter (string)(optional) : Filter that you can use to get a specific manifest or pagination for
            example

            **Returns**

            * x (dict) :  Return a dict containing the targeted manifest from a collection
        """
        spec_ver = list_filter.get("spec_version")
        version = list_filter.get("version")
        limit = self.limit_filter(list_filter)
        page = self.page_filter(list_filter)

        db = self.client[api_root]
        col = db['objects']
        x = None
        has_next_page = None
        if spec_ver is not None and version is not None:
            x = col.find({"_id_collection": id_col, "spec_version": spec_ver, "version": version},
                         {'_id': 0, '_manifest': 1}).skip(page * limit).limit(limit)
            has_next_page = col.count_documents(
                {"_id_collection": id_col, "spec_version": spec_ver, "version": version}) > (
                                    page + 1) * limit

        elif spec_ver is not None and version is None:
            x = col.find({"_id_collection": id_col, "spec_version": spec_ver},
                         {'_id': 0, '_manifest': 1}).skip(page * limit).limit(limit)
            has_next_page = col.count_documents(
                {"_id_collection": id_col, "spec_version": spec_ver}) > (
                                    page + 1) * limit
        elif version is not None and spec_ver is None:
            x = col.find({"_id_collection": id_col, "version": version},
                         {'_id': 0, '_manifest': 1}).skip(page * limit).limit(limit)
            has_next_page = col.count_documents(
                {"_id_collection": id_col, "version": version}) > (
                                    page + 1) * limit
        if spec_ver is None and version is None:
            x = col.find({}, {'_id': 0, '_manifest': 1}).skip(page * limit).limit(limit)
            has_next_page = col.count_documents({}) > (page + 1) * limit

        collection = []
        for document in x:
            collection.append(document)

        if has_next_page:
            x = self.create_envelope(True, None, collection)
        else:
            x = self.create_envelope(False, None, collection)
        return x

    def get_api_root_collections_objects(self, api_root: str, id_col: str, list_filter: dict) -> dict:
        """
            This function get all the object of a specific collection

            Cf : Section 5.4 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from *
            id_col (string)(required) : The id of the specific collection you want to get information about *
            list_filter (string)(optional) : Filter that you can use to get a specific object or pagination for example

            **Returns**

            * x (dict) :  Return a dict containing all object from a specific collection
        """
        limit = self.limit_filter(list_filter)
        page = self.page_filter(list_filter)

        spec_ver = list_filter.get("spec_version")
        version = list_filter.get("version")

        db = self.client[api_root]
        col = db['objects']
        has_next_page = 0
        x = None
        if spec_ver is not None and version is not None:
            x = col.find({'_collection_id': id_col, "spec_version": spec_ver, "_manifest.version": version},
                         {'_id': 0}).skip(page * limit).limit(limit)
            has_next_page = col.count_documents(
                {'_collection_id': id_col, "spec_version": spec_ver, "_manifest.version": version}) > (page + 1) * limit
        elif spec_ver is not None and version is None:
            x = col.find({'_collection_id': id_col, "spec_version": spec_ver}, {'_id': 0}).skip(page * limit).limit(
                limit)
            has_next_page = col.count_documents({'_collection_id': id_col, "spec_version": spec_ver}) > (
                    page + 1) * limit
        elif version is not None and spec_ver is None:
            x = col.find({'_collection_id': id_col, "_manifest.version": version}, {'_id': 0}).skip(page * limit).limit(
                limit)
            has_next_page = col.count_documents({'_collection_id': id_col, "_manifest.version": version}) > (
                    page + 1) * limit
        if spec_ver is None and version is None:
            x = col.find({'_collection_id': id_col}, {'_id': 0}).skip(page * limit).limit(limit)
            has_next_page = col.count_documents({'_collection_id': id_col}) > (page + 1) * limit

        collection = []
        for document in x:
            collection.append(document)
        x = collection
        if has_next_page:
            x = self.create_envelope(True, None, x)
        else:
            x = self.create_envelope(False, None, x)

        return x

    def add_api_root_collections_object(self, api_root: str, id_col: str, obj: dict) -> dict or None:
        """
            This function put a new the object to a specific collection

            Cf : Section 5.5 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from
            * id_col (string)(required) : The id of the specific collection you want to get information about
            * obj (string)(required) : The object a dict string. You get that from Body of the http request

            **Returns**

            * x (dict) :  Return a dict containing the status of the query (envelope)
        """
        length = len(obj['objects'])
        if length > 0:
            db = self.client[api_root]
            status = self.generate_status('pending',
                                          self.get_date(),
                                          None, None, None)
            status_id = status['id']
            db['status'].insert_one(status)
            col = self.get_api_root_collections(api_root)
            exist = False
            for x in col:
                if x['id'] == id_col:
                    exist = True

            if exist:
                cpt = 0
                for x in obj['objects']:
                    self.add_object_manifest(obj['objects'], cpt)
                    obj['objects'][cpt]['_collection_id'] = id_col
                    spec_version = obj['objects'][cpt].get("spec_version", None) or None
                    if spec_version is None:
                        obj['objects'][cpt]["spec_version"] = "2.1"
                    col = db['objects']
                    col.insert_one(x)
                    cpt += 1

                filter_update = {'id': status_id}
                new_values = {
                    '$set': {'status': 'success', 'success_count': length, 'total_count': length,
                             'timestamp': self.get_date()}
                }
                db['status'].update_one(filter_update, new_values)
                x = self.get_api_root_status_by_id(api_root, status_id)

                return x
            else:
                return None

    def get_api_root_collections_object_by_id(self, api_root: str, id_col: str, id_obj: str, list_filter: dict) -> dict:
        """
            Function to get a specific object by his id

            Cf : Section 5.6 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from
            * id_col (string)(required) : The id of the specific collection you want to get information about
            * id_obj (string)(required) : The id of the object you want to get
            * list_filter (string)(optional) : Filter that you can use to get a specific object or pagination for
             example

            **Returns**

            * x (dict) :  Return a dict containing the status of the query (envelope)
        """
        limit = self.limit_filter(list_filter)
        page = self.page_filter(list_filter)

        spec_ver = list_filter.get("spec_version")
        version = list_filter.get("version")
        db = self.client[api_root]
        col = db['objects']
        x = None
        if spec_ver is not None and version is not None:
            x = col.find(
                {'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver, "_manifest.version": version},
                {'_id': 0}).skip(page * limit).limit(limit)
        elif spec_ver is not None and version is None:
            x = col.find({'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver}, {'_id': 0}).skip(
                page * limit).limit(limit)
        elif version is not None and spec_ver is None:
            x = col.find({'_collection_id': id_col, 'id': id_obj, "_manifest.version": version}, {'_id': 0}).skip(
                page * limit).limit(limit)
        if spec_ver is None and version is None:
            print(page)
            x = col.find({'_collection_id': id_col, 'id': id_obj}, {'_id': 0}).skip(page * limit).limit(limit)

        collection = []
        for document in x:
            collection.append(document)
        x = collection

        has_next_page = col.count_documents({'_collection_id': id_col, 'id': id_obj}) > (page + 1) * limit
        if has_next_page:
            x = self.create_envelope(True, id_obj, x)
        else:
            x = self.create_envelope(False, None, x)

        return x

    def delete_api_root_collections_object_by_id(self, api_root, id_col, id_obj, list_filter):
        """
            Function to delete a specific object by his id

            Cf : Section 5.7 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from
            * id_col (string)(required) : The id of the specific collection you want to get information about
            * id_obj (string)(required) : The id of the object you want to delete
            * list_filter (string)(optional) : Filter that you can use to get a specific object or pagination for
            example

            **Returns**

            * x (dict) :  Return a dict containing the status of the query (envelope)
        """
        spec_ver = list_filter.get("spec_version")
        version = list_filter.get("version")
        db = self.client[api_root]
        col = db['objects']
        x = None
        if spec_ver is not None and version is not None:
            x = col.delete_one(
                {'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver, "_manifest.version": version})
        elif spec_ver is not None and version is None:
            x = col.delete_one({'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver})
        elif version is not None and spec_ver is None:
            x = col.delete_one({'_collection_id': id_col, 'id': id_obj, "_manifest.version": version})
        if spec_ver is None and version is None:
            x = col.delete_one({'_collection_id': id_col, 'id': id_obj})
        x = {'delete_count': x.deleted_count}

        return x

    def get_api_root_collections_object_by_id_versions(self, api_root, id_col, id_obj, list_filter):
        """
            Function to get all versions of an object

            Cf : Section 5.7 of the specification

            **Input params**

            * api_root (string)(required) : A name of the API root you want to get the collection object from
            * id_col (string)(required) : The id of the specific collection you want to get information about
            * id_obj (string)(required) : The id of the object you want to delete

            * list_filter (string)(optional) : Filter that you can use to get a specific object or pagination for
             example

            **Returns**

            * x (dict) :  Return a dict containing the status of the query (envelope)
        """
        spec_ver = list_filter.get("spec_version")
        limit = self.limit_filter(list_filter)
        page = self.page_filter(list_filter)
        db = self.client[api_root]
        col = db['objects']

        if spec_ver is not None:
            x = col.find({'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver},
                         {'_id': 0, '_manifest': {'version': 1}}).skip(
                page * limit).limit(limit)
            has_next_page = col.count_documents({'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver}) > (
                    page + 1) * limit
        else:
            x = col.find({'_collection_id': id_col, 'id': id_obj}, {'_id': 0, '_manifest': {'version': 1}}).skip(
                page * limit).limit(limit)
            has_next_page = col.count_documents({'_collection_id': id_col, 'id': id_obj, "spec_version": spec_ver}) > (
                    page + 1) * limit

        col = []
        for doc in x:
            col.append(doc)

        if has_next_page:
            x = self.create_envelope(True, id_obj, col)
        else:
            x = self.create_envelope(False, None, col)

        return x

    def add_object_manifest(self, stix_obj, cpt):
        """
            Custom function to add a manifest everytime you add an object into the Taxii server.

            Example :

                - "media_type": "application/stix+json;version2.1",
                - "version": "2014-11-19T23:39:03.893Z",
                - "id": "bundle--e31cae3a-4145-4d9a-ac0c-063ae65a5d22",
                - "date_added": "2023-05-10T09:15:56.008587+00:00"

            **Input params**

            * stix_obj (dict)(required) : the dict as top object, you'll find the targeted object within
            this list object.
            * cpt (string)(required) : The current position (call in a loop) of the object

            **Returns**

        """
        _manifest = dict()
        print(stix_obj)
        media_type = stix_obj[cpt]['objects'][0].get('spec_version', None) or None
        _type = stix_obj[cpt]['type']
        version = stix_obj[cpt]['objects'][0].get('created', None) or None

        if media_type is not None:
            _manifest['media_type'] = 'application/stix+json;version' + media_type
        else:
            _manifest['media_type'] = None
        if version is None:
            dt = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            _manifest['version'] = dt.isoformat()
        else:
            _manifest['version'] = version

        _manifest['id'] = _type + '--' + self.generate_uuid()
        _manifest['date_added'] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        stix_obj[cpt]['_manifest'] = _manifest

    def generate_uuid(self):
        """
            Generate uuid4 and return it

            **Returns**

            * uuid : A string (64 char long) representing and Universal unique identifier
        """
        return str(uuid.uuid4())

    def get_date(self):
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    def read_config_file(self):
        file_directory = os.path.dirname(os.path.abspath(__file__))
        try:
            with open('{}/db_config.yaml'.format(file_directory)) as f:
                config = yaml.safe_load(f)
                return config
            # end with
        except Exception:
            print(traceback.format_exc())
            return None

    def generate_status(self, status, request_timestamp, successes, failures, pending):
        """
            Custom function to generate the status of an added object, remember that you can query this once.

            **Input params**

            * stix_obj (dict)(required) : the dict as top object, you'll find the targeted object within
            this list object.
            * cpt (string)(required) : The current position (call in a loop) of the object

            **Returns**

        """
        if successes is not None:
            success_count = len(successes)
        else:
            success_count = 0

        if failures is not None:
            failure_count = len(failures)
        else:
            failure_count = 0

        if pending is not None:
            pending_count = len(pending)
        else:
            pending_count = 0

        total_count = success_count + failure_count + pending_count
        status = {
            '_queryable': 0,
            'id': str(uuid.uuid4()),
            'status': status,
            'request_timestamp': request_timestamp,
            'total_count': total_count,
            'success_count': success_count,
            'failure_count': failure_count,
            'pending_count': pending_count,
        }
        return status

    def create_envelope(self, more, next_id, obj):
        """
            Function to create the envelope that is used as a wrapper for all the multiple object queries.

            **Input params**

            * obj (dict)(required) : the object that you want to wrap into the envelope * next_id (string)(required)
            : the next id of the object in case of querying a pagination stuff. (Not used at this time, but I plan to
            implement it ASAP)

            **Returns**

            * envelope (dict) : it returns the wrapper with the object inside.

        """
        if more is False:
            next_param = None
        else:
            next_param = next_id
        envelope = {
            "more": more,
            "next": next_param,
            "objects": [obj]
        }
        return envelope

    def limit_filter(self, list_filter):
        limit = list_filter.get("limit")
        if limit is not None:
            limit = int(limit)
        if limit is None:
            limit = self.server_limit
        return limit

    def page_filter(self, list_filter):
        page = list_filter.get("page")
        if page is not None:
            page = int(page)
            page += -1
        else:
            page = 0
        return page


if __name__ == '__main__':
    p = DataHandler('mongodb://127.0.0.1:27017/', 'mongo', 'password')
    # p.get_collections_names() x = p.discovery() print(x) x = p.get_root_information('taxii2') x =
    # p.get_api_root_collections('taxii2') print(x) p.get_api_root_collection_by_id('taxii2',
    # '91a7b528-80eb-42ed-a74d-c6fbd5a26116') x = p.get_api_root_collections_objects('example1',
    # '91a7b528-80eb-42ed-a74d-c6fbd5a26116', {}) x = p.get_api_root_collections_object_by_id('example1',
    # '91a7b528-80eb-42ed-a74d-c6fbd5a26116','bundle--601cee35-6b16-4e68-a3e7-9ec7d755b4c3',{"limit": 1, "page": 1,
    # "spec_version": 2.1, "version": "2023-04-14T14:06:28.000Z"}) p.get_api_root_collections_manifest('taxii2',
    # '91a7b528-80eb-42ed-a74d-c6fbd5a26116', ) p.add_api_root_collections_object('example1',
    # '91a7b528-80eb-42ed-a74d-c6fbd5a26116', 'post') x = p.delete_api_root_collections_object_by_id('example1',
    # '91a7b528-80eb-42ed-a74d-c6fbd5a26116', 'bundle--0d8dfb44-b8d6-458a-9430-7336ace819ed',{"spec_version": "2.1",
    # "version": "2023-04-14T14:06:28.000Z"}) print(x) 'bundle--0d8dfb44-b8d6-458a-9430-7336ace819ed') print(x) x=
    # p.get_api_root_collections_object_by_id_versions( 'taxii2', '91a7b528-80eb-42ed-a74d-c6fbd5a26116',
    # 'bundle--0d8dfb44-b8d6-458a-9430-7336ace819ed') print(x)
