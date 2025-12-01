import json
def test_api_register_login_and_create_thread(client):
    # register via api
    rv = client.post('/auth/api/register', json={'username':'apiuser','password':'pw'})
    assert rv.status_code == 201
    token = rv.get_json()['access_token']
    # create thread via api
    rv2 = client.post('/api/threads', json={'title':'API Thread','body':'api body'}, headers={'Authorization': f'Bearer {token}'})
    assert rv2.status_code == 201
    data = rv2.get_json()
    assert data['title'] == 'API Thread'
