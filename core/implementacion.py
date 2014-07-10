'''
Created on 3/06/2014
@author: Juan Pablo Moreno - 20111020059
@author:
@author:
@author:
'''
from __future__ import print_function
from PIL import Image
import numpy as np
import pyfftw as pFT

_formatos = ['PNG', 'JPEG', 'GIF', 'BMP']

def _abrirImagen(_ruta):
    
    imagenes = []
    if isinstance(_ruta, list):
        if len(_ruta) == 1:
            imagenes = Image.open(_ruta.pop())
        elif len(_ruta)>1:
            for img in _ruta:
                imagenes.append(Image.open(img))
        else:
            imagenes = None
    elif isinstance(_ruta, str):
        imagenes = Image.open(_ruta)
    return imagenes

def transformar(ruta):
    """
    Calcula la Transformada Discreta de Fourier de una imagen RGB o en escala de grises 
    y retorna en forma de imagenes la parte real, parte imaginaria, magnitud y angulo fase
    """
    imagen = _abrirImagen(ruta)
    if imagen.format in _formatos:
        if imagen.mode != 'L':
            imagen = imagen.convert('L')
            
        datos = list(imagen.getdata())
        datos = np.array(datos)/255.0# - 1.0
        datos.shape = imagen.size
        transf = pFT.builders.fft2(datos, datos.shape)
        resultado = transf()
        
        #magnitud
        magnitud = Image.new('L', imagen.size)
        datosMag = np.around(np.log2((np.absolute(resultado))))
        datosMag.shape = (datosMag.size)
        magnitud.putdata(list(datosMag))
        
        #angulo fase
        fase = Image.new('L', imagen.size)
        datosFase = np.around(np.rad2deg(np.arctan2(resultado.imag, resultado.real)))
        datosFase.shape = (datosFase.size)
        fase.putdata(list(datosFase))
        
        return magnitud, fase
    else:
        return None, None

def filtrar(ruta):
    imagen = _abrirImagen(ruta)
    if imagen.format in _formatos:
        if imagen.mode != 'L':
            pass
        else:
            pass
    else:
        return None

def _print(lista):
    for fila in lista:
        for columna in fila:
            print(columna, end='\t')
        print("")

if __name__ == '__main__':
    _ruta = ['D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\escalon.png']
    img = transformar()
    _ruta2='D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\'
    for i, num in zip(img, range(len(img))):
        i.save(_ruta2 + 'escalon_' + str(num) + '.png')
    
