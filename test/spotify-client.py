import requests, time, json, base64

client_id = ""
secret_key = ""


b64encoded = base64.b64encode(f"{client_id}:{secret_key}".encode())

token_data = {
    'grant_type' : "client_credentials"
}

headers = {
    'Authorization' : f'Basic {b64encoded.decode()}' #base64 encoded
}
method = 'POST'

r = requests.post('https://accounts.spotify.com/api/token', data=token_data, headers=headers)
print(r.json())