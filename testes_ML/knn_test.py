import numpy 			 as np
import pandas 			 as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors 		 import KNeighborsClassifier
from sklearn.metrics 		 import confusion_matrix, classification_report

plt.style.use('ggplot')

#Carrega o dataset
df = pd.read_csv('datasets/rssi_final.csv')

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
X = df.drop('Lugar',axis=1).values #dados
y = df['Lugar'].values #resultados

print(X)
print(y)

#Definir conjunto de treinamento/testes:
#Treinamento  -> 40%,
#random_state -> semente para dividir os dados randomicamente
#stratify 	  -> separar por y (resultados)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.4,random_state=42, stratify=y)

'''
#Verificando precisao do K-NN para diferentes valores de K
neighbors = np.arange(1,50)
train_accuracy =np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

for i,k in enumerate(neighbors):
    #Configura o classificador com k vizinhos
    knn = KNeighborsClassifier(n_neighbors=k)
    
    #divide o modelo
    knn.fit(X_train, y_train)
    
    #Calcula a precisao dos dados de treinamento
    train_accuracy[i] = knn.score(X_train, y_train)
    
    #Calcula a precisao dos dados de teste
    test_accuracy[i] = knn.score(X_test, y_test)

plt.title('k-NN variando numero de vizinhos proximos')
plt.plot(neighbors, test_accuracy, label='Precisao no teste')
plt.plot(neighbors, train_accuracy, label='Precisao no treinamento')
plt.legend()
plt.xlabel('Numero de vizinhos proximos')
plt.ylabel('Precisao')
plt.show()

'''

#Configura o classificador K-NN com 3 vizinhos
knn = KNeighborsClassifier(n_neighbors=3)

#Ajusta os modelos
knn.fit(X_train,y_train)
print("Teste:")
print("Precisao: " + str(knn.score(X_test,y_test)))

#Predicao utilizando o classificador anteriormente ajustado
y_pred = knn.predict(X_test)
print("----------------------------")
print("Matriz de confusao")
# print(confusion_matrix(y_test,y_pred))

#A matriz de confusao tambem pode ser obtida atraves de:
print(pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))

print("----------------------------")
#Diagnostico de classificacao
print(classification_report(y_test,y_pred))