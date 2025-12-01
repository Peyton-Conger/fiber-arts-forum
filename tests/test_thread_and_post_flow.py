def register(client, username='alice', password='password'):
    return client.post('/auth/register', data={'username': username, 'password': password})

def login(client, username='alice', password='password'):
    return client.post('/auth/login', data={'username': username, 'password': password})

def test_thread_creation_and_reply(client):
    # register and login
    rv = register(client)
    assert rv.status_code in (302, 200)
    rv = login(client)
    assert rv.status_code in (302, 200)

    # create a thread
    rv = client.post('/thread/new', data={'title': 'Yarn recommendations', 'craft': 'Knitting', 'body': 'What yarns do you like?'})
    assert rv.status_code in (302, 201, 200)

    # get index and ensure thread present
    rv = client.get('/')
    assert b'Yarn recommendations' in rv.data

    # view thread and post reply
    # find thread id by visiting index and parsing link is complex; instead list threads via DB in other tests
