'''
Created on 3/06/2014
@author: Juan Pablo Moreno - 20111020059
@author:
@author:
@author:
'''
from PyQt4.QtGui import QMainWindow, QDialog, QFileDialog, QSizePolicy
from PyQt4.QtGui import QComboBox, QPushButton, QMessageBox, QLabel

class VentanaMenu(QMainWindow):
    def __init__(self):
        super(VentanaMenu, self).__init__()
        self.inicializar()
        
    def inicializar(self):
        self.titulo = QLabel("PROCESAMIENTO DIGITAL DE IMAGENES", self)
        self.titulo.move(50,50)
        self.titulo.adjustSize()
        
        self.filtrar = QPushButton("Filtrar", self)
        self.filtrar.move(100,100)
        self.filtrar.clicked.connect(self.abrirFiltrar)
        
        self.analizar = QPushButton("Analizar", self)
        self.analizar.move(100,150)
        self.analizar.clicked.connect(self.abrirAnalizar)
        
        self.invertir = QPushButton("Invertir", self)
        self.invertir.move(100,200)
        self.invertir.clicked.connect(self.abrirInvertir)
        self.setWindowTitle("Transformada de Fourier")
        self.resize(300,300)
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.show()
        
    def abrirFiltrar(self):
        self.ventanaFiltrar = VentanaFiltrar(self)
    
    def abrirAnalizar(self):
        archivo = QFileDialog(self)
        ruta = archivo.getOpenFileName(self, 'Seleccionar imagen', '', "Images (*.png *.gif *.jpg *.bmp)")
        if not ruta.isEmpty():
            try:
                from core import transformar
                img1, img2 = transformar(str(ruta))
                ruta1 = archivo.getSaveFileName(self, "Guardar Magnitud", '', "Images (*.png *.gif *.jpg *.bmp)")
                img1.save(str(ruta1) + ".png")
                ruta2 = archivo.getSaveFileName(self, "Guardar Fase", '', "Images (*.png *.gif *.jpg *.bmp)")
                img2.save(str(ruta2) + ".png")
            except ImportError:
                resp = QMessageBox.information(self, 'Error', 'Hubo un error inesperado', 
                                        QMessageBox.Ok, QMessageBox.NoButton)
        else:
            resp = QMessageBox.information(self, 'Error', 'No ha elegido imagenes', 
                                        QMessageBox.Ok, QMessageBox.NoButton)
    
    def abrirInvertir(self):
        self.ventanaInversa = VentanaInvertir(self)
    
class VentanaFiltrar(QDialog):
    def __init__(self, padre):
        super(VentanaFiltrar, self).__init__(padre)
        self.inicializar()
    
    def inicializar(self):
        self.titulo = QLabel("SELECCIONE EL FILTRO A APLICAR", self)
        self.titulo.move(50,50)
        self.titulo.adjustSize()
        
        self.filtros = QComboBox(self)
        self.filtros.move(100,100)
        self.filtros.sizeAdjustPolicy()
        self.filtros.addItem("Low pass filter")
        self.filtros.addItem("High pass filter")
        self.filtros.addItem("Gaussian filter")
        self.filtros.addItem("Pyramidal filter")
        self.filtros.addItem("Sinc filter")
        
        self.seleccionar = QPushButton("Seleccionar imagen", self)
        self.seleccionar.move(100,200)
        self.seleccionar.clicked.connect(self.filtrar)
        self.setWindowTitle("Filtrar una imagen")
        self.resize(300,300)
        self.setWindowModality(1)
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.show()
        
    def filtrar(self):
        archivo = QFileDialog(self)
        ruta = archivo.getOpenFileName(self, 'Seleccionar imagen', '', "Images (*.png *.gif *.jpg *.bmp)")
        if not ruta.isEmpty():
            try:
                from core import filtrar
                img = filtrar(str(ruta), str(self.filtros.currentText()))
                ruta1 = archivo.getSaveFileName(self, "Guardar imagen", '', "Images (*.png *.gif *.jpg *.bmp)")
                img.save(str(ruta1) + ".png")
            except ImportError:
                resp = QMessageBox.information(self, 'Error', 'Hubo un error inesperado', 
                                        QMessageBox.Ok, QMessageBox.NoButton)
        else:
            resp = QMessageBox.information(self, 'Error', 'No ha elegido imagenes', 
                                        QMessageBox.Ok, QMessageBox.NoButton)

class VentanaInvertir(QDialog):
    def __init__(self, padre):
        super(VentanaInvertir, self).__init__(padre)
        self.inicializar()
        
    def inicializar(self):
        self.titulo = QLabel("SELECCIONE LAS IMAGENES DE MAGNITUD Y FASE", self)
        self.titulo.move(50,50)
        self.titulo.adjustSize()
        
        self.magnitud = QPushButton("magnitud", self)
        self.magnitud.move(100,200)
        self.magnitud.clicked.connect(self.seleccionar)
        """
        self.fase = QPushButton("fase", self)
        self.fase.move(100,150)
        self.fase.clicked.connect(self.seleccionar)
        """
        self.setWindowTitle("Transformada Inversa")
        self.resize(300,300)
        self.setWindowModality(1)
        self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.show()
        
    def seleccionar(self):
        archivo = QFileDialog(self)
        ruta1 = archivo.getOpenFileName(self, 'Seleccionar magnitud', '', "Images (*.png *.gif *.jpg *.bmp)")
        ruta2 = archivo.getOpenFileName(self, 'Seleccionar fase', '', "Images (*.png *.gif *.jpg *.bmp)")
        if not ruta1.isEmpty() and not ruta2.isEmpty():
            from core import invertir, NoCorrespondenError
            try:
                img = invertir((str(ruta1), str(ruta2)))
                ruta3 = archivo.getSaveFileName(self, 'Guardar imagen', '', "Images (*.png *.gif *.jpg *.bmp)")
                img.save(str(ruta3) + ".png")
            except NoCorrespondenError:
                resp = QMessageBox.information(self, 'Error', 'Las imagenes no corresponden', 
                                        QMessageBox.Ok, QMessageBox.NoButton)    
        else:
            resp = QMessageBox.information(self, 'Error', 'No ha elegido imagenes', 
                                        QMessageBox.Ok, QMessageBox.NoButton)
