import numpy as np
import pandas as pd
from sklearn.model_selection import  KFold, GridSearchCV, train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

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

gridFit=pd.read_pickle('RegresionIndiceIntensidadCV.pkl')
scalTest=scal.transform(testFeats)
predTest =gridFit.predict(scalTest)
resid=testClass-predTest

plt.plot(testClass, predTest,'o')
plt.xlabel('respuesta real')
plt.ylabel('predicción')
plt.show()

plt.plot(testClass, resid,'o')
plt.xlabel('respuesta real')
plt.ylabel('residuo')
plt.show()

