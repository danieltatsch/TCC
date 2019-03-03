import requests

col = {}

col['nodo_mac'] = 'macNodo4'
# col['gateway_lugar'] = 'xablau'

url = 'http://localhost:5001/cadastra_nodo'
r = requests.post(url, json = col)

print(r)