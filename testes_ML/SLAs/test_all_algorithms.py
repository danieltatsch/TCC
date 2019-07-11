import numpy 			 as np
import pandas 			 as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.neighbors 		 import KNeighborsClassifier
from sklearn.ensemble 		 import RandomForestClassifier
from sklearn.svm 			 import SVC  
from sklearn.metrics 		 import confusion_matrix, classification_report
from sklearn 				 import metrics
from scipy 					 import stats

plt.style.use('ggplot')

#Carrega o dataset
df = pd.read_csv('../datasets/cenario3/cen3_semOutliers.csv')
# df = pd.read_csv('../datasets/cenario2/sem_outliers/cen2_semOutliers.csv')

#Print das 5 primeiras linhas
# print("----------------------------")
# print("Amostra do dataset:")
# print("----------------------------")
# print(df.head())

#Formato do dataset
# #Primeiras 3 colunas: features (dados)
# #Ultima coluna: target (resultado)
# print("----------------------------")
# print("(linhas, colunas): " + str(df.shape))
# print("----------------------------")

#Criando arrays separados para os dados e os resultados
X = df.drop('Setor',axis=1).values #dados
y = df['Setor'].values #resultados

# print(X)
# print(y)

#Definir conjunto de treinamento/testes:
#Testes  -> 40%,
#random_state -> semente para dividir os dados randomicamente
#stratify 	  -> separar por y (resultados)
neighbors_trees = 50
neighbors = np.arange(1,neighbors_trees)
trees 	  = np.arange(1,neighbors_trees)

svclassifier_linear = SVC(kernel='linear')
svclassifier_gaussiana = SVC(kernel='rbf')

test_accuracy_knn  			 = np.empty(len(neighbors))
test_accuracy_random_forest  = np.empty(len(trees))
test_accuracy_svm			 = np.empty(len(trees))

knn_precision_list  = []
rf_precision_list   = []
svm_precision_list  = []
svm_precision_list2 = []

k_variation 	= []
trees_variation = []

i = 0
while i < 100:
	X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, stratify=y)
	
	for j,k in enumerate(neighbors):
		knn = KNeighborsClassifier(n_neighbors=k)
		random_forest = RandomForestClassifier(n_estimators=k)  
	
		#divide o modelo
		knn.fit(X_train, y_train)	
		random_forest.fit(X_train, y_train)
	    	
    	# Calcula a precisao dos dados de teste
		test_accuracy_knn[j] 		   = knn.score(X_test, y_test)
		test_accuracy_random_forest[j] = random_forest.score(X_test, y_test)

	knn_precision_list.append(max(test_accuracy_knn))
	rf_precision_list.append(max(test_accuracy_random_forest))

	k_variation.append(np.argmax(test_accuracy_knn))
	trees_variation.append(np.argmax(test_accuracy_random_forest))
	
	svclassifier_gaussiana.fit(X_train, y_train)
	svm_precision_list2.append(svclassifier_gaussiana.score(X_test, y_test))
	svclassifier_linear.fit(X_train, y_train)
	svm_precision_list.append(svclassifier_linear.score(X_test, y_test))
	
	i += 1

# print(k_variation)
# print(trees_variation)

k_variation = np.array(k_variation)
media_knn 	= np.mean(k_variation)
std_knn 	= np.std(k_variation)

trees_variation = np.array(trees_variation)
media_rf 		= np.mean(trees_variation)
std_rf 			= np.std(trees_variation)

knn_precision_list = np.array(knn_precision_list)
rf_precision_list  = np.array(rf_precision_list)
svm_precision_list = np.array(svm_precision_list)
svm_precision_list2 = np.array(svm_precision_list2)


knn_media = np.mean(knn_precision_list)
rf_media  = np.mean(rf_precision_list)
svm_media = np.mean(svm_precision_list)
svm_media2 = np.mean(svm_precision_list2)

print("-------K-NN-------")
print("Media: " + str(knn_media))

print("-------Random Forest-------")
print("Media: " + str(rf_media))

print("-------SVM Linear-------")
print("Media: " + str(svm_media))
print("-------SVM Gaussiana-------")
print("Media: " + str(svm_media2))


print("-------Vizinhos-------")
print("Media: " + str(media_knn))
print("Min: " + str(media_knn - std_knn))
print("Max: " + str(media_knn + std_knn))
print("-------Arvores-------")
print("Media: " + str(media_rf))
print("Min: " + str(media_rf - std_rf))
print("Max: " + str(media_rf + std_rf))

print("numd e vizinhos mais repetido: " + str(stats.mode(k_variation)))
print("num de arvores mais repetido: " + str(stats.mode(trees_variation)))

# '''
#Verificando precisao do K-NN para diferentes valores de K


# train_accuracy = np.empty(len(neighbors))

    #Configura o classificador com k vizinhos

# plt.title('k-NN variando numero de vizinhos proximos')
# plt.plot(neighbors, test_accuracy_knn, label='Precisao K-NN')
# plt.plot(trees, test_accuracy_random_forest, label='Precisao Random Forest')
# plt.legend()
# plt.xlabel('Numero de vizinhos proximos / Arvores de decisao')
# plt.ylabel('Precisao')
# plt.show()

# '''

# #Configura o classificador K-NN com 3 vizinhos
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