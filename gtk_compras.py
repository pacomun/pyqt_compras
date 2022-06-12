"""Programa GUI para gestion del listado de compras de supermercado
con GTK.

"""
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyGMainWindow(Gtk.Window):
    """Ventana principal de la aplicación de escritorio para lista de
    compras en supermercado

    """
    def __init__(self):
        super().__init__(title='Compras Supermercado')
        self.grid = Gtk.Grid()
        self.list_group = Gtk.TreeView()
        self.scrollable = Gtk.ScrolledWindow()
        self.full_list()
        self.packing()

    def packing(self):
        self.scrollable.add(self.list_group)
        self.grid.attach(self.scrollable, 0, 1, 3, 4)
        etiqueta1 = Gtk.Label(label='Etiqueta 1')
        self.grid.attach(etiqueta1, 0, 0, 1, 1)
        self.add(self.grid)

    def full_list(self):
        grupos = ['Frutería', 'Comestibles', 'Aseo Personal',
                  'Congelados']
        store_group = Gtk.ListStore(str)
        for group in grupos:
            store_group.append([group])
        self.list_group.set_model(store_group)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Grupos", renderer, text=0)
        self.list_group.append_column(column)


        
if __name__ == '__main__':
    win = MyGMainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    Gtk.main()
