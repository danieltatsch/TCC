# import requests

# col = {}

# col['gateway_mac'] = 'mac3'
# col['nodo_mac'] = 'macNodo1'
# col['rssi'] = -94
# col['count'] = 4

# url = 'http://localhost:5001/insere_medicao'
# # r = requests.post(url)
# r = requests.post(url, json = col)

# print(r)

import requests

col = {}

col['cenario_nome'] = 'Sala'
col['nodo_mac'] = 'macNodo1'
# col['rssi'] = -42

url = 'http://localhost:5001/gera_csv'
# r = requests.post(url)
r = requests.post(url, json = col)

print(r)

# import requests

# col = {}

# col['cenario_nome'] = 'Sala'
# col['setor_nome'] = 'mesa'
# # col['rssi'] = -42

# url = 'http://localhost:5001/inicio_cenario_medicao'
# # r = requests.post(url)
# r = requests.post(url, json = col)

# print(r)

# import requests

# url = 'http://localhost:5001/fim_cenario_medicao'
# r = requests.post(url)
# # r = requests.post(url, json = col)

# print(r)