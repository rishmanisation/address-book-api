# Address Book API

This is an API that provides basic address book functionality. It is written in Python powered by the Flask framework, and uses Elasticsearch as a data store.

### Contact
* Required fields: name, phone_number
* Not required: any other information goes. Checks are only enforced on 'name' and 'phone_number'.

**name**: The name of the person whose contact is to be stored. Names must be unique, and can only contain alphabets.

**phone_number**: The phone number of the person to be stored. They must be unique, and can only contain digits. They can also not be longer than 15 digits.

### Endpoints
* **GET** /contacts : Returns all the contacts stored.
* **GET** /contacts?pageSize={}&page={}&query={} : Paginates the results, and allows Elasticsearch queries to be performed on the results.
    * **Default values**
        * pageSize = 20 (This must be an integer > 0)
        * page = 1 (This must be an integer > 0)
        * query = 'match all' (This must be a [queryStringQuery](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html))
    * **Supported queries**
        * '+' : This means 'AND'. Example: 'a+b' will return documents that match 'a' and 'b'.
        * '|' : This means 'OR'. Example: 'a|b' will return documents matching 'a' or 'b'.
        * '-' : This means 'NOT'. Example: '-a' will return everything that doesn't match 'a'.
        * Wildcard character: Example: 'a*' returns everything that starts with a.
* **POST** /contacts : Allows user to create a contact by using a 'json' object containing the data to be entered.
* **GET** /contacts/name : Allows user to retrieve information of a contact using 'name' to select the contact.
* **PUT** /contacts/name : Allows user to edit information of a contact whose 'name' is used.
* **DELETE** /contacts/name : Allows user to delete information of a contact whose 'name' is used.


### Installation

The following packages are needed for proper installation:

1. Elasticsearch: Download the tarball [here](https://www.elastic.co/downloads/elasticsearch).
2. This API was developed using Python 3.6.4 and the latest version of Flask. Compatibility with earlier versions of Python 3.x and Flask, as well as Python 2.x is **NOT** guaranteed.
3. While not required, it is **highly recommended** to install packages in a virtual environment. To set one up, run the following in a terminal (if you don't want to, just run the last command, although once again, it is highly recommended to set up a virtual environment):

```
pip install virtualenv
virtualenv env (replace 'env' with what you want to call it)
source env/bin/activate
python -m pip install -r requirements.txt
```

### Execution

Follow the following steps in the exact order in which they are mentioned:

1. After setting up the virtual environment, unzip the tarball in the project directory.
```
tar -xvzf elasticsearch-6.2.2.tar
```

2. Launch elasticsearch.
```
./elasticsearch-6.2.2/bin/elasticsearch
```

3. Open up a new terminal, and start the server. If both python2 and python3 are installed, you may have to replace 'python' with 'python3', depending on how it has been set up.
```
python server.py
```

4. The API is now running. The end-points can be tested using a tool such as [Postman](https://www.getpostman.com/apps).

5. This API ships with a set of tests in server_tests.py. In order to run these, open up another terminal (while Elasticsearch and server.py are still running) and type (once again, change 'python' to 'python3' as necessary):

```
python server_tests.py
```
### Changelog

#### 03/15/2018 (v0.1)
1. Basic endpoints supported.

#### 03/14/2018
1. Initial commit.
2. End-points to view all contacts and add new contacts implemented.

### To-do list
* ~~Filtering by name.~~
* ~~Editing and deleting contacts.~~ 
* ~~Support for boolean operators (and maybe wildcard characters) in Elasticsearch queries.~~
* Unit tests.
* Separate logic from HTTP stuff.
* Create data model for contact.
* Documentation!


