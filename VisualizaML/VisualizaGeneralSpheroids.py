#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
OblGRAMA BÁSICO DE VISUALIZACIÓN DE UNA SERIE DE ELEMENTOS DE LA MATRIZ DE SCATTERING, 
A TODOS LOS POSIBLES ÁNGULOS        

Es un Oblgrama para Obleras, en la que se considerarán solo 4 elementos.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#1. Entrada ficheros/genera estructuras
f11=pd.read_csv('./F11_OblR1.csv')
f12=pd.read_csv('./F12_F11_OblR1.csv')
f22=pd.read_csv('./F22_F11_OblR1.csv')
f33=pd.read_csv('./F33_F11_OblR1.csv')
f34=pd.read_csv('./F34_F11_OblR1.csv')
f44=pd.read_csv('./F44_F11_OblR1.csv')


f11Im=f11['ImInd']
f12Im=f12['ImInd']
f33Im=f33['ImInd']
f34Im=f34['ImInd']


#normalizacion extra valores y generacion de matrices:
def normaf11(row):
    return np.log(row/row[30])


f11Mat=np.array(f11[f11.columns[1:-4]].apply(pd.to_numeric).apply(normaf11, axis=1))
f12Mat=np.array(f12[f12.columns[1:-4]].apply(pd.to_numeric))
f22Mat=np.array(f22[f22.columns[1:-4]].apply(pd.to_numeric))
f33Mat=np.array(f33[f33.columns[1:-4]].apply(pd.to_numeric))
f34Mat=np.array(f34[f34.columns[1:-4]].apply(pd.to_numeric))
f44Mat=np.array(f44[f44.columns[1:-4]].apply(pd.to_numeric))

##plots de todos

fig,ax = plt.subplots(nrows=2,ncols=2, sharex=False)
#carbon
fig.suptitle(' Oblates, all')
ax[0,0].set_xticks([])
ax[0,1].set_xticks([])

for i in range(len(f11['0deg'])):
   ax[0,0].plot(f11Mat[i,:])

ax[0,0].set_title('log(f11/f11(30deg))')

for i in range(len(f12['0deg'])):
   ax[0,1].plot(-f12Mat[i,:])

ax[0,1].set_title('-(f12/f11)')

#for i in range(len(f22['0deg'])):
#   ax[0,2].plot(f22Mat[i,:])

#ax[0,2].set_title('(f22/f11)')

for i in range(len(f33['0deg'])):
    ax[1,0].plot(f33Mat[i,:])

ax[1,0].set_title('f33/f11')

for i in range(len(f34['0deg'])):
   ax[1,1].plot(f34Mat[i,:])

ax[1,1].set_title('f34/f11')

#for i in range(len(f44['0deg'])):
#   ax[1,2].plot(f44Mat[i,:])

#ax[1,2].set_title('(f44/f11)')

fig.text(0.5, 0.04, 'Scattering angle (deg)', ha='center')

plt.savefig('AllOblateR1Def.pdf')
plt.close()
#plt.show()


##means plots

fig,ax = plt.subplots(nrows=2,ncols=2, sharex=False)
#carbon
fig.suptitle('Oblates, means')
ax[0,0].plot(np.mean(f11Mat, axis=0))
ax[0,0].set_title('(log(f11/f11(30dg)))')
ax[0,0].set_xticks([])
ax[0,1].plot(-np.mean(f12Mat, axis=0))
ax[0,1].set_title('(-(f12/f11))')
ax[0,1].set_xticks([])
ax[1,0].plot(np.mean(f33Mat, axis=0))
ax[1,0].set_title('((f33/f11))')
ax[1,1].plot(np.mean(f34Mat, axis=0))
ax[1,1].set_title('((f34/f11))')
plt.savefig("MeanOblateR1.pdf")
plt.close()
#plt.show()