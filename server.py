from flask import Flask, request
from flask_jsonpify import jsonify 
from flask_restful import Resource, Api
from json import dumps 
from elasticsearch import Elasticsearch 
import requests

port_number = 9200
es = Elasticsearch([{
    'host': 'localhost',
    'port': port_number
}])
app = Flask(__name__)
api = Api(app)
index = 'address_book'
doc_type = 'contact'
es.indices.create(index=index, ignore=400)

@app.route('/')
def test_service():
    response = requests.get('http://localhost:9200/')
    return response.content

class Contacts(Resource):
    def get(self):
        if 'pageSize' in request.args:
            page_size = int(request.args['pageSize'])
            if page_size < 1:
                return 'Error! Page size cannot be less than 1', 400
        else:
            page_size = 20
        
        if 'page' in request.args:
            page_number = int(request.args['page'])
            if page_number < 1:
                return 'Error! Page number cannot be less than 1', 400
        else:
            page_number = 1
        
        if 'query' in request.args:
            query_str = request.args['query']
            body = {
                'query': {
                    'query_string': {
                        'default_field': 'name',
                        'query': query_str
                    }
                }
            } 
        else:
            body = {
                'query': {
                    'match_all': {

                    }
                }
            }
        
        response = es.search(index=index, doc_type=doc_type, body=body)
        count = int(response['hits']['total'])
        docs = []
        for doc in response['hits']['hits']:
            docs.append(doc)

        if page_number > 1:
            if count > page_size * (page_number - 1):
                if count < page_size * page_number:
                    return jsonify(docs[page_size * (page_number - 1):count])
                return jsonify(docs[page_size * (page_number - 1):page_size * page_number])
            return 'Error! Page does not exist', 400
        else:
            if count > page_size:
                return jsonify(docs[0:page_size])
            return jsonify(docs[0:count])
    
    def post(self):
        if not request.get_json().get('name'):
            return 'Error! name is a required field', 400
        name = request.get_json().get('name')

        if not request.get_json().get('phone_number'):
            return 'Error! phone_number is a required field', 400
        phone_number = request.get_json().get('phone_number')
        
        if len(phone_number) > 15:
            return 'Error! phone_number cannot be longer than 15 digits', 400
        else:
            if not name.isalpha():
                return 'Error! name must contain only alphabets', 400
            search_body = {
                'query': {
                    'match': {
                        'name': name
                    }
                }
            }
            response = es.search(index=index, doc_type=doc_type, body=search_body)
            if response['hits']['total'] != 0:
                return 'Error! name already exists in records', 400
            index_body = {
                'name': name,
                'phone_number': phone_number
            }
            response = jsonify(es.index(index=index, refresh=True, doc_type=doc_type, body=index_body))
        return response

class FilterContacts(Resource):
    def retrieve_documents(self, name):
        body = {
            'query': {
                'match': {
                    'name': name
                }
            }
        }
        response = es.search(index=index, doc_type=doc_type, body=body)
        return response

    def get(self, name):
        docs = []
        response = self.retrieve_documents(name)
        if response['hits']['total'] == 0:
            return 'Error! No matching documents exist', 400
        
        for doc in response['hits']['hits']:
            docs.append(doc)
        
        return jsonify(docs)
    
    def put(self, name):
        docs = []
        user_ids = []
        response = self.retrieve_documents(name)

        if response['hits']['total'] == 0:
            return 'Error! No matching documents exist', 400
        for doc in response['hits']['hits']:
            user_ids.append(doc['_id'])
        
        phone_number = request.get_json().get('number')
        if not phone_number:
            return 'Error! number field is missing', 400
        
        body = {
            'doc': {
                'name': name,
                'phone_number': phone_number
            }
        }
        for user_id in user_ids:
            response = es.update(index=index, refresh=True, doc_type=doc_type, id=user_id, body=body)
            docs.append(response)
        
        return jsonify(docs)
    
    def delete(self, name):
        docs = []
        user_ids = []
        response = self.retrieve_documents(name)

        if response['hits']['total'] == 0:
            return 'Error! No matching documents exist', 400

        for doc in response['hits']['hits']:
            user_ids.append(doc['_id'])
            
        for user_id in user_ids:
            response = es.delete(index=index, refresh=True, doc_type=doc_type, id=user_id)
            docs.append(response)
        
        return jsonify(docs)

api.add_resource(Contacts, '/contacts')
api.add_resource(FilterContacts, '/contacts/<name>')

if __name__ == '__main__':
    app.run()
        
        
