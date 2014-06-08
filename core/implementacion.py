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
    y retorna en forma de imagenes la parte real, parte imaginaria, magnitud y angulo fase
    """
    imagen = _abrirImagen()
    if imagen.format in _formatos:
        if imagen.mode != 'L':
            imagen = imagen.convert('L')
            
        datos = imagen.getdata()
        datos = np.array(datos)
        datos.shape = imagen.size
        transf = pFT.builders.fft2(datos)
        resultado = transf()

        ptReal = Image.new('L', imagen.size)
        datosReal = np.around(resultado.real)
        datosReal.shape = (datosReal.size)
        ptReal.putdata(list(datosReal))  
        
        ptImag = Image.new('L', imagen.size)
        datosImag = np.around(resultado.imag)
        datosImag.shape = (datosImag.size)
        ptImag.putdata(list(datosImag))
        
        magnitud = Image.new('L', imagen.size)
        datosMag = np.around(np.absolute(resultado))
        datosMag.shape = (datosMag.size)
        magnitud.putdata(list(datosMag))
        
        fase = Image.new('L', imagen.size)
        datosFase = np.around(np.rad2deg(np.arctan2(resultado.imag, resultado.real)))
        datosFase.shape = (datosFase.size)
        fase.putdata(list(datosFase))
        
        return ptReal, ptImag, magnitud, fase

def inversa():
    imagenes = _abrirImagen()
    for imagen in imagenes:
        pass

def _print(lista):
    for fila in lista:
        for columna in fila:
            print(columna, end='\t')
        print("")

if __name__ == '__main__':
    _ruta = ['D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\cubosPNG.png']
    img = transformada()
    _ruta2='D:\\Juanpa\\Ingenieria de Sistemas UD\\Semestre V\\Matematicas especiales\\transformadas+\\'
    for i, num in zip(img, range(len(img))):
        i.save(_ruta2 + 'cubosT' + str(num) + '.png')
    
