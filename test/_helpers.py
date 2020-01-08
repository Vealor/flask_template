
def seed_db_data(db):
    # pull in each of jsons from seed folder and run scripts to import stuff
    print('SEEDING')
    pass

#===============================================================================
def login(client, username, password):
    payload = {
        'username': username,
        'password': password
    }
    headers = {
        'Accept': 'application/json'
    }
    response = client.post('/auth/login',
        json = payload,
        headers = headers,
        follow_redirects = True
    )
    return (response.get_json())['access_token']

#===============================================================================
def get_req(url, client, token=None):
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }
    response = client.get(url,
        headers = headers,
        follow_redirects = True
    )
    return response
