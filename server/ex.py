coletas = [{'gw': 1, 'rssi': -72, 'setor': 'Telefone'}, {'gw': 2, 'rssi': -80, 'setor': 'Telefone'}, {'gw': 3, 'rssi': -45, 'setor': 'Telefone'}, {'gw': 1, 'rssi': -72, 'setor': 'Telefone'}, {'gw': 2, 'rssi': -82, 'setor': 'Telefone'}, {'gw': 3, 'rssi': -29, 'setor': 'Telefone'}, {'gw': 1, 'rssi': -79, 'setor': 'Telefone'}, {'gw': 2, 'rssi': -90, 'setor': 'Telefone'}, {'gw': 3, 'rssi': -39, 'setor': 'Telefone'}]
c = coletas

print("COLETAS: \n" + str(coletas))

rssi_list = []
s_list = []

while(len(c) > 0):
	x = c.pop()
	rssi_list.insert(0, x['rssi'])
	s_list.insert(0, x['setor'])

print("RSSI_LIST: \n" + str(rssi_list))
print("S_LIST: \n" + str(s_list))

res = {}

res['GW1'] = rssi_list[0::3]
res['GW2'] = rssi_list[1::3]
res['GW3'] = rssi_list[2::3]
res['Setor'] = s_list[0::3]

print("--------------------")
print("RESULTADO: \n" + str(res))

o = {}
a = {}
out = []
print("--------------------")
i = 0
while i < len(res['GW1']):
	o['GW1'] = res['GW1'][i]
	o['GW2'] = res['GW2'][i]
	o['GW3'] = res['GW3'][i]
	#na Medicao ja garante que vai ser o mesmo pra todos nesse intervalo de tempo
	o['Setor'] = res['Setor'][i]
	print(o)
	out.insert(0, o.copy())
	i += 1
print("---------------------------_")
print("SAIDA FINAL: \n" + str(out))