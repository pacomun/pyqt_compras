""" Funciones auxiliares """


def bool_to_str(boleano):
    """Convierte booleano a cadena 'COMPRAR' ó 'HAY'"""
    if boleano:
        return 'COMPRAR'
    else:
        return 'HAY'


def str_to_bool(cadena):
    """Convierte cadena a entero (0, ó 1). Si la cadena no es correcta
    lanza una excepción."""
    if cadena == 'COMPRAR':
        return 1
    elif cadena == 'HAY':
        return 0
    else:
        raise ValueError(
            "Se espera 'COMPRAR' o 'HAY' sea ha pasado: {}".format(cadena))


if __name__ == '__main__':
    print(bool_to_str(0))
    print(bool_to_str(1))
    print(bool_to_str(2.3))
    print(str_to_bool('HAY'))
    print(str_to_bool('Otra cadena'))
