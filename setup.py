'''
Created on 11/07/2014

@author: Juanpa y Yami
'''

from cx_Freeze import setup, Executable

#includes = ["atexit", "PyQt4.QtGui", "numpy", "PIL", "pyfftw.builders"]
packages = ["GUI", "core"]
setup(
      options={"build_exe":{"packages":packages, "excludes":["Tkinter"]}}, 
      name="Transformada de Fourier",
      version="0.5",
      description="Programa que calcula la FTT de imagenes",
      executables = [Executable(script="mainffT.py", base="Win32GUI")]
      )