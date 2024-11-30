from sqlalchemy import text


def test_main_app_test_route(client_fixture):
    response = client_fixture.get('/test')
    assert response.status_code == 200
    
    data = response.json()
    assert data['message'] == 'test successful'




def test_database_connection(session_fixture):
    statement = text("SELECT 'hello';")
    result = session_fixture.execute(statement)
    
    assert result.one()[0] == 'hello'