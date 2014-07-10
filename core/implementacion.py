'''
Created on 3/06/2014
@author: Juan Pablo Moreno - 20111020059
@author:
@author:
@author:
'''
from __future__ import print_function
import os
from PIL import Image
import numpy as np
import pyfftw as pFT

_FORMATOS = ['PNG', 'JPEG', 'GIF', 'BMP']
_FILTROS = ['Gaussian filter.png', 'High pass filter.png', 'Low pass filter.png',
            'pyramidal filter.png', 'Sinc filter.png']

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
    if imagen.format in _FORMATOS:
        if imagen.mode != 'L':
            imagen = imagen.convert('L')
            
        datos = list(imagen.getdata())
        datos = np.array(datos)#/255.0# - 1.0
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
        datosFase = np.around(np.rad2deg(np.arctan(resultado.imag, resultado.real)))
        datosFase.shape = (datosFase.size)
        fase.putdata(list(datosFase))
        
        return magnitud, fase
    else:
        return None, None

def filtrar(rutaimg, filtro):
    imagen = _abrirImagen(rutaimg)
    filtro = _abrirImagen(os.path.join(os.path.dirname(os.path.dirname(__file__)),"filtros\\" + filtro + ".png"))
    filtro = filtro.resize(imagen.size)
    if imagen.format in _FORMATOS:
        if imagen.mode != 'L':
            imagen = imagen.convert('L')
            filtro = filtro.convert('L')
        
        datos = list(imagen.getdata())
        datos = np.array(datos)
        datos.shape = imagen.size
        transf = pFT.builders.fft2(datos, datos.shape)
        resultado = transf()
        
        datosFiltro = list(filtro.getdata())
        datosFiltro = np.array(datosFiltro)/255.0
        datosFiltro.shape = filtro.size
        
        magnitud = np.around(np.absolute(resultado))
        magnitud -= np.min(magnitud)
        magnitud *= datosFiltro
        
        fase = np.around(np.rad2deg(np.arctan2(resultado.imag, resultado.real)))
        resultado = magnitud*(np.cos(np.deg2rad(fase)) + np.sin(np.deg2rad(fase))*1j)
        inv = pFT.builders.ifft2(resultado, resultado.shape)
        inversa = inv()#/inv.N
        _print(inversa)
        inversa.shape = inversa.size
        imagen2 = Image.new("L", imagen.size)
        imagen2.putdata(list(inversa.real))
        return imagen2
    else:
        return None

def _print(lista):
    for fila in lista:
        for columna in fila:
            print(columna, end='\t')
        print("")

if __name__ == '__main__':
    
    filtrar("D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\XD.png", "High pass filter")
    """
    _ruta = ['D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\escalon.png']
    img = transformar()
    _ruta2='D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\'
    for i, num in zip(img, range(len(img))):
        i.save(_ruta2 + 'escalon_' + str(num) + '.png')
    """
