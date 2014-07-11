'''
Created on 1/05/2014
@author: Juan Pablo Moreno - 20111020059
'''

import sys
from PyQt4.QtGui import QApplication
from GUI import VentanaMenu 

def main():
    app = QApplication(sys.argv)
    ventana = VentanaMenu()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()