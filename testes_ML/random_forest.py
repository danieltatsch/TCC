import numpy 			 as np
import pandas 			 as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics 		 import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing 	 import StandardScaler
from sklearn.ensemble 		 import RandomForestClassifier

plt.style.use('ggplot')

#Carrega o dataset
df = pd.read_csv('datasets/cancer.csv')

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
X = df.drop('diagnosis',axis=1).values #dados
y = df['diagnosis'].values #resultados

# print(X)
# print(y)

#Definir conjunto de treinamento/testes:
#Testes  -> 20%,
#random_state -> semente para dividir os dados randomicamente
#stratify 	  -> separar por y (resultados)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

#n_estimators -> numero de arvores que serao criadas na analise
#random_state -> semente para dividir os dados randomicamente
random_forest = RandomForestClassifier(n_estimators=20, random_state=0)  

#Ajusta os modelos
random_forest.fit(X_train, y_train)  

print("Precisao: " + str(random_forest.score(X_test,y_test)))

y_pred = random_forest.predict(X_test)

print("----------------------------")
print("Matriz de confusao")
# print(confusion_matrix(y_test,y_pred))

#A matriz de confusao tambem pode ser obtida atraves de:
print(pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))

print("----------------------------")

#Diagnostico de classificacao
print(classification_report(y_test,y_pred))