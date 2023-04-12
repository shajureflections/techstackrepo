
Access_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzY4NDg2NzgsImlhdCI6MTY3NjM0ODY3OCwic3ViIjo0fQ.-xl6D4KCKM0GkE5pHh9xMLRAVO2vW09X78XFsZmeVqg'
def test_todo_get(app, client):
    res = client.get('/task/',\
        headers = {'x-access-token':Access_token})
    assert res.status_code == 200


def test_todo_post(app, client):
    res = client.post('/task/addtask',\
        headers = {'x-access-token':Access_token},data={"Description":"Simple test task todo fdxgchjkhgc"})
    assert res.status_code == 200


def test_todo_put(app, client):
    res = client.put('/task/updatetask/11',\
        headers = {'x-access-token':Access_token},\
            data={"Description":"Simple test task todo updated","Completed":True}
        )
    assert res.status_code == 200

def test_todo_delete(app, client):
    res = client.delete('/task/deletetask/10',\
        headers = {'x-access-token':Access_token})
    assert res.status_code == 200
        
