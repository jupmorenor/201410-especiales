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

_ruta = []
_formatos = ['PNG', 'JPEG', 'GIF', 'BMP']

def _abrirImagen():
    
    imagenes = []
    if len(_ruta) == 1:
        imagenes = Image.open(_ruta.pop())
    elif len(_ruta)>1:
        for img in _ruta:
            imagenes.append(Image.open(img))
    else:
        imagenes = None
    return imagenes

def estabecerRuta(ruta):
    _ruta = ruta

def transformada():
    """
    Calcula la Transformada Discreta de Fourier de una imagen RGB o en escala de grises 
    y retorna en forma de imagenes la parte reeal, parte imaginaria, magnitud y angulo fase
    """
    imagen = _abrirImagen()
    if imagen.format in _formatos:
        if imagen.mode == 'RGB' or imagen.mode == 'RGBA':
            datos = np.asarray(imagen)/255.0
            transf = pFT.builders.fftn(datos, datos.shape)
            resultado = transf()
            ptReal = Image.fromarray(np.around(resultado.real), 'RGB')
            ptImag = Image.fromarray(np.around(resultado.imag), 'RGB')
            magnitud = Image.fromarray(np.around(np.absolute(resultado)), 'RGB')
            fase = Image.fromarray(np.around(np.rad2deg(np.arctan2(resultado.imag, resultado.real))), 'RGB')
            return ptReal, ptImag, magnitud, fase
    

def inversa():
    imagenes = _abrirImagen()
    for imagen in imagenes:
        pass

class NoImagenError(Exception):
    pass

def _print(lista):
    for fila in lista:
        for columna in fila:
            print(columna, end='\t')
        print("")

if __name__ == '__main__':
    _ruta = ["D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\XD.png"]
    print(transformada()) 
    
