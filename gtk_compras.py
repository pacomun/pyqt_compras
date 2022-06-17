"""Programa GUI para gestion del listado de compras de supermercado
con GTK.

"""
import sys
import gi
from uri_base import URI_BASE
from bd_supermercado import ListaCompra

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gio


class MyGMainWindow(Gtk.ApplicationWindow):
    """Ventana principal de la aplicación de escritorio para lista de
    compras en supermercado

    """
    def __init__(self, application):
        super().__init__(application=application)
        self.set_default_size(1200, 800)
        self.list_group = Gtk.TreeView()
        self.list_elements = Gtk.TreeView()
        self.lista = ListaCompra(URI_BASE)
        self.store_element = Gtk.ListStore(int, str, bool)
        self.store_group = Gtk.ListStore(str)
        self.menubutton = Gtk.MenuButton()
        self.group_selected = ""
        self.packing()
        self.full_list_groups()

        # Crearmos el menú
        menumodel = Gio.Menu()
        self.menubutton.set_menu_model(menumodel)
        menumodel.append("Grupos", "app.new")
        menumodel.append("Productos", "app.quit")



        # Creamos las columnas de los elementos
        self.list_elements.set_model(self.store_element)
        render_element = Gtk.CellRendererText()
        column_element = Gtk.TreeViewColumn("Producto", render_element, text=1)
        self.list_elements.append_column(column_element)
        render_state = Gtk.CellRendererToggle()
        column_state = Gtk.TreeViewColumn('Estado', render_state, active=2)
        # Conecto señal a la segunda columna visible
        render_state.connect('toggled', self.on_cell_toggled)
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
        menubox = Gtk.Box()
        menubox.pack_start(self.menubutton, False, False, 0)
        vbox.pack_start(menubox, False, False, 0)
        vbox.pack_start(hbox, True, True, 0)
        self.add(vbox)

    def full_list_groups(self):
        """Llenamos los datos en LisStore"""
        # Creo un modelo para asociar a TreeView para grupos
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
        """ Consigue el grupo activado y muestra los elementos"""
        model = widget.get_model()
        text = model[row][0]
        self.full_list_element(text)
        self.group_selected = text

    def full_list_element(self, group):
        """Actualiza los elementos del grupo suministrado."""
        elements = self.lista.conseguir_elementos(group)
        self.store_element.clear()

        for element in elements:
            self.store_element.append(element)

    def on_cell_toggled(self, widget, path):
        """Invierte el valor del estado seleccionado"""
        self.store_element[path][2] = not self.store_element[path][2]
        self.lista.cambiar_estado(self.group_selected,
                                  self.store_element[path][0],
                                  int(self.store_element[path][2]))


class Application(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        window = MyGMainWindow(self)
        window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.mensaje)
        self.add_action(new_action)

    def mensaje(self, valor, valor2):
        print('Pulsado  ', valor)
        print(valor2)


if __name__ == '__main__':
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)
