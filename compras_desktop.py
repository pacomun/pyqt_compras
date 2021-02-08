import sys
import threading
import PyQt5.QtWidgets as QtW
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from bd_supermercado import ListaCompra
from conversiones import bool_to_str
from dialogos import DialogoEditar, DialogoNuevo
from barra_progreso import DialogoBarra, HiloObjeto

URI_BASE = 'sqlite:///supermercado.db'


class MyQMainWindow(QtW.QMainWindow):
    """Primer acercamiento a la aplicación de escritorio para lista de
    compras en supermerdado.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Conexión con la base de datos.
        self.lst = ListaCompra(URI_BASE)

        # Llamada a formulario principal y renombrado de widget
        self.uic = loadUi('formulario.ui', self)
        self.grupos = self.uic.grupos
        self.productos = self.uic.productos
        self.statusbar = self.uic.statusbar

        # Menú
        self.menu = self.uic.menubar
        self.menu_limpiar_lista.triggered.connect(self.reset_lista)
        self.menu_nuevo_grupo.triggered.connect(self.nuevo_grupo)

        # Inicio lista de grupos y conecto slots
        self.actualizar_grupos()
        self.__grupo_selec = None
        self.grupos.itemActivated.connect(self.mostrar_productos)
        self.grupos.itemDoubleClicked.connect(self.nuevo_producto)
        self.productos.cellDoubleClicked.connect(self.celda_act)

        # Instancio Dialogo para barra de progreso.
        self.bpr = DialogoBarra()


    def nuevo_producto(self):
        """Método para entrada de un nuevo producto."""
        datos_entrada  = []
        datos_entrada.append(self.lst.grupos())
        datos_entrada.append(self.__grupo_selec.text())
        dlg_nuevo = DialogoNuevo(self, datos_entrada)
        if dlg_nuevo.exec_() == QtW.QDialog.Accepted:
            self.lst.insertar(*datos_entrada)
        self.mostrar_productos(self.__grupo_selec)

    def nuevo_grupo(self):
        grupo, valor = QtW.QInputDialog.getText(self,
                                                'Nuevo Grupo',
                                                'Nombre del grupo:')
        if valor:
            grupo = grupo.replace(' ', '')  # Por si hay espacios.
            self.lst.crear_grupo(grupo)
            self.actualizar_grupos()

    def actualizar_grupos(self):
        """Lista los grupos"""
        grupos = self.lst.grupos()
        self.grupos.clear()
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
        hilo = HiloObjeto(self.lst, self)
        self.bpr.bpr.setValue(0)
        hilo.senal.connect(self.bpr.bpr.setValue)
        self.bpr.show()
        hilo.start()

        if self.__grupo_selec:
            self.mostrar_productos(self.__grupo_selec)


if __name__ == '__main__':
    myapplication = QtW.QApplication(sys.argv)
    myapp = MyQMainWindow()
    myapp.show()
    sys.exit(myapplication.exec_())
