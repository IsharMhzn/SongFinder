import requests, time, json, base64, os

def get_bearer_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    secret_key = os.getenv("SPOTIFY_SECRET_KEY")

    b64encoded = base64.b64encode(f"{client_id}:{secret_key}".encode())

    token_data = {
        'grant_type' : "client_credentials"
    }

    headers = {
        'Authorization' : f'Basic {b64encoded.decode()}' #base64 encoded
    }

    r = requests.post('https://accounts.spotify.com/api/token', data=token_data, headers=headers)
    return r.json().get('access_token')


def authorize_account():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    
    query = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:5000/spotify/authorize',
        'scope': 'user-top-read user-read-recently-played',
        'show_dialog': True,
    }

    r = requests.get('https://accounts.spotify.com/authorize', params=query)
    return r.url

