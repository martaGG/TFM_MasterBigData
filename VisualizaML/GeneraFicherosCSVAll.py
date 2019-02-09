#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
script que genera 1 conjunto de datos tipo entrenamiento o test de categorías, que guardará en formato csv.

Usa los ficheros de 2 directorios: 
      dir1: Estos se asignaran a la categoria 1 (carbonaceos)

Genera ficheros csv: 
  
Con el nombre del fichero del q salen los datos, los valores de polarizacion / intensidad / otra F que elijamos medidos y la clase de la particula

Sin entrada y salida, yo modifico los paths a los dos directorios/nombres de la salida en el script
"""
import numpy as np
from os import listdir
from os.path import splitext, join
import csv
import sys

def line_num_for_F11_in_file(filename='file.txt'):
    with open(filename,'r') as f:
        for (i, line) in enumerate(f):
            if "F11" in line:
                return i
    return -1


dir1 =input("introduzca directorio\n")
tag=input("introduzca tag (empieza por Esf, Obl, o Pro)\n")
if(tag.startswith("Esf")):
   sfoot=0
   shap="Sphere"
   salidas=['F11_','F12_F11_','F13_F11_','F14_F11_','F21_F11_','F22_F11_', 'F23_F11_', 'F24_F11_', 'F31_F11_', 'F32_F11_', 'F33_F11_', 'F34_F11_', 'F41_F11_', 'F42_F11_', 'F43_F11_', 'F44_F11_' ]
   ir=0
elif(tag.startswith("Obl")):
   ir=1
   sfoot=1
   shap="Oblate"
   salidas=['F11_','F22_F11_','F33_F11_','F44_F11_','F12_F11_','F34_F11_']
elif(tag.startswith("Pro")):
   ir=1
   sfoot=1
   shap="Prolate"
   salidas=['F11_','F22_F11_','F33_F11_','F44_F11_','F12_F11_','F34_F11_']
else:
   print("wrong tag, should start with Esf, Obl, or Pro\n")
   sys.exit()


#"R1"#'./esferas/absorbentes90/'#'./esferas/absorbentes400/'
salidas = [txt+tag+".csv" for txt in salidas]

head=["filename"]
for i in range(181):
    head.append(str(i)+"deg")
    
head.append("ReInd")
head.append("ImInd")
head.append("Shape")
head.append("Compo")
l1= [fin for fin in listdir(dir1) if splitext(fin)[1]==".out"]
for indi,sali in enumerate(salidas):
  print(indi, sali)
  with open(sali, 'w') as f: 
     writer = csv.writer(f)
    #escribe cabecero
     writer.writerow(head)  
     #primero los carbonaceos
     for fnam in l1:
         #print(join(dir1,fnam))
         #los ficheros traen un cabecero de 5 lineas con otra info
         fn=join(dir1,fnam)
         shead=line_num_for_F11_in_file(fn)
        # print("shead", shead)
         dat=np.genfromtxt(fn, skip_header=shead+1, skip_footer=sfoot)
         
         d2=np.genfromtxt(fn[:-4]+".in")# 2 el re 3 el im
         #intensidad: f11: dat[:,1]; polariz: f14: dat[:,5]
         linea=[fn]
         fun=dat[:,indi+1]
         if(indi >0): fun=fun/dat[:,1]
         for i in range(len(fun)):
            linea.append(fun[i])
            
         linea.append(d2[ir+2])
         linea.append(d2[ir+3])
         linea.append(shap)
         compo="Carbon"
         if(d2[ir+3] <= 9e-3):
            compo="Silic"
         linea.append(compo)
         writer.writerow(linea)          

         
        
         

