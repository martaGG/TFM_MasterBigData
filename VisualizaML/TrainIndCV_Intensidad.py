#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
PROGRAMA BÁSICO QUE ENTRENA UNA RED NEURONAL DE TAMAÑO FIJO
Entrada: Fichero entrenamiento csv de la forma q crea el de genera_ficheros (i.e: 1a col=fname, medio medidas, ultima clase)
Salida (Por pantalla):
        Metricas
        Plots pesos        

"""

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn import metrics as m
from sklearn.model_selection import  KFold, GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pickle


#1. Entrada ficheros/genera estructuras

datAll=pd.read_csv('F11_EsfR1.csv')
datAll2=pd.read_csv('F11_OblR1.csv')
datAll3=pd.read_csv('F11_ProR1.csv')
datos=pd.concat([datAll, datAll2, datAll3])
#separo en id, features q quiero, clase. Igual si tengo muchos es mejor hacerlo con 
def normaf11(row):
    return np.log(row/row[30])


datNorm=np.array(datos[datos.columns[1:-4]].apply(pd.to_numeric).apply(normaf11, axis=1))

dFeats=np.array(datNorm)
dIm=np.array(datos.ImInd)

#print(sum(dIm < 1.e-2))
##1, parte imaginaria
dClass=np.log(dIm)

trainFeats, testFeats, trainClass, testClass = train_test_split(dFeats, dClass, test_size=0.25, random_state=42)

scal=StandardScaler()
scal.fit(trainFeats)
#print("media_escalado",scal.mean_)
scalTrain=scal.transform(trainFeats)

lista=[]
l1=[(i,) for i in range(1,102,3)]
lista=lista+l1
l1=[(i,i) for i in range(1,102,3)]
lista=lista+l1

tuned_parameters = {'hidden_layer_sizes': lista,
                'alpha':[1.e-3,1.e-2, 1.e-1, 1.e0, 1.e1, 1.e2],
                'solver':['lbfgs']}
n_folds = 5
mlp=MLPRegressor()
#mlp=MLPRegressor(hidden_layer_sizes=(88,88), solver='lbfgs', alpha=0.001)
modelo = GridSearchCV(mlp,tuned_parameters, cv=n_folds, verbose=3)
gridFit = modelo.fit(scalTrain, trainClass)
print("Best Parameter", gridFit.best_params_)

pkl_filename = "RegresionIndiceIntensidadCV.pkl"  
with open(pkl_filename, 'wb') as file:  
    pickle.dump(gridFit, file)
predTrain=gridFit.predict(scalTrain)
plt.plot(predTrain, trainClass, 'o')
plt.show()
print("trn score", gridFit.score(predTrain, trainClass))
scalTest=scal.transform(testFeats)
predTest =gridFit.predict(scalTest)
plt.plot(predTest, testClass, 'o')
plt.show()
print("tsst score", gridFit.score(predTest, testClass))