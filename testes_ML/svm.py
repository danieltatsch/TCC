import numpy 			 as np
import pandas 			 as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics 		 import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing 	 import StandardScaler
from sklearn.svm 			 import SVC  
from sklearn 				 import metrics

plt.style.use('ggplot')

#Carrega o dataset
df = pd.read_csv('datasets/bill_authentication.csv')

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
X = df.drop('Class',axis=1).values #dados
y = df['Class'].values #resultados

# print(X)
# print(y)

#Definir conjunto de treinamento/testes:
#Testes  -> 20%,
#random_state -> semente para dividir os dados randomicamente
#stratify 	  -> separar por y (resultados)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

#Treino e ajuste dos modelos
svclassifier_linear = SVC(kernel='linear')
svclassifier_linear.fit(X_train, y_train)

svclassifier_gaussian = SVC(kernel='rbf') #gaussian
svclassifier_gaussian.fit(X_train, y_train)

svclassifier_sigmoid = SVC(kernel='sigmoid') #sigmoid
svclassifier_sigmoid.fit(X_train, y_train)  

svclassifier_poly = SVC(kernel='poly')  
svclassifier_poly.fit(X_train, y_train)

y_pred_linear	= svclassifier_linear.predict(X_test)
y_pred_gaussian = svclassifier_gaussian.predict(X_test)
y_pred_sigmoid  = svclassifier_sigmoid.predict(X_test)
y_pred_poly  = svclassifier_poly.predict(X_test)

print("Precisao (Linear): " + str(svclassifier_linear.score(X_test, y_pred_linear)))
print("Precisao (Linear): " + str(metrics.accuracy_score(y_test, y_pred_linear)))
print("----------------------------")

print("Precisao (gaussian): " + str(svclassifier_linear.score(X_test, y_pred_gaussian)))
print("Precisao (gaussian): " + str(metrics.accuracy_score(y_test, y_pred_gaussian)))
print("----------------------------")

print("Precisao (sigmoid): " + str(svclassifier_linear.score(X_test, y_pred_sigmoid)))
print("Precisao (sigmoid): " + str(metrics.accuracy_score(y_test, y_pred_sigmoid)))
print("----------------------------")

print("Precisao (poly): " + str(svclassifier_linear.score(X_test, y_pred_poly)))
print("Precisao (poly): " + str(metrics.accuracy_score(y_test, y_pred_poly)))
print("----------------------------")

'''
print("Matriz de confusao")
# print(confusion_matrix(y_test,y_pred))

#A matriz de confusao tambem pode ser obtida atraves de:
print(pd.crosstab(y_test, y_pred_linear, rownames=['True'], colnames=['Predicted'], margins=True))

print("----------------------------")

#Diagnostico de classificacao
print(classification_report(y_test,y_pred))
'''