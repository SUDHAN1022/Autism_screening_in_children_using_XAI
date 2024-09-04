# -*- coding: utf-8 -*-
"""Autism screening in children using XAI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e6-XcQDgio9NmcrpnD3jbQ9cvl_ci_Uk?usp=sharing

Import modules
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestRegressor

"""Model Helpliners"""

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV
from sklearn.model_selection import GridSearchCV , KFold , cross_val_score, ShuffleSplit, cross_validate

from sklearn.preprocessing import MinMaxScaler , StandardScaler, LabelEncoder

from sklearn.metrics import mean_squared_log_error,mean_squared_error, r2_score,mean_absolute_error 

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score, classification_report

"""Dataset loadding and basic EDA"""

asd = pd.read_csv("Toddler Autism dataset July 2018.csv")

asd.head()

asd.describe()

asd.columns

asd.drop(['Case_No', 'Who completed the test'], axis = 1, inplace = True)
asd.columns

asd.dtypes

corr = asd.corr()
plt.figure(figsize = (15,15))
sns.heatmap(data = corr, annot = True, square = True, cbar = True)

plt.figure(figsize = (16,8))
sns.countplot(x = 'Ethnicity', data = asd)

asd.drop('Qchat-10-Score', axis = 1, inplace = True)

asd.columns

le = LabelEncoder()
columns = ['Ethnicity', 'Family_mem_with_ASD', 'Class/ASD Traits ', 'Sex', 'Jaundice']
for col in columns:
    asd[col] = le.fit_transform(asd[col])
asd.dtypes
features=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'Age_Mons', 'Sex', 'Ethinicity', 'Jaundice', 'Family_mem_with_ASD', 'Class/ASD Traits']

X = asd.drop(['Class/ASD Traits '], axis = 1)
Y = asd['Class/ASD Traits ']
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size = 0.20, random_state = 7)

model=RandomForestRegressor()

model.fit(x_train, y_train)

pred = model.predict(x_test).astype(int)

print(accuracy_score(y_test, pred))

"""Expandable AI SHAP"""

!pip install shap

import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(x_train)

"""SHAP feature importance"""

shap.summary_plot(shap_values, x_train, plot_type="bar")

"""SHAP summary plot"""

shap.summary_plot(shap_values, x_train)

"""SHAP dependance plot"""

shap.dependence_plot(12, shap_values, x_train)

"""SHAP Decision plot"""

shap.decision_plot(explainer.expected_value[0], shap_values[0])

"""LIME Expandable AI"""

!pip install lime

import lime
from lime import lime_tabular

explainer = lime_tabular.LimeTabularExplainer(
    training_data=np.array(x_train),
    feature_names=x_train.columns,
    class_names=['0', '1'],
    mode='regression'
)

"""ASD positive"""

exp = explainer.explain_instance(
    data_row=x_test.iloc[27], 
    predict_fn=model.predict
)

exp.show_in_notebook(show_table=True)

"""ASD negative"""

exp = explainer.explain_instance(
    data_row=x_test.iloc[30], 
    predict_fn=model.predict
)

exp.show_in_notebook(show_table=True)
