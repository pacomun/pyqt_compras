import sys
import threading
import PyQt5.QtWidgets as QtW
from PyQt5.QtCore import Qt
from formulario import Ui_MainWindow
from bd_supermercado import ListaCompra
from conversiones import bool_to_str
from dialogos import DialogoEditar

URI_BASE = 'mysql+pymysql://supermercado:@netbook/supermercado'


class MyQMainWindow(QtW.QMainWindow):
    """Primer acercamiento a la aplicación de escritorio para lista de
    compras en supermerdado.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.grupos = self.uic.grupos
        self.productos = self.uic.productos
        self.statusbar = self.uic.statusbar
        self.menu = self.uic.menuLista
        self.menu_lista = self.menu.addAction('Limpiar lista.')
        # Hilo para función pesada.
        self.menu_lista.triggered.connect(self.llamo_hilo)
        self.actualizar_grupos()
        self.__grupo_selec = None
        self.grupos.itemActivated.connect(self.mostrar_productos)
        self.productos.cellDoubleClicked.connect(self.celda_act)

    def actualizar_grupos(self):
        """Lista los grupos"""
        self.lst = ListaCompra(URI_BASE)
        grupos = self.lst.grupos()
        for grupo in grupos:
            self.grupos.addItem(grupo)

    def celda_act(self, *vargs):
        """Edita producto."""
        fila, columna = vargs
        indice = self.productos.item(fila, 0)
        self.statusbar.showMessage(
            f'fila: {fila + 1}, Columna: {columna + 1}')
        if columna == 2:
            registro = self.lst.elemento(self.__grupo_selec.text(),
                                         indice.text())
            estado = not registro[2]
            self.lst.cambiar_estado(self.__grupo_selec.text(),
                                    indice.text(), estado)

        elif columna == 1:
            reg = self.lst.elemento(self.__grupo_selec.text(),
                                    int(indice.text()))
            registro = list(reg)
            dialogo = DialogoEditar(registro, self, 'Editar Registo')
            dialogo.show()
            dialogo.exec_()
            if registro == list(reg):
                self.statusbar.showMessage(
                    'Sin cambios en el registro')
            else:
                self.lst.actualizar_registro(
                    self.__grupo_selec.text(), registro)
        self.mostrar_productos(self.__grupo_selec)

    def mostrar_productos(self, e):
        """Carga la tabla con el grupo escepecificado en 'e'"""
        self.__grupo_selec = e
        elementos = self.lst.conseguir_elementos(e.text())
        self.productos.setRowCount(len(elementos))
        for fila, elemento in enumerate(elementos):
            indice = QtW.QTableWidgetItem(str(elemento[0]))
            product = QtW.QTableWidgetItem(str(elemento[1]))
            estado = QtW.QTableWidgetItem(bool_to_str(elemento[2]))
            indice.setTextAlignment(Qt.AlignRight)
            self.productos.setItem(fila, 0, indice)
            self.productos.setItem(fila, 1, product)
            estado.setTextAlignment(Qt.AlignHCenter)
            self.productos.setItem(fila, 2, estado)

    def reset_lista(self):
        """Cambia al estado 0 para todos los productos."""
        self.statusbar.showMessage('Limpiado la lista de compra, espere...')
        grupos = self.lst.grupos()
        for grupo in grupos:
            self.statusbar.showMessage(f'Limpiado {grupo}')
            ids = self.lst.conseguir_ids(grupo)
            for i in ids:
                self.lst.cambiar_estado(grupo, i, 0)
        self.statusbar.showMessage('Se ha limpiado la lista.')
        self.mostrar_productos(self.__grupo_selec)

    def llamo_hilo(self):
        """ Crea hilo para llamar a self.reset_lista."""
        mi_hilo = threading.Thread(target=self.reset_lista)
        mi_hilo.start()


if __name__ == '__main__':
    myapplication = QtW.QApplication(sys.argv)
    myapp = MyQMainWindow()
    myapp.show()
    sys.exit(myapplication.exec_())
