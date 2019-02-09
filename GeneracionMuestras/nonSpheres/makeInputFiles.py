#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
genero ficheros de entrada para mie: nFil carbonaceos y nFil silicatos
"""

import numpy as np

nFil=900

#oblatos
#genero carbonaceos
for i in range(nFil):
    fName="ObCar"+str(i).zfill(3)
    im= np.random.random()*0.7+0.09#np.random.random()*0.1+0.6
    fi=open(fName+".in","w")
    fi.write(fName+"\n")
    fi.write(str(2)+"\n") #ratio  
    fi.write(str(0.6)+"\n") #wavelength
    fi.write(str(1.8)+"\n") #real
    fi.write(str(im)+"\n") #imaginary
    fi.close() 
    
for i in range(nFil):
    fName="ObSil"+str(i).zfill(3)
    im= np.random.random()*1.e-2+1.e-6#(1.e-3-1.e-6)+1.e-6
    fi=open(fName+".in","w")
    fi.write(fName+"\n")
    fi.write(str(2)+"\n") #ratio
    fi.write(str(0.6)+"\n") #wavelength
    fi.write(str(1.5)+"\n") #real
    fi.write(str(im)+"\n") #imaginary
    fi.close()
    
    #prolatos
    #genero carbonaceos
for i in range(nFil):
        fName="PrCar"+str(i).zfill(3)
        im=np.random.random()*0.7+0.09 #np.random.random()*0.1+0.6
        fi=open(fName+".in","w")
        fi.write(fName+"\n")
        fi.write(str(0.5)+"\n") #ratio
        fi.write(str(0.6)+"\n") #wavelength
        fi.write(str(1.8)+"\n") #real
        fi.write(str(im)+"\n") #imaginary
        fi.close() 
    
for i in range(nFil):
        fName="PrSil"+str(i).zfill(3)
        im= np.random.random()*1.e-2+1.e-6#(1.e-3-1.e-6)+1.e-6pen(fName+".in","w")
        fi=open(fName+".in","w")    
        fi.write(fName+"\n")
        fi.write(str(0.5)+"\n") #ratio
        fi.write(str(0.6)+"\n") #wavelength
        fi.write(str(1.5)+"\n") #real
        fi.write(str(im)+"\n") #imaginary
        fi.close()