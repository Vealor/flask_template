from seed._seed_data import do_seed

def seed_db_data():
    do_seed()

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
                           follow_redirects = True)
    return (response.get_json())['access_token']

#===============================================================================
def get_req(url, client, token=None):
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    response = client.get(url,
                          headers = headers,
                          follow_redirects = True)
    return response

def post_req(url, client, payload={}, token=None):
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    response = client.post(url,
                           json = payload,
                           headers = headers,
                           follow_redirects = True)
    return response

def put_req(url, client, payload={}, token=None):
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    response = client.put(url,
                          json = payload,
                          headers = headers,
                          follow_redirects = True)
    return response

def delete_req(url, client, token=None):
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    response = client.delete(url,
                             headers = headers,
                             follow_redirects = True)
    return response
