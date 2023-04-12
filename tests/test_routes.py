
def test_default_get(app, client):
    res = client.get('/user/')
    assert res.status_code == 200

def test_user_get(app, client):
    res = client.get('/user/user_list',headers = {
        'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzcwMjE4OTMsImlhdCI6MTY3NjUyMTg5Mywic3ViIjozMn0.xJH48e6ADlEMOG6ARvfbdFCNoPYG27Xj1l2C0fARFco'})
    assert res.status_code == 200

def test_login_post(app, client):
    response = client.post(
        '/user/login', data={'Email Address': 'testuser2@test.com', 'Password': 'testu'}
    )
    assert response.status_code == 200

def test_register_post(app, client):
    res = client.post('/user/register',data={
        'Email Address': 'pytest1260@test.com',
        'Password': 'testu',
        'Username':"pytest1260",
        "Confirm Password":"testu"

    })
    assert res.status_code == 200

def test_updateuser_post(app, client):
    res = client.put('/user/updateuser',headers = {
        'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzcwMjE4OTMsImlhdCI6MTY3NjUyMTg5Mywic3ViIjozMn0.xJH48e6ADlEMOG6ARvfbdFCNoPYG27Xj1l2C0fARFco'}\
            ,data={
        'Email Address': 'pytest120@test.com',
        'Password': 'testu',
        'Username':"pytest120",

    })
    assert res.status_code == 200

def test_deleteuser_post(app, client):
    res = client.delete('/user/user_delete',headers = {
        'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzcwMjIzNTcsImlhdCI6MTY3NjUyMjM1Nywic3ViIjozM30.sEVq2puBpT_8OYsFUcVcEBWMztcCn68b2jXuwee-mLI'})
    assert res.status_code == 200