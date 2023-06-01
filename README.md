##  Louis' Taxii Server implementation

 _Implementation of the taxii2.1 specification in order to well understand the whole thing and to have the simpliest implementation_

### Purpose :
Taxii/Stix is currently becoming, if it not the alreadu the case, the common way to share and collect CTI (Cyber Threat Intelligence) along with MISP (Malware information sharing plateform). I found the specification and the currents servers a bit complicated. So in order to understand the whole thing, I started this project, on my own time and on my profesionnal time at KOR Labs (https://korlabs.io/).

You'll find a well documented code, it might not be the best way to do all the thing, but the implementation is correct and it's working and feel free to add issues and ask for improvement. With always the "simplest as possible" mindset.

You'll find bellow a installation guide and a step by step to customize my code the way you want.

The goal here is that you can implement your own server based on mine. (Check-out the references at the end might be useful too)

#### Notes :
You'll find the API's basics request bellow in the section "API Paths and CURLs' request"

### Configuration :
Before doing one thing, you've to copy and paste the configs files. You'll find in the project two files, one about the API configuration and one about the Database configuration.

API Configuration, the file is api_config.yaml. You'll find within the file :
- BASE_URL : "http://localhost/"
    - It's the default url for the base API
- PORT : "6100"
    - The port where the API will listen to the calls
- USER : "api_log"
    - It's the API's user, you'll have to add it to your HTTP basics authentication (Cf. API's path bellow) 
- PASSWORD : "password"
    - It's your user's password
- SERVER_LIMIT: 20
    - It's the maximum number of object returned for one call.  


Database Configuration, the file is db_config.yaml. You'll find within the file :

- USER_DB : "mongo"
    - It's your user for the DB 
- PASSWORD_DB : "password"
    - It's your user's password for the DB 

### About Docker 
So, my server work with DOCKER, it is composed by two containers :

- MongoBD image
    - Storing objects, collections, root_api, etc...
- Ubuntu image
    - Handling API requests and connection to the back-end DB 

### Docker 
In order to use the Taxii server you'll have to have docker & docker-compose installed and ready to use.
If it's your first-time with docker (or if you re-install it) go check the documentation : https://docs.docker.com/get-docker/ .

Once you got a smooth install. You can go to the directory where docker-compose.yaml is located.
It should be on the root directory you've just downloaded from git (extract it of course).

Then you've to do theses commandes in the order :

```bash
    docker-compose build
```
You might be root if you didn't had your docker user to the sudoers. 

Then 
```bash
    docker-compose up -d
```
You should have this :
```bash
Starting taxiiserver_mongodb_1 ... done
Starting taxiiserver_ubuntu_1  ... done
```

The option -d is for "detach" that mean your container will run as a deamon. It's good in prod. If you want to have the output from the API/DB then forget about the -d. You'll have the output in you current terminal.
You can stop it by using "Ctrl + Z" and then kill it with "docker-compose down". Or kill it with "Ctlr + C", remenber that the last one is a Sigquit, strong interrupt, so it maybe be cleaner to use the first proposal.

When you start without the "-d" option, you should see the ubuntu launching the API.PY :
```bash
ubuntu_1   | mongodb://mongo:password@mongodb:27017/mydatabase
ubuntu_1   |  * Serving Flask src 'api'
ubuntu_1   |  * Debug mode: on
ubuntu_1   | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
ubuntu_1   |  * Running on all addresses (0.0.0.0)
ubuntu_1   |  * Running on http://127.0.0.1:6100
ubuntu_1   |  * Running on http://172.26.0.3:6100
ubuntu_1   | Press CTRL+C to quit
ubuntu_1   |  * Restarting with stat
```

When you kill it you should have this :

```bash
Stopping taxiiserver_ubuntu_1  ... done
Stopping taxiiserver_mongodb_1 ... done
Removing taxiiserver_ubuntu_1  ... done
Removing taxiiserver_mongodb_1 ... done
Removing network taxiiserver_default
```

Your flask server (this is not a production server) should listen on the port you've configured in the "api_config.yaml".

You can start calling it with your most loved requester. (Postman, curl etc).

#### DATABASE, Handling and understanding :

You've currently no data in the mongoDB. You can add somes and create examples of object, collections etc start the file called /database/init_database.py

It'll create the DB and all the collections you need :

- discovery_database :
    - discovery_information
        - It's the document/table you querry when you call the Taxii2
    - api_root_information
        - It's the document/table you querry when you can api_root (example1 here)
         
- API_ROOT_NAME (here example1)
    - Collections
        - It's all the collections you querry from get all collections or get specific collections 
    - Objects
        - It's all the object from all the collections (yes there are stored in the same place, the property within the object \_id\_collection will help retrieving the correct collection )
    - Status
        - It's the documents you got when you ADD an object into the Taxii Server    

To connect to the DB i personnaly use MongoDB (UI) Compass or mongosh (Shell) :
Connection string :
```bash
mongodb://mongo:password@localhost:27017/?authMechanism=DEFAULT
```


### API calls and structures of the methods :

There is a brief of the methods and their paths, i used postman, and the default port and host (change with your owns) :

#### Notes :

_The ID for Object & Collection are all UUID like this : "91a7b528-80eb-42ed-a74d-c6fbd5a26116 "_
_Info : https://fr.wikipedia.org/wiki/Universally_unique_identifier_

_"Example1" bellow is a root_api, you can list all root_api by calling the "Taxii2 request" (the first one bellow)._

#### GET :
- Information about the whole Taxii2
    - http://localhost:6100/taxii2
- Information about the API_ROOT
    - http://localhost:6100/example1
- All collections 
    - http://localhost:6100/example1/collections
-  A specific collection (by his ID)
    - http://localhost:6100/example1/collections/UUID-OF-COLLECTION
- All object from a specific collection :
    - http://localhost:6100/example1/collections/UUID-OF-COLLECTION/objects 
- A specific object from a specific collection 
    -  http://localhost:6100/example1/collections/UUID-OF-COLLECTION/objects/UUID-OF-OBJECT 
    -  You might add filter :  ?page=1&limit=1 directly to the end of the url  .../UUID-OF-COLLECTION/objects/UUID-OF-OBJECT?page=1&limit1
-  An object with a all his version :
    -  http://localhost:6100/example1/collections/UUID-OF-COLLECTION/objects/UUID-OF-OBJECT/versions/
    -  You can add the same filter than above
-  All manifest for a specific collection :
    -  http://localhost:6100/example1/collections/UUID-OF-COLLECTION/manifest/ 
- A status for the previous ADD Object call (see post section bellow)
    - http://localhost:6100/example1/status/UUID-OF-THE-POST-REQUEST
    
#### POST :
- Add an object to a specific collection :
    - http://localhost:6100/example1/collections/UUID-OF-COLLECTION/objects
    - The object is stored in the body of the post request (see bellow curls calls)
    - You can add multiple objects at once

You'll get in return a response with the status ID you can use in the get status request above.    

#### DELETE :
- Delete a specific object from a specific collection :
    - http://localhost:6100/example1/collections/UUID-OF-COLLECTION/objects/UUID-OF-OBJECT

#### Curls equivalent :
- Information about the whole Taxii2
```bash
curl --location 'http://localhost:6100/taxii2' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
- Information about the API_ROOT
```bash
curl --location 'http://localhost:6100/example1' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
- All collections 
```bash
curl --location 'http://localhost:6100/example1/collections' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
-  A specific collection (by his ID)
```bash
curl --location 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
- All object from a specific collection :
```bash
curl --location 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7-9ec7d755b4c3?page=1&limit=1' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
- A specific object from a specific collection 
```bash
curl --location 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7-9ec7d755b4c3/versions/?limit=1&page=1' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
-  An object with a all his version :
```bash
curl --location 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--601cee35-6b16-4e68-a3e7-9ec7d755b4c3/versions/?limit=1&page=1' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```


-  All manifest for a specific collection :
```bash
curl --location 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/manifest/' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
- A status for the previous ADD Object call (see post section bellow)
```bash
curl --location 'http://localhost:6100/example1/status/0f5cc140-6def-4ae7-bc41-7b4b940aa485' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
- Add an object to a specific collection :
```bash
curl --location 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects' \
--header 'Accept: application/taxii+json;version=2.1' \
--header 'Content-Type: application/taxii+json;version=2.1' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA==' \
--data '{   "objects":
[
    {
    "type": "bundle",
    "id": "bundle--0d8dfb44-b8d6-458a-9430-7336ace819ed",
    "collection_id" : "91a7b528-80eb-42ed-a74d-c6fbd5a26116",
    "objects": [
        {
            "type": "identity",
            "spec_version": "2.1",
            "id": "identity--15c02107-bd7a-479d-8c21-375e39f2ad63",
            "created": "2023-04-14T14:06:28.000Z",
            "modified": "2023-04-14T14:06:28.000Z",
            "name": "KOR Labs",
            "identity_class": "organization"
        }
    ]
}
]
}'
```
- Delete a specific object from a specific collection :
```bash
curl --location --request DELETE 'http://localhost:6100/example1/collections/91a7b528-80eb-42ed-a74d-c6fbd5a26116/objects/bundle--0d8dfb44-b8d6-458a-9430-7336ace819ed' \
--header 'Authorization: Basic YXBpX2xvZzpwYXNzd29yZA=='
```
### Documentation

1. In order to re-generate the HTML document of the source code, first install pdoc3

```bash
pip3 install pdoc3
```

and then use theses commands :

```bash
pdoc --force --html data_handling.py -o .
```

then you will have data_handling.html, file in the same directory.
You can use an http server in python to see the doc :


```python3
cd "your/hmtl/file/path"
python3 -m http.server
```


### File structure
```
src
├──  database
     ├── Config
         └── db_config.yaml
     ├── data_handling.py
     ├── db_config.yaml
     ├── init_database.py
     └── stixExample.json   
├──  API   
     ├── Config
         └── api_config.yaml
     ├──  api.py
     └──  api_error.py
docker-compose.yaml
Dockerfile
requirements.txt

```

