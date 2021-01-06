import sys
import PyQt5.QtWidgets as QtW
from formulario import Ui_MainWindow
from bd_supermercado import ListaCompra


URI_BASE = 'mysql+pymysql://supermercado:@netbook/supermercado'


class My_QMainWindow(QtW.QMainWindow):
    """Primer acercamiento a la aplicación de escritorio para lista de
    compras en supermerdado.

    """
    def __init__(self, parent=None):
        super(My_QMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.grupos = self.ui.grupos
        self.productos = self.ui.productos

        self.lst = ListaCompra(URI_BASE)
        grupos = self.lst.grupos()
        for g in grupos:
            self.grupos.addItem(g)


if __name__ == '__main__':
    myapplication = QtW.QApplication(sys.argv)
    myapp = My_QMainWindow()
    myapp.show()
    sys.exit(myapplication.exec_())
