import sys
import PyQt5.QtWidgets
from conversiones import str_to_bool
from PyQt5.uic import loadUi


class DialogoEditar(PyQt5.QtWidgets.QDialog):
    """Documentation for DialogoEditar

    """
    def __init__(self, registro, parent=None, titulo=''):
        super().__init__(parent)
        super().setModal(True)
        self.registro = registro
        self.setWindowTitle(titulo)
        self.setContentsMargins(40, 5, 40, 15)
        self.setFixedSize(480, 200)
        self.layout = PyQt5.QtWidgets.QFormLayout(self)
        self.etq_texto = PyQt5.QtWidgets.QLabel()
        self.etq_texto.setText('Editar datos para...')
        self.layout.addRow(self.etq_texto)
        self.etq_pto = PyQt5.QtWidgets.QLabel()
        self.etq_pto.setText('Producto: ')
        self.producto = PyQt5.QtWidgets.QLineEdit()
        self.producto.setText(registro[1])
        self.layout.addRow(self.etq_pto, self.producto)
        self.estado = PyQt5.QtWidgets.QComboBox()
        self.estado.addItem('HAY')
        self.estado.addItem('COMPRAR')
        self.etq_estado = PyQt5.QtWidgets.QLabel()
        self.etq_estado.setText('Estado: ')
        self.layout.addRow(self.etq_estado, self.estado)
        self.btn_aceptar = PyQt5.QtWidgets.QPushButton()
        self.btn_aceptar.setText('Aceptar')
        self.btn_cancelar = PyQt5.QtWidgets.QPushButton()
        self.btn_cancelar.setText('Cancelar')
        self.grup_btn = PyQt5.QtWidgets.QHBoxLayout()
        self.grup_btn.addWidget(self.btn_aceptar)
        self.grup_btn.addWidget(self.btn_cancelar)
        self.layout.addRow(self.grup_btn)

        self.btn_cancelar.clicked.connect(self.close)
        self.btn_aceptar.clicked.connect(self.aceptar)

    def aceptar(self, *args):
        self.registro[1] = self.producto.text()
        self.registro[2] = str_to_bool(self.estado.currentText())
        self.accept()

class DialogoNuevo(PyQt5.QtWidgets.QDialog):
    """Ventana de dialogo para recabar datos de entrada de un nuevo
    producto.

    """
    def __init__(self, parent=None, lista=[]):
        super().__init__(parent)
        self.lista = lista
        self.uic = loadUi('nuevo_producto.ui', self)
        self.uic.dialogButtonBox.accepted.connect(self.accept)
        self.uic.comboBox.addItems(self.lista[0])

    def accept(self):
        self.lista.clear()
        self.lista.append(self.uic.comboBox.currentText())
        self.lista.append(self.uic.input_producto.text())
        self.lista.append(self.uic.checkBox.isChecked())
        super().accept()


if __name__ == '__main__':
    Aplicacion = PyQt5.QtWidgets.QApplication(sys.argv)
    reg = [1, 'Algo', 0]
    mi_app = DialogoEditar(registro=reg, titulo='Edición de Registro')
    mi_app.show()
    print(reg)

    Aplicacion.exec_()
