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
        response = self.app.get('/contacts/Troy', follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_creation(self):
        response = self.create_contact('Test', '122234')
        self.assertEqual(response.status_code, 200)

    def test_get_all_contacts(self):
        response = self.app.get('/contacts', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_pagination(self):
        response1 = self.app.get('/contacts?pageSize=3&page=1', follow_redirects=True)
        response2 = self.app.get('/contacts?pageSize=3&page=2', follow_redirects=True)
        assert (response1.status_code == 200) and (response2.status_code == 200)
    
    def test_queries(self):
        response1 = self.app.get('/contacts?pageSize=3&page=1&query=allison', follow_redirects=True)
        response2 = self.app.get('/contacts?pageSize=5&page=1&query=a*', follow_redirects=True)
        response3 = self.app.get('/contacts?pageSize=5&page=1&query=-allison', follow_redirects=True)
        response4 = self.app.get('/contacts?pageSize=5&page=1&query=allison+tony', follow_redirects=True)
        response5 = self.app.get('/contacts?pageSize=5&page=1&query=allison|tony', follow_redirects=True)
        assert (response1.status_code == 200) and (response2.status_code == 200) and (response3.status_code == 200) and (response4.status_code == 200) and (response5.status_code == 200)

    def test_get_contact_by_name(self):
        response = self.app.get('/contacts/Allison', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_contact(self):
        response = self.edit_contact('3300033')
        self.assertEqual(response.status_code, 200)
    
    def test_deletion(self):
        response = self.app.delete('/contacts/Test', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # helpers
    def create_contact(self, name, phone_number):
        #data = dict(name=name, phone_number=phone_number)
        data = json.loads("{\n\t\"name\": \"" + name + "\",\n\t\"phone_number\": \"" + phone_number + "\"\n}")
        return requests.post('http://localhost:5000/contacts', json=data)
        #return self.app.post('/contacts', data=data, follow_redirects=True)
    
    def edit_contact(self, phone_number):
        data = json.loads("{\n\t\"phone_number\": \"" + phone_number + "\"\n}")
        return requests.put('http://localhost:5000/contacts/Test', json=data)


if __name__ == '__main__':
    unittest.main()