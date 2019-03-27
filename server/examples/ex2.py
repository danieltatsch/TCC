import operator

# coletas = [(1, -63, 'mesa', 0), (3, -70, 'mesa', 0), (1, -43, 'mesa', 1), (2, -63, 'mesa', 1), (3, -91, 'mesa', 1), (1, -49, 'mesa', 2), (2, -59, 'mesa', 2), (3, -85, 'mesa', 2), (2, -47, 'mesa', 3), (3, -88, 'mesa', 3), (1, -33, 'mesa', 4), (2, -55, 'mesa', 4), (3, -94, 'mesa', 4)]
coletas = [(1, -43, 'mesa', 1), (3, -70, 'mesa', 0), (2, -63, 'mesa', 1), (3, -91, 'mesa', 1), (1, -63, 'mesa', 0), (1, -49, 'mesa', 2), (2, -59, 'mesa', 2), (3, -85, 'mesa', 2), (2, -47, 'mesa', 3), (3, -88, 'mesa', 3), (1, -33, 'mesa', 4), (2, -55, 'mesa', 4), (3, -94, 'mesa', 4) , (3, -94, 'mesa', 5), (3, -94, 'mesa', 5), (2, -88, 'telefone', 6), (1, -99, 'telefone', 6), (3, -77, 'telefone', 6), (3, -22, 'telefone', 7), (1, -33, 'telefone', 7), (2, -44, 'telefone', 7),]
# print("ANTES: " + str(coletas))
# coletas  = sorted(coletas)

x = coletas

a = []

# pega os valores dos contadores das coletas
for i in coletas:
	a.append(i[3])

# ordena e tira valores repetidos
b = sorted(set(a))
c = b.copy()

#verifica se todos os gws tem valor do contador e os exclui senao
i = 0
while i <= max(b):
	count = a.count(i)
	if count != 3:
		c.remove(i)
	i += 1

x = [elem for elem in coletas if elem[3] in c]

# print ("coletas: " + str(coletas))	
# print ("a = " + str(a))
# print ("b sorted(sort(a)) = " + str(b))
# print ("c = " + str(c))
# print ("FINAL coletas: " + str(x.sort(key=lambda l: l[3])))

l = [] 
# l = x.sort(key = operator.itemgetter(0))
l = sorted(x, key=lambda x: x[0])
print ("FINAL coletas: " + str(l))

d = {}

d['GW1'] = []
d['GW2'] = []
d['GW3'] = []
d['Setor'] = []

for i in l:
	if i[0] == 1:
		d['GW1'].append(i[1])
	if i[0] == 2:
		d['GW2'].append(i[1])
	if i[0] == 3:
		d['GW3'].append(i[1])		
	d['Setor'].append(i[2])
print("D: " + str(d))

out = []
o = {}
i = 0
while i < len(d['GW1']):
	o['GW1'] = d['GW1'][i]
	o['GW2'] = d['GW2'][i]
	o['GW3'] = d['GW3'][i]
	o['Setor'] = d['Setor'][i]
	i += 1
	print(o)
	out.insert(0, o.copy())

# print("FINAL: " + str(out))
# i = 0
# while i < 10:
# 	if i in d['GW1'] and i in d['GW2'] and i in d['GW3']:
# 		print ("COUNTS IGUAIS: " + str(i))
# 	else:
# 		print ("NADA IGUAL EM i = " + str(i))
# 	i += 1