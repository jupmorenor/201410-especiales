'''
Created on 1/05/2014
@author: Juan Pablo Moreno - 20111020059
'''
from __future__ import print_function
import sys
if int(sys.version[0])==3:
    del print_function
del sys
    
from PIL import Image as img
from math import atan2, degrees, cos, sin
import pyfftw as pFT
import numpy as np
from scipy.misc import toimage
#import matplotlib.pyplot as plt

formatos = ['PNG', 'JPEG', 'GIF', 'BMP']

path = 'D:/Juanpa/Ingenieria de Sistemas UD/Semestre V/Matematicas especiales/transformadas+/'

def inversa():
    imagen1 = img.open(path+'gaussM2.png')
    imagen2 = img.open(path+'gaussF2.png')
    datos1 = imgALista(imagen1, imagen1.size)
    datos2 = imgALista(imagen2, imagen2.size)
    matrizTR = generarComplejosB(datos1, datos2)
    #print(imagen1.size)
    #print(datos2)
    #print(matrizTR)
    npArray = np.array(matrizTR)
    inv = pFT.builders.irfftn(npArray, npArray.shape)
    matrizRespPre = _arrayALista2D(inv(), imagen1.size)
    matrizRespDef = _lista2Da1D(matrizRespPre)
    print(matrizRespDef)
    imagenFinal = img.new('RGB', imagen1.size)
    imagenFinal.putdata(matrizRespDef)
    imagenFinal.save('C:/Users/Juanpa y Yami/Pictures/slantdiagOriginal.png')
    
    
    

def transformar():
    imagen = img.open(path+'gauss.png')
    if imagen.format in formatos:
        if imagen.format == 'PNG' or imagen.format == 'JPEG' \
        or imagen.format == 'BMP':
            matrizImagen = imgALista(imagen, imagen.size)
            print(matrizImagen) #imprime OK
            npArray = np.array(matrizImagen)
            #print("data size: " + str(npArray.size)) #dato correcto
            #print("data shape: " + str(npArray.shape)) #dato correcto
            #_print(npArray)
            transformar = pFT.builders.rfftn(npArray, npArray.shape)
            #print("tranf size: " + str(transformar().size)) #dato correcto
            #print("transf shape: " + str(transformar().shape)) #dato correcto
            salida1, salida2, salida3, salida4 = listaAImg(transformar(), imagen.size)
            salida1.save('C:/Users/Juanpa y Yami/Pictures/gaussM2.png')
            salida2.save('C:/Users/Juanpa y Yami/Pictures/gaussF2.png')
            salida3.save('C:/Users/Juanpa y Yami/Pictures/gaussR2.png')
            salida4.save('C:/Users/Juanpa y Yami/Pictures/gaussI2.png')
        elif imagen.format == 'GIF' or imagen.mode == 'P':
            matrizImagen = list(imagen.getdata())
            npArray = np.array(matrizImagen)
            transformar = pFT.builders.rfft(npArray)
            salida1, salida2, salida3, salida4 = separarComplejos1D(transformar())
            imagenMagnitud = img.new("L", imagen.size)
            imagenFase = img.new("L", imagen.size)
            imagenReal = img.new("L", imagen.size)
            imagenImag = img.new("L", imagen.size)
            imagenMagnitud.putdata(salida1)
            imagenFase.putdata(salida2)
            imagenReal.putdata(salida3)
            imagenImag.putdata(salida4)
            imagenMagnitud.save('C:/Users/Juanpa y Yami/Pictures/centerWaveM.gif')
            imagenFase.save('C:/Users/Juanpa y Yami/Pictures/centerWaveF.gif')
            imagenFase.save('C:/Users/Juanpa y Yami/Pictures/centerWaveF.gif')
        else:
            print("Formato no reconocido")
            
    
def separarComplejos1D(lista):
    magnitud = []
    fase = []
    ptReal = []
    ptImag = [] 
    for num in lista:
        magnitud.append(int(abs(num)))
        fase.append(int(degrees(atan2(num.imag,num.real))))
        ptReal.append(int(num.real))
        ptImag.append(int(num.imag))
    return magnitud, fase, ptReal, ptImag

def separarComplejos2D(arreglo):
    """
    A partir del arreglo de tuplas separa los valores reales de los imaginarios
    y genera una lista con cada uno
    """
    magnitud = []
    fase = []
    ptReal = []
    ptImag = [] 
    for fila in arreglo:
        for columna in fila:
            colMag = []
            colFase = []
            colReal = []
            colImag = []
            for num in columna:
                colMag.append(int(abs(num)))#magnitud del complejo
                colFase.append(int(degrees(atan2(num.imag,num.real))))#angulo fase
                colReal.append(int(num.real))#parte real
                colImag.append(int(num.imag))#parte imaginaria
            magnitud.append(tuple(colMag))
            fase.append(tuple(colFase))
            ptReal.append(tuple(colReal))
            ptImag.append(tuple(colImag))
    
    return magnitud, fase, ptReal, ptImag
    
def generarComplejosA(parteReal, parteImag):
    complejos = []
    for fila1, fila2 in zip(parteReal, parteImag):
        filaComplejos = []
        for col1, col2 in zip(fila1, fila2):
            colComplejos = []
            for num1, num2 in zip(col1, col2):
                colComplejos.append(complex(num1, num2))
            filaComplejos.append(colComplejos)
        complejos.append(filaComplejos)
    return complejos    

def generarComplejosB(magnitud, fase):
    complejos = []
    for fila1, fila2 in zip(magnitud, fase):
        filaComplejos = []
        for col1, col2 in zip(fila1, fila2):
            colComplejos = []
            for mag, fas in zip(col1, col2):
                num = complex(mag*cos(fas), mag*sin(fas))
                colComplejos.append(num)
            filaComplejos.append(tuple(colComplejos))
        complejos.append(filaComplejos)
    return complejos
                

def imgALista(imagen, tam):
    """
    Convierte el archivo de imagen de PIL en una lista de python de 2 dimensiones
    """
    datos = list(imagen.getdata())
    #print(datos)
    #Los datos se obtienen en una lista unidimensional
    l2D = _arrayALista2D(datos, tam)
    return l2D

def listaAImg(npArray, tam):
    """
    Genera una nueva imagen a partir de una lista
    """
    datos = _arrayALista2D(npArray, tam)
    #print(tam) #imprime OK
    magnitud, fase, ptReal, ptImag = separarComplejos2D(datos)
    #print(magnitud)
    #print("")
    #print(ptImag)
    imagenMagnitud = img.new("RGB", tam)
    imagenFase = img.new("RGB", tam)
    imagenReal = img.new("RGB", tam)
    imagenImg = img.new("RGB", tam)
    imagenMagnitud.putdata(magnitud)
    imagenFase.putdata(fase)
    imagenReal.putdata(ptReal)
    imagenImg.putdata(ptImag)
    return imagenMagnitud, imagenFase, imagenReal, imagenImg

def _arrayALista2D(arreglo, tam):
    l2D = []
    #print(type(arreglo[0]))
    if isinstance(arreglo, list):
        for i in range(tam[0]):
            fila = []
            for j in range(tam[1]):
                fila.append(tuple(arreglo.pop(0)))
            l2D.append(fila)
        #return l2D
    elif isinstance(arreglo, np.ndarray):
        for i in range(tam[0]):
            fila = []
            for j in range(tam[1]):
                fila.append(tuple(arreglo[i][j]))
            l2D.append(fila)
        #return l2D
    else:
        raise Exception("Datos en formato incorrecto")
    return l2D

def _lista2Da1D(lista):
    lista1D = []
    for fila in lista:
        for columna in fila:
            tupla = []
            for RGB in columna:
                tupla.append(int(RGB*255))
            lista1D.append(tuple(tupla))
    return lista1D
    
    
def _print(lista):
    for fila in lista:
        for columna in fila:
            print(columna, end='\t')
        print("")

if __name__ == '__main__':
    inversa()
