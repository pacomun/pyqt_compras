import sys
import threading
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtW
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QTextDocument
from bd_supermercado import ListaCompra
from conversiones import bool_to_str
from dialogos import DialogoEditar, DialogoNuevo
from barra_progreso import DialogoBarra, HiloObjeto
from uri_base import URI_BASE


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
        self.textEdit = self.uic.textEdit
        self.textEdit.setReadOnly(True)

        # Menú
        self.menu = self.uic.menubar
        self.menu_limpiar_lista.triggered.connect(self.reset_lista)
        self.menu_nuevo_grupo.triggered.connect(self.nuevo_grupo)
        self.menu_borrar_grupo.triggered.connect(self.borrar_grupo)
        self.menu_nuevo_producto.triggered.connect(self.nuevo_producto)
        self.menu_borrar_producto.triggered.connect(self.borrar_producto)

        # Conecto botón de búsqueda
        self.btn_buscar.clicked.connect(self.buscar_registro)

        # Inicio lista de grupos y conecto slots
        self.actualizar_grupos()
        self.__grupo_selec = None
        self.grupos.itemClicked.connect(self.mostrar_productos)
        self.grupos.itemDoubleClicked.connect(self.nuevo_producto)
        self.productos.cellDoubleClicked.connect(self.celda_act)
        self.input_buscar.returnPressed.connect(self.buscar_registro)

        # Coloco un texto de ejemplo
        self.textEdit.setHtml('<h3>Cadena de ejemplo</h3>')
        self.textEdit.append('<p>Cuerpo <b>del</b> texto</p>')


        # Instancio Dialogo para barra de progreso.
        self.bpr = DialogoBarra()

        # Centro la ventana principal.
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra la ventana en el escritorio."""
        disponible = QtW.QDesktopWidget().availableGeometry()
        ventana = self.geometry()
        print('Dimesiones disponibles: ', disponible)
        print('Dimesiones de la Ventana: ', ventana)
        self.move(
            int((disponible.width() - ventana.width()) / 2),
            int((disponible.height() - ventana.height()) / 2))

    def borrar_grupo(self):
        """Borra la tabla seleccionada. Muestra mensaje de
        confirmación."""
        if self.__grupo_selec:
            grupo_seleccionado = self.__grupo_selec.text()
        else:
            self.statusbar.showMessage(
                'No se ha seleccionado ningún grupo.')
            return
        # Construir ventana de confirmación.
        mensaje = '¿Quieres borrar el grupo {}'.format(
            grupo_seleccionado)
        respuesta = QtW.QMessageBox()
        respuesta.setIcon(QtW.QMessageBox.Question)
        respuesta.setWindowTitle('Borrar Grupo Seleccionado')
        respuesta.setInformativeText(mensaje)
        respuesta.setStandardButtons(
            QtW.QMessageBox.Yes | QtW.QMessageBox.No)
        if QtW.QMessageBox.Yes == respuesta.exec():
            self.lst.borrar_grupo(grupo_seleccionado)
            self.statusbar.showMessage(
                'Se ha borrado el grupo {}'.format(grupo_seleccionado))
            self.__grupo_selec = None
            self.actualizar_grupos()
            self.mostrar_productos(self.__grupo_selec)

    def nuevo_producto(self, grupo=None):
        """Método para entrada de un nuevo producto."""
        datos_entrada = []
        # Si grupo = None -> La llamada es desde el menú.
        if not grupo:
            datos_entrada.append(self.lst.grupos())
        else:
            datos_entrada.append([grupo.text(), ])
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

    def actualizar_grupos(self, lst_grupos=None):
        """Lista los grupos"""
        if lst_grupos:
            grupos = lst_grupos
        else:
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

    def limpiar_tabla(self):
        self.productos.setRowCount(0)

    def mostrar_productos(self, elec):
        """Carga la tabla con el grupo escepecificado en 'elec'"""
        self.__grupo_selec = elec
        if self.__grupo_selec is None:
            self.limpiar_tabla()
            return
        elementos = self.lst.conseguir_elementos(elec.text())
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
        """ Pone todos los estados de los productos en 0."""
        hilo = HiloObjeto(self)
        self.bpr.bpr.setValue(0)
        hilo.senal.connect(self.bpr.slot_progreso)
        hilo.final.connect(self.actualizar)
        self.bpr.show()
        hilo.start()

    def actualizar(self):
        self.mostrar_productos(self.__grupo_selec)
        self.statusbar.showMessage('La tabla se ha limpiado.')

    def borrar_producto(self):
        """Borra un elemento de un grupo."""
        if self.__grupo_selec is not None:
            grupo = self.__grupo_selec.text()
            if self.productos.currentRow() >= 0:
                celda = self.productos.item(
                    int(self.productos.currentRow()), 0)
                self.lst.borrar_elemento(grupo, int(celda.text()))
                self.mostrar_productos(self.__grupo_selec)

    def buscar_registro(self):
        """Muestra en tabla los resultados de la búsqueda de producto."""
        self.limpiar_tabla()
        cadena = self.input_buscar.text()
        coincidencias = self.lst.buscar_registro(cadena)
        if not coincidencias:
            return
        grupo = QtW.QListWidgetItem(coincidencias[0][0])
        self.__grupo_selec = grupo
        if coincidencias:
            self.productos.setRowCount(len(coincidencias))
            for fila, elemento in enumerate(coincidencias):
                if elemento[0] == grupo.text():
                    indice = QtW.QTableWidgetItem(str(elemento[1]))
                    producto = QtW.QTableWidgetItem(elemento[2])
                    estado = QtW.QTableWidgetItem(bool_to_str(
                        elemento[3]))
                    self.productos.setItem(fila, 0, indice)
                    self.productos.setItem(fila, 1, producto)
                    estado.setTextAlignment(Qt.AlignHCenter)
                    self.productos.setItem(fila, 2, estado)


if __name__ == '__main__':
    myapplication = QtW.QApplication(sys.argv)
    myapp = MyQMainWindow()
    myapp.show()
    sys.exit(myapplication.exec_())
