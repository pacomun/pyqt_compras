import sys
import PyQt5.QtWidgets as QtW
from formulario import Ui_MainWindow
from bd_supermercado import ListaCompra


URI_BASE = 'mysql+pymysql://supermercado:@netbook/supermercado'


class MyQMainWindow(QtW.QMainWindow):
    """Primer acercamiento a la aplicación de escritorio para lista de
    compras en supermerdado.

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.grupos = self.ui.grupos
        self.productos = self.ui.productos
        self.statusbar = self.ui.statusbar
        self.menu = self.ui.menubar
        self.actualizar_gupos()
        self.__grupo_selec = None
        self.grupos.itemActivated.connect(self.mostrar_productos)
        self.productos.cellDoubleClicked.connect(self.celda_act)

    def actualizar_gupos(self):
        """  lista los grupos"""
        self.lst = ListaCompra(URI_BASE)
        grupos = self.lst.grupos()
        for g in grupos:
            self.grupos.addItem(g)

    def celda_act(self, *vargs):
        """ Edita el estado o producto"""
        fila, columna = vargs
        indice = self.productos.item(fila, 0)
        self.statusbar.showMessage(f'fila: {fila + 1}, Columna: {columna + 1}')
        if columna == 2:
            estados = ['0', '1']
            estado, ok = QtW.QInputDialog.getItem(self, 'Editar estado',
                                                  'Introduce el nuevo estado',
                                                  estados)
            print('Estado:', estado, 'OK:', ok)
            if ok:
                self.lst.cambiar_estado(self.__grupo_selec.text(),
                                        indice.text(), int(estado))
                print('Id_producto: ', indice.text())
                self.mostrar_productos(self.__grupo_selec)
        elif columna == 1:
            pass

    def mostrar_productos(self, e):
        """Carga la tabla con el grupo escepecificado en 'e'"""
        self.__grupo_selec = e
        elementos = self.lst.conseguir_elementos(e.text())
        self.productos.setRowCount(len(elementos))
        for fila in range(len(elementos)):
            indice = QtW.QTableWidgetItem(str(elementos[fila][0]))
            product = QtW.QTableWidgetItem(str(elementos[fila][1]))
            estado = QtW.QTableWidgetItem(str(elementos[fila][2]))
            self.productos.setItem(fila, 0, indice)
            self.productos.setItem(fila, 1, product)
            self.productos.setItem(fila, 2, estado)


if __name__ == '__main__':
    myapplication = QtW.QApplication(sys.argv)
    myapp = MyQMainWindow()
    myapp.show()
    sys.exit(myapplication.exec_())
