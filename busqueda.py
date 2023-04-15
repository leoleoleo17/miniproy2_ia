import numpy as np
from types import MethodType

class Nodo:

    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo

def nodo_hijo(problema, madre, accion):

    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase ocho_reinas
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo

    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)

def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]

def depth(nodo):
    if nodo.madre == None:
        return 0
    else:
        return depth(nodo.madre) + 1

def camino_codigos(nodo):
    if nodo.madre == None:
        return [nodo.codigo]
    else:
        return camino_codigos(nodo.madre) + [nodo.codigo]

def is_cycle(nodo):
    codigos = camino_codigos(nodo)
    return len(set(codigos)) != len(codigos)

def expand(problema, nodo):
    s = nodo.estado
    nodos = []
    for accion in problema.acciones_aplicables(s):
        hijo = nodo_hijo(problema, nodo, accion)
        nodos.append(hijo)
#    print(f"El nodo {nodo.codigo} tiene los hijos {[n.codigo for n in nodos]}")
    return nodos

def anchura(problema):
    
    '''Método de búsqueda primero en anchura'''
    
    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    if problema.test_objetivo(nodo.estado):
            return nodo
    frontera = [nodo]
    while len(frontera) > 0:
        nodo = frontera.pop(0)
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if not is_cycle(hijo):
                frontera.append(hijo)
    return None

def profundidad(problema):

    '''Método de búsqueda primero en profundidad'''

    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    if problema.test_objetivo(nodo.estado):
            return nodo
    frontera = [nodo]
    while len(frontera) > 0:
        nodo = frontera.pop()
        acciones = problema.acciones_aplicables(nodo.estado)
        for a in acciones:
            hijo = nodo_hijo(problema, nodo, a)
            if problema.test_objetivo(hijo.estado):
                return hijo
            if not is_cycle(hijo):
                frontera.append(hijo)
    return None

def backtracking(problema, nodo):

    '''Método de búsqueda backtracking'''

    if problema.test_objetivo(nodo.estado):
        return nodo
    acciones = problema.acciones_aplicables(nodo.estado)
    for a in acciones:
        hijo = nodo_hijo(problema, nodo, a)
        if not is_cycle(hijo):
            resultado = backtracking(problema, hijo)
            if resultado is not None:
                return resultado    
    return None

def profundidad_limitada(problema, l):
    '''Función de búsqueda depth-limited search'''
    nodo = Nodo(problema.estado_inicial, None, None, 0, problema.codigo(problema.estado_inicial))
    frontera = [nodo]
    resultado = None
    while len(frontera) > 0:
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        if depth(nodo) >= l:
            resultado = 'cutoff'
        elif not is_cycle(nodo):
            frontera += expand(problema, nodo)
    return resultado

def expand(problema, nodo):
    s = nodo.estado
    nodos = []
    for accion in problema.acciones_aplicables(s):
        hijo = nodo_hijo(problema, nodo, accion)
        nodos.append(hijo)
    return nodos

def profundizacion(problema, l_max, DEB=False):
    for depth in range(0, l_max + 1):
        if DEB:
            print("Buscando a profundidad máxima ", depth)
        resultado = profundidad_limitada(problema, depth)
        if resultado != 'cutoff':
            return resultado