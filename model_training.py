# importing Libraries
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# creating a dummy dataset

data =[[98,0,0,0,0,'paracetmol'],[98,1,0,0,0,'paracetmol,coldmedicine'],[98,0,1,0,0,'paracetmol,tater'],[98,0,0,1,0,'dolo'],[98,0,0,0,1,'paracetmol,dolo'],[98,1,1,1,1,'paracetmol,dolo,tter']]
df = pd.DataFrame(data,columns=['fever','cold','cough','headache','bodypains',"medicine"])
data =[[99,0,0,0,0,'paracetmol'],[99,1,0,0,0,'paracetmol,coldmedicine'],[99,0,1,0,0,'paracetmol,tater'],[99,0,0,1,0,'dolo'],[99,0,0,0,1,'paracetmol,dolo'],[99,1,1,1,1,'paracetmol,dolo,tter']]
df1 = pd.DataFrame(data,columns=['fever','cold','cough','headache','bodypains',"medicine"])
df2=pd.merge(df,df1,how= 'outer')
df=df2

# feature extraction or future engineering
x =df[['fever','cold','cough','headache','bodypains']].values
y= df["medicine"].values
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# model selection
clf = DecisionTreeClassifier(max_leaf_nodes=3, random_state=0)
clf.fit(x_train, y_train)

# model Testing
y_pred = clf.predict(x_test)

joblib.dump(clf, "model.pkl", compress=('zlib', 3))