from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from subprocess import call
from IPython.display import Image
import pandas as pd

df = pd.read_csv('../datasets/cenario1/100_amostras/cen1_TESTE100.csv')

#Criando arrays separados para os dados e os resultados
X = df.drop('Setor',axis=1).values #dados
y = df['Setor'].values #resultados

# Model (can also use single decision tree)
model = RandomForestClassifier(n_estimators=10)

# Train
model.fit(X, y)
# Extract single tree
estimator = model.estimators_[5]

feature_names = ['GW1', 'GW2', 'GW3']
target_names  = ['c1_s1', 'c1_s2', 'c1_s3', 'c1_s4']
# Export as dot file
export_graphviz(estimator, out_file='tree.dot', 
                feature_names = feature_names,
                class_names = target_names,
                rounded = True, proportion = False, 
                precision = 2, filled = True)

# Convert to png using system command (requires Graphviz)
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

# Display in jupyter notebook
Image(filename = 'tree.png')