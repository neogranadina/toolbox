import requests
import json

def get_auth_token():
    url = 'http://172.22.139.213/ifrepo-admin/service/Auth'
    headers = {'Content-Type': 'application/json'}

    query = '''
    query {
        login(username: "administrator", password: "f8491d2d") {
            jwt,
            refresh,
            user {
                id,
                fname,
                lname,
                email
            }
        }
    }
    '''

    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code} and message {response.text}")

print(get_auth_token())