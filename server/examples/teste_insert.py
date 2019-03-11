import requests

col = {}

col['gateway_mac'] = 'mac1'
col['nodo_mac'] = 'macNodo1'
col['rssi'] = -82

url = 'http://localhost:5001/insere_medicao'
# r = requests.post(url)
r = requests.post(url, json = col)

print(r)