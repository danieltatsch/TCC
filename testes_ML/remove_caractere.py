f = open("rssi_final3.csv","r") #saida
f2  = open("rssi_final.csv","a+") #entrada

fl =f.readlines()

for i in fl:
	i = i.replace("Monitoria", "2")
	f2.write(i)