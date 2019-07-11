import numpy 			 as np
import pandas 			 as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics 		 import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing 	 import StandardScaler
from sklearn.ensemble 		 import RandomForestClassifier
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
#Testes  -> 20%,
#random_state -> semente para dividir os dados randomicamente
#stratify 	  -> separar por y (resultados)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)


#Verificando precisao do Random Forest para diferentes quantidades de arvores
# trees = np.arange(1,70)
# train_accuracy =np.empty(len(trees))
# test_accuracy = np.empty(len(trees))

# for i,N in enumerate(trees):
#     #Configura o classificador com k vizinhos
# 	random_forest = RandomForestClassifier(n_estimators=N, random_state=0)  
    
#     #divide o modelo
# 	random_forest.fit(X_train, y_train)
    
#     #Calcula a precisao dos dados de treinamento
# 	train_accuracy[i] = random_forest.score(X_train, y_train)
    
#     #Calcula a precisao dos dados de teste
# 	test_accuracy[i] = random_forest.score(X_test, y_test)

# plt.title('Random Forest variando num de arvores para analise')
# plt.plot(trees, test_accuracy, label='Precisao no teste')
# plt.plot(trees, train_accuracy, label='Precisao no treinamento')
# plt.legend()
# plt.xlabel('Numero de arvores')
# plt.ylabel('Precisao')
# plt.show()



# n_estimators -> numero de arvores que serao criadas na analise
# random_state -> semente para dividir os dados randomicamente
random_forest = RandomForestClassifier(n_estimators=20, random_state=0)  

#Ajusta os modelos
random_forest.fit(X_train, y_train)  

y_pred = random_forest.predict(X_test)

print("Precisao: " + str(random_forest.score(X_test,y_test)))
print("Precisao: " + str(metrics.accuracy_score(y_test,y_pred)))

print("----------------------------")
print("Matriz de confusao")
# print(confusion_matrix(y_test,y_pred))

#A matriz de confusao tambem pode ser obtida atraves de:
print(pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))

print("----------------------------")

#Diagnostico de classificacao
print(classification_report(y_test,y_pred))