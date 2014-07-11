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

def _abrirImagen(_ruta):
    
    imagenes = []
    if isinstance(_ruta, list) or isinstance(_ruta, tuple):
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
    Calcula la Transformada Discreta de Fourier de una imagen en escala de grises 
    y retorna en forma de imagenes la magnitud y angulo fase
    """
    imagen = _abrirImagen(ruta)
    if imagen.format in _FORMATOS:
        if imagen.mode != 'L':
            imagen = imagen.convert('L')
            
        datos = np.array(list(imagen.getdata()))/255.0# - 1.0
        datos.shape = imagen.size
        transf = pFT.builders.fft2(datos, datos.shape)
        resultado = transf()
        
        #magnitud
        magnitud = Image.new('L', imagen.size)
        datosMag = np.around((np.absolute(resultado)))
        datosMag = _reordenar(datosMag)
        datosMag.shape = (datosMag.size)
        magnitud.putdata(list(datosMag))
        
        #angulo fase
        fase = Image.new('L', imagen.size)
        datosFase = np.rad2deg(np.arctan2(resultado.imag, resultado.real))
        datosFase-=np.min(datosFase)
        datosFase*=(255.0/np.max(datosFase))
        datosFase = _reordenar(np.around(datosFase))
        datosFase.shape = (datosFase.size)
        fase.putdata(list(datosFase))
        
        return magnitud, fase
    else:
        return None, None

def filtrar(rutaimg, filtro):
    """
    Obtiene la magnitud del espectro de frecuencia y lo opera con el :filtro: seleccionado
    """
    imagen = _abrirImagen(rutaimg)
    filtro = _abrirImagen(os.path.join(os.path.dirname(os.path.dirname(__file__)),"filtros\\" + filtro + ".png"))
    filtro = filtro.resize(imagen.size)
    if imagen.format in _FORMATOS:
        if imagen.mode != 'L' or filtro.mode!='L':
            imagen = imagen.convert('L')
            filtro = filtro.convert('L')
        
        datos = np.array(list(imagen.getdata()))
        datos.shape = imagen.size
        transf = pFT.builders.fft2(datos, datos.shape)
        resultado = transf()
        
        datosFiltro = np.array(list(filtro.getdata()))/255.0
        datosFiltro.shape = filtro.size
        
        magnitud = np.around(np.absolute(resultado))
        magnitud -= np.min(magnitud)
        magnitud = _reordenar(magnitud)
        magnitud *= datosFiltro
        
        fase = np.rad2deg(np.arctan2(resultado.imag, resultado.real))
        fase-=np.min(fase)
        fase*=(255.0/np.max(fase))
        fase = _reordenar(np.around(fase))
        resultado = magnitud*(np.cos(np.deg2rad(fase)) + np.sin(np.deg2rad(fase))*1j)
        inv = pFT.builders.ifft2(resultado, resultado.shape)
        inversa = inv()#/inv.N
        inversa.shape = inversa.size
        imagen2 = Image.new("L", imagen.size)
        imagen2.putdata(list(np.absolute(inversa)))
        return imagen2
    else:
        return None

def invertir(rutas):
    """
    calcula la transformada inversa a partir de las imagenes de magnitud y angulo fase
    y genera una imagen
    """
    imagenes = _abrirImagen(rutas)
    datos = []
    for imagen in imagenes:
        lista = np.array(list(imagen.getdata()))
        lista.shape = imagen.size
        datos.append(lista)
    
    magnitud, fase = datos
    if magnitud.size != fase.size:
        raise NoCorrespondenError()
    datos = magnitud*(np.cos(np.deg2rad(fase)) + np.sin(np.deg2rad(fase))*1j)
    inv = pFT.builders.ifft2(datos, datos.shape)
    inversa = inv()
    inversa.shape = inversa.size
    imagen2 = Image.new("L", imagen.size)
    imagen2.putdata(list(np.absolute(inversa)*255))
    return imagen2
    
class NoCorrespondenError(Exception):
    pass
    
def _print(lista):
    for fila in lista:
        for columna in fila:
            print(columna, end='\t')
        print("")
        
def _reordenar(a):
    b = np.concatenate((a[(len(a))/2:,:],a[:(len(a))/2,:]),0)
    c = np.concatenate((b[:,(len(a))/2:], b[:,:(len(a))/2]),1)
    return c