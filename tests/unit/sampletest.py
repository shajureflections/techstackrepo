import unittest
import requests
import json
import sys, os

class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://localhost:5000/user/')
        self.assertEqual(response.json(), {'tester': 'tester'})

    def test_login_request(self):
        response = requests.post('http://localhost:5000/user/login',data={'Email Address': 'testuser2@test.com', 'Password': 'testu'})
        self.assertEqual(response.status_code,200)  
    
    def test_user(self):
        response = requests.get('http://localhost:5000/user/user_list',headers = {'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzcwMjI4MzAsImlhdCI6MTY3NjUyMjgzMCwic3ViIjozNH0.iYFivnjpb6m9jumsnGV277qmwe-zI0ZluIlucMOTJnI'})
        self.assertEqual(response.status_code,200)  

    def test_register(self):
        response = requests.post('http://localhost:5000/user/register',
        data={
        'Email Address': 'pytest1890@test.com',
        'Password': 'testu',
        'Username':"pytest1890",
        "Confirm Password":"testu"})
        self.assertEqual(response.status_code,200) 

    def test_update(self):
        response = requests.put('http://127.0.0.1:5000/user/updateuser',\
            headers = {'x-access-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzcwMjM3MzUsImlhdCI6MTY3NjUyMzczNSwic3ViIjozNn0.LoJJnL3C9lNaOU2xG4mVMiPu00m9HEis31v173_v2Fc'},\
                data={'Password': 'testu'})
        self.assertEqual(response.status_code,200) 
    
    def test_userdelete(self):
        response = requests.delete('http://localhost:5000/user/user_delete',\
            headers = {'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzcwMjM0MTUsImlhdCI6MTY3NjUyMzQxNSwic3ViIjozNX0.aWjsnu4olymg_JKr0dsZYx3nGJBdrMXBEHbvo3WnikE'})
        self.assertEqual(response.status_code,200) 


if __name__ == "__main__":
    unittest.main()
