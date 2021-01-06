from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import MetaData
from sqlalchemy.exc import NoSuchTableError, OperationalError


URI_BASE = 'mysql+pymysql://supermercado:@netbook/supermercado'


class ListaCompra():
    """Documentation for ListaCompra

    """
    def __init__(self, base=URI_BASE):
        self.base = base
        self.engine = create_engine(URI_BASE, echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData()

    def crear_grupo(self, grupo):
        try:
            grupo = Table(grupo, self.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('product', String(60), nullable=False,
                                 unique=True),
                          Column('estado', Integer),
                          extend_existing=True)
            self.metadata.create_all(self.engine)
        except Exception as e:
            print(e)

    def insertar(self, grupo, product, estado=0):
        try:
            grupo = Table(grupo, self.metadata, autoload=True,
                          autoload_with=self.engine)
            ins = grupo.insert().values(product=product, estado=estado)
            self.engine.execute(ins)
        except Exception as e:
            print(e)

    def grupos(self):
        self.metadata.reflect(self.engine)
        return list(self.metadata.tables.keys())

    def borrar_grupo(self, grupo):
        try:
            grupo = self.__carga_tabla(grupo)
        except NoSuchTableError:
            print('La tabla no existe')
        else:
            self.metadata.drop_all(tables=(grupo,), bind=self.engine)

    def conseguir_elementos(self, grupo):
        tabla = self.__carga_tabla(grupo)
        salida = []
        for consulta in self.session.query(tabla).order_by(tabla.c.product):
            salida.append(consulta)
        self.session.close()
        return salida

    def conseguir_ids(self, grupo):
        tabla = self.__carga_tabla(grupo)
        ids = []
        for consulta in self.session.query(tabla.c.id).order_by(tabla.c.id):
            ids.append(consulta[0])  # Devuelve tupla.
        self.session.close()
        return ids

    def cambiar_estado(self, grupo, indice, estado):
        tabla = self.__carga_tabla(grupo)
        actualizar = tabla.update().where(
            tabla.c.id == indice).values(estado=estado)
        self.engine.execute(actualizar)

    def __carga_tabla(self, tabla):
        return Table(tabla, self.metadata, autoload=True,
                     autoload_with=self.engine)

    def borrar_elemento(self, grupo, indice):
        """Borra un elemento dado de su grupo (table) e índice"""
        tabla = self.__carga_tabla(grupo)
        borrado = tabla.delete().where(tabla.c.id == indice)
        self.engine.execute(borrado)


if __name__ == '__main__':
    conn = ListaCompra()
    conn.borrar_grupo('aseo_personal')
    conn.borrar_grupo('congelados')
    conn.crear_grupo('aseo_personal')
    conn.insertar('aseo_personal', 'Pasta de dientes')
    conn.crear_grupo('congelados')
    conn.insertar('congelados', 'guisantes', 1)
    print(conn.grupos())
    salida = conn.conseguir_elementos('congelados')
    print(salida)
    for i in conn.conseguir_ids('aseo_personal'):
        print(i)

    conn.cambiar_estado('congelados', 1, 0)
    salida = conn.conseguir_elementos('congelados')
    print(salida)
