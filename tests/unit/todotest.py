import unittest
import requests

Access_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzY4NDg2NzgsImlhdCI6MTY3NjM0ODY3OCwic3ViIjo0fQ.-xl6D4KCKM0GkE5pHh9xMLRAVO2vW09X78XFsZmeVqg'

class TestTodoFlaskApiUsingRequests(unittest.TestCase):
    def test_task_get(self):
        response = requests.get('http://localhost:5000/task/',\
                        headers = {'x-access-token':Access_token})
        self.assertEqual(response.status_code,200)

    def test_todo_create(self):
        response = requests.post('http://localhost:5000/task/addtask',
                    headers = {'x-access-token':Access_token},\
                        data={'Description':'A  testing Todo'})
        self.assertEqual(response.status_code,200) 

    def test_todo_delete(self):
        response = requests.delete('http://localhost:5000/task/deletetask/15',
                    headers = {'x-access-token':Access_token})
        self.assertEqual(response.status_code,200) 

    def test_todo_update(self):
        response = requests.put('http://localhost:5000/task/updatetask/11',
                    headers = {'x-access-token':Access_token},\
                        data={"Description":"Simple test task todo updated","Completed":True})
        self.assertEqual(response.status_code,200) 

if __name__ == "__main__":
    unittest.main()