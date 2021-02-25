import sys
import PyQt5.QtWidgets
import PyQt5.uic
import PyQt5.Qt
import PyQt5.QtCore
import threading
import time
from bd_supermercado import ListaCompra
from uri_base import URI_BASE


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
    """Ventana que muestra barra de progreso."""
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
    sys.exit(Applicacion.exec_())
