



def test_auth_test_route(client_fixture):
    resposne = client_fixture.get('/auth/test')
    assert resposne.status_code == 200

    assert resposne.json()['message'] == 'auth test route successful'





def test_auth_signup_route(client_fixture):
    resposne = client_fixture.post('/auth/signup', json={
        "username": "test1",
        "email": "test1@example.com",
        "password": "test123"
    })
    
    assert resposne.status_code == 201