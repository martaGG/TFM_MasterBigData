#! /usr/bin/env python
# -*- coding: utf-8 -*-

#tienen cabeceros distintos
#pero siempre grados ---> 0
# intensidad  ----->1
#polarizacion  -----> 3

from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
#ref. ind montmorillonita: 1.52+0.0001 (488 nm, no hay de 600)
Mont=np.genfromtxt("../Ficheros/Montmorillonita.txt", skip_header=6)
print("Montmorillonita")
print("grados",Mont[:,0])
polar=np.concatenate((np.array([0,0]).reshape(1,2),Mont[:,[0,3]],np.array([180,0]).reshape(1,2)))

eje=np.arange(181)
intMont=interpolate.interp1d(polar[:,0], polar[:,1], kind='slinear', fill_value='extrapolate')
rellenoMont=intMont(eje)
#plt.plot(eje, rellenoMont)
#plt.plot(polar[:,0], polar[:,1], 'o')
#plt.show()
#estimación -i0.1-0.01
Hemat=np.genfromtxt("../Ficheros/Hematita.txt", skip_header=12)
print("Hematita")
print("grados",Hemat[:,0])
polar=np.concatenate((np.array([0,0]).reshape(1,2),Hemat[:,[0,3]],np.array([180,0]).reshape(1,2)))


eje=np.arange(181)
intHemat=interpolate.interp1d(polar[:,0], polar[:,1], kind='slinear', fill_value='extrapolate')
rellenoHem=intHemat(eje)
#plt.plot(eje, rellenoHem)
#plt.plot(polar[:,0], polar[:,1], 'o')
#plt.show()
#Ref. index Basalto: 1.52+0.001 0.647micr
Basal=np.genfromtxt("../Ficheros/Basalto.txt", skip_header=6)
print("Basalto")
print("grados",Basal[:,0])
polar=np.concatenate((np.array([0,0]).reshape(1,2),Basal[:,[0,3]],np.array([180,0]).reshape(1,2)))

eje=np.arange(181)
intBasal=interpolate.interp1d(polar[:,0], polar[:,1], kind='slinear', fill_value='extrapolate')
rellenoBas=intBasal(eje)
#plt.plot(eje, rellenoBas)
#plt.plot(polar[:,0], polar[:,1], 'o')
#plt.show()

import pandas as pd
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn import metrics as m
from sklearn.model_selection import  KFold, GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler

datAll=pd.read_csv('F12_F11_EsfR1.csv')
datAll2=pd.read_csv('F12_F11_OblR1.csv')
datAll3=pd.read_csv('F12_F11_ProR1.csv')
datos=pd.concat([datAll, datAll2, datAll3])
#separo en id, features q quiero, clase. Igual si tengo muchos es mejor hacerlo con 

dFeats=np.array(datos[datos.columns[1:-4]])
dIm=np.array(datos.ImInd)
dIm=np.log(dIm)

#entreno con todo usando el mejor para polarizacion
scal=StandardScaler()
scal.fit(dFeats)
#print("media_escalado",scal.mean_)
escalados=scal.transform(dFeats)

mod=MLPRegressor(hidden_layer_sizes=(49,49), alpha=0.001, solver='lbfgs')
mfit=mod.fit(escalados, dIm)
pred=mfit.predict(escalados)
mfit.score(escalados, dIm)
#plt.plot(pred, dIm, 'o')



smont=scal.transform(-rellenoMont.reshape(1,-1))
predMont=mfit.predict(smont)

shem=scal.transform(-rellenoHem.reshape(1,-1))
predhem=mfit.predict(shem)

sbas=scal.transform(-rellenoBas.reshape(1,-1))
predBas=mfit.predict(sbas)

plt.plot(predhem,  np.log(0.01),'o',label='hematita')
plt.plot(predBas,np.log(0.001), 'o',label='basalto')
plt.plot(predMont,np.log(0.0001), 'o',label='Montmorillonita')
plt.title("log(absorbancia)")
plt.xlabel('prediccion')
plt.ylabel('real')
plt.legend()
plt.savefig('IndiceRealPolarizacion.jpg')


dClass=datos['Shape']+datos['Compo']
modClas=MLPClassifier(hidden_layer_sizes=(28,), alpha=0.1, solver='lbfgs')
mClassFit=modClas.fit(escalados, dClass)
mClassFit.score(escalados, dClass)

print('montmorillonita',mClassFit.predict(smont))
print('hematita',mClassFit.predict(shem))
print('basalto',mClassFit.predict(sbas))