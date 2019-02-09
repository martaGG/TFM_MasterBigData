#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
genero ficheros de entrada para mie: nFil carbonaceos y nFil silicatos
"""

import numpy as np

nFil=900

#genero carbonaceos
for i in range(nFil):
    fName="SpCar"+str(i).zfill(3)
    im= np.random.random()+0.09
    fi=open(fName+".in","w")
    fi.write(fName+"\n")
    fi.write(str(0.6)+"\n") #wavelength
    fi.write(str(1.8)+"\n") #real
    fi.write(str(im)+"\n") #imaginary
    fi.write(str(91)+"\n") #nang (/2+1)  
    fi.close() 
    
for i in range(nFil):
    fName="SpSil"+str(i).zfill(3)
    im= np.random.random()*1.e-2+1.e-6#
    fi=open(fName+".in","w")
    fi.write(fName+"\n")
    fi.write(str(0.6)+"\n") #wavelength
    fi.write(str(1.5)+"\n") #real
    fi.write(str(im)+"\n") #imaginary
    fi.write(str(91)+"\n") #nang (/2+1)    
    fi.close()