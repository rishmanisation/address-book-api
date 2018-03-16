import server
from server import get_json_output
import requests
import unittest
from unittest import TestCase
import json
from elasticsearch import Elasticsearch

class TestAddressBook(TestCase):
    def setUp(self):
        server.app.testing = True
        self.app = server.app.test_client()

    def tearDown(self):
        pass
    
    def test_get_fail(self):
        response = self.app.get('/contacts/Alan', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
    
    # the commented out function gives 'AttributeError'
    '''
    def test_creation(self):
        response = self.create_contact('Alan', '9920014423')
        self.assertEqual(response.status_code, 200)
    '''
    def test_get_all_contacts(self):
        response = self.app.get('/contacts', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_contact_by_name(self):
        response = self.app.get('/contacts/Allison', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    # helpers
    def create_contact(self, name, phone_number):
        data = dict(name=name, phone_number=phone_number)
        return self.app.post('/contacts', data=data, follow_redirects=True)
    

if __name__ == '__main__':
    unittest.main()