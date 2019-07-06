## TFM: Perceptrones multicapa aplicados al problema inverso de scattering

Este repositorio contiene el software asociado al trabajo de máster presentado por Marta González para el Máster en Visual Analytics y Big Data de la UNIR.

Contiene todo el código necesario para aplicar la metodología propuesta en el trabajo.

# CARPETAS

# Generación muestras

Contiene scripts de generación de ficheros de condiciones iniciales y código fortran para generar partículas de polvo esféricas con Mie y esferoides con T-Matrix. Los códigos fortran de otros autores utilizados en el trabajo también se incluyen por reproducibilidad, y son los siguientes:

- Sphere

  - Rutina fortran de Daniel Guirado para generar una distribución de tamaños
  
  - bhmie.for, de Bohren & Hufmann
  
- nonSphere
  
  - tmatrix, tmd.lp.f, tmd.par.f, lpd.f  de Mishchenko,Travis & Mackowski
  
# Visualización
