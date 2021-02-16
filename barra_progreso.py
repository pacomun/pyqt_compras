import sys
import PyQt5.QtWidgets
import PyQt5.uic
import PyQt5.Qt
import PyQt5.QtCore
import threading
import time
from bd_supermercado import ListaCompra

URI_BASE = 'mysql+pymysql://supermercado:@netbook/supermercado'


class Ventana(PyQt5.QtWidgets.QDialog):
    """ Ventana de dialog con barra de progreso

    """
    def __init__(self):
        super().__init__()
        self.setGeometry(1000, 1000, 480, 280)
        self.barra = DialogoBarra()
        self.btn_contador = PyQt5.QtWidgets.QPushButton(self)
        self.btn_contador.setText('Pulsa para contar')
        self.btn_contador.move(150, 100)
        self.btn_contador.clicked.connect(self.lanzar_hilo )

    def lanzar_hilo(self):
        mi_hilo = HiloObjeto(self)
        mi_hilo.senal.connect(self.mi_slot)
        self.barra.bpr.setValue(0)
        self.barra.show()
        mi_hilo.senal.connect(self.barra.bpr.setValue)
        mi_hilo.start()

    def mi_slot(self, arg):
        print(arg)

class HiloObjeto(threading.Thread, PyQt5.QtCore.QObject):
    """Un objeto hilo (Thread) para crea subproceso y además QObject, que
    le faculta para emitir señales.

    """

    senal = PyQt5.QtCore.pyqtSignal(int, str)
    final = PyQt5.QtCore.pyqtSignal(int)

    def __init__(self,parent=None):
        threading.Thread.__init__(self)
        PyQt5.QtCore.QObject.__init__(self, parent)
        self.lst = ListaCompra(URI_BASE)

    def run(self):
        """Cambia al estado 0 para todos los productos."""
        grupos = self.lst.grupos()
        for i, grupo in enumerate(grupos):
            i += 1
            self.senal.emit(
                int((i / len(grupos) * 100)), grupo)
            ids = self.lst.conseguir_ids(grupo)
            for j in ids:
                self.lst.cambiar_estado(grupo, j, 0)
        self.final.emit(1)


class DialogoBarra(PyQt5.QtWidgets.QDialog):
    """Documentation for DialogoBarra

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uic = PyQt5.uic.loadUi('barra_progreso.ui', self)
        self.bpr = self.uic.pbr_progreso
        self.uic.setModal(True)

    def slot_progreso(self, entero, cadena):
        self.uic.etq_grupo.setText(
            'Limpiando el grupo {}'.format(cadena)
        )
        self.uic.bpr.setValue(entero)
        if entero == 100:
            self.accept()



if __name__ == '__main__':
    Applicacion = PyQt5.QtWidgets.QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(Applicacion.exec_())
