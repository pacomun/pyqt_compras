"""Programa GUI para gestion del listado de compras de supermercado
con GTK.

"""
import gi
from uri_base import URI_BASE
from bd_supermercado import ListaCompra

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyGMainWindow(Gtk.Window):
    """Ventana principal de la aplicación de escritorio para lista de
    compras en supermercado

    """
    def __init__(self):
        super().__init__(title='Compras Supermercado')
        self.set_default_size(1200, 800)
        self.list_group = Gtk.TreeView()
        self.list_elements = Gtk.TreeView()
        self.lista = ListaCompra(URI_BASE)
        self.store_element = Gtk.ListStore(int, str, bool)
        self.store_group = Gtk.ListStore(str)
        self.packing()
        self.full_list_groups()

        # Creamos las columnas de los elementos
        self.list_elements.set_model(self.store_element)
        render_element = Gtk.CellRendererText()
        column_element = Gtk.TreeViewColumn("Producto", render_element, text=1)
        self.list_elements.append_column(column_element)
        render_state = Gtk.CellRendererToggle()
        column_state = Gtk.TreeViewColumn('Estado', render_state, active=2)
        self.list_elements.append_column(column_state)

    def packing(self):
        """Función para el empaquetado de los elementos en la ventana
        principal."""
        scrol_groups = Gtk.ScrolledWindow()
        scrol_elements = Gtk.ScrolledWindow()
        scrol_groups.add(self.list_group)
        scrol_elements.add(self.list_elements)
        hbox = Gtk.Box(homogeneous=False, spacing=6)
        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            homogeneous=False,
            spacing=6
        )
        hbox.pack_start(scrol_groups, True, True, 0)
        hbox.pack_start(scrol_elements, True, True, 0)
        etiqueta1 = Gtk.Label(label='Etiqueta 1')
        vbox.pack_start(etiqueta1, False, False, 10)
        vbox.pack_start(hbox, True, True, 0)
        self.add(vbox)

    def full_list_groups(self):
        """Llenamos los datos en LisStore"""

        grupos = self.lista.grupos()


        for group in grupos:
            self.store_group.append([group])
        self.list_group.set_model(self.store_group)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Grupos", renderer, text=0)
        self.list_group.append_column(column)

        # Conectar señales
        self.list_group.connect('row-activated', self.grupo_activado)

    def grupo_activado(self, widget, row, col):
        """ Consigue el grupo activado."""
        model = widget.get_model()
        text = model[row][0]
        print(text)
        self.full_list_element(text)

    def full_list_element(self, group):
        elements = self.lista.conseguir_elementos(group)
        self.store_element.clear()

        for element in elements:
            print(element)
            self.store_element.append(element)


if __name__ == '__main__':
    win = MyGMainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    Gtk.main()
