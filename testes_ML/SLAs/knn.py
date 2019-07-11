import numpy 			 as np
import pandas 			 as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors 		 import KNeighborsClassifier
from sklearn.ensemble 		 import RandomForestClassifier
from sklearn.metrics 		 import confusion_matrix, classification_report
from sklearn 				 import metrics

plt.style.use('ggplot')

#Carrega o dataset
df = pd.read_csv('../datasets/cenario2/100_amostras/cen2_TESTE100.csv')

#Print das 5 primeiras linhas
print("----------------------------")
print("Amostra do dataset:")
print("----------------------------")
print(df.head())

#Formato do dataset
#Primeiras 3 colunas: features (dados)
#Ultima coluna: target (resultado)
print("----------------------------")
print("(linhas, colunas): " + str(df.shape))
print("----------------------------")

#Criando arrays separados para os dados e os resultados
X = df.drop('Setor',axis=1).values #dados
y = df['Setor'].values #resultados

# print(X)
# print(y)

#Definir conjunto de treinamento/testes:
#Testes  -> 40%,
#random_state -> semente para dividir os dados randomicamente
#stratify 	  -> separar por y (resultados)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, stratify=y)

neighbors_trees = 50
neighbors = np.arange(1,neighbors_trees)
trees 	  = np.arange(1,neighbors_trees)

neighbors_pred = np.empty(len(neighbors))
trees_pred     = np.empty(len(trees))

for i,k in enumerate(neighbors):
    #Configura o classificador com k vizinhos
	knn = KNeighborsClassifier(n_neighbors=k)
	random_forest = RandomForestClassifier(n_estimators=k)  

	#divide o modelo
	knn.fit(X_train, y_train)	
	random_forest.fit(X_train, y_train)

	#Calcula a precisao dos dados de teste
	neighbors_pred[i] = knn.score(X_test, y_test)
	trees_pred[i]     = random_forest.score(X_test, y_test)

plt.title('k-NN variando numero de vizinhos proximos')
plt.plot(neighbors, neighbors_pred, label='Precisao K-NN')
plt.plot(trees, trees_pred, label='Precisao Random Forest')
plt.legend(loc='lower right')
plt.xlabel('Numero de vizinhos proximos / Arvores de decisao')
plt.ylabel('Precisao')
plt.show()
# '''

#Configura o classificador K-NN com 3 vizinhos
# knn = KNeighborsClassifier(n_neighbors=3)

# #Ajusta os modelos
# knn.fit(X_train,y_train)

# #Predicao utilizando o classificador anteriormente ajustado
# y_pred = knn.predict(X_test)

# print("Precisao: " + str(knn.score(X_test,y_test)))
# print("Precisao: " + str(metrics.accuracy_score(y_test,y_pred)))

# print("----------------------------")
# print("Matriz de confusao")
# # print(confusion_matrix(y_test,y_pred))

# #A matriz de confusao tambem pode ser obtida atraves de:
# print(pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))

# print("----------------------------")
# #Diagnostico de classificacao
# print(classification_report(y_test,y_pred))
