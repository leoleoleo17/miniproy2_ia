from triangulo_magico import triangulo_magico
from types import MethodType

def crea_test(estado:list, heuristica, vertices):
    '''
    Toma un estado y una heurística y devuelve un
    triángulo mágico con estado como estado inicial y
    con heurística heuristica.
    Input:
        - estado, una matriz con el estado inicial del triángulo
        - heuristica, una función para convertirla en método del triángulo
        - vertices, numero de vértices del triángulo
    Output:
        - t, un objeto triángulo mágico
    '''
    t = triangulo_magico(n=vertices)
    assert len(estado) == len(t.estado_inicial), f"{estado} no es compatible con un triángulo mágico de {t.vertices} vértices" 
    t.heuristica = MethodType(heuristica, t)
    t.estado_inicial = estado
    return t


def test_suite_heuristicas_triangulos(lista_estados:list, lista_heuristicas:list, nombres:list,vertices=3) -> list:
    '''
    Toma una lista de estados y de heurísticas y crea una
    lista de tests donde cada heurística se evalúa sobre
    cada uno de los estados.
    Input:
        - lista_estados, una lista de estados
        - lista_heuristicas, una lista de heurísticas para incluir como métodos
        - lista_nombres, una lista de los nombres de las heurísticas
        - vertices, numero de vértices del triángulo
    Output:
        - lista_tests, una lista con los rompecabezas
        - lista_nombres, una lista con el nombre correspondiente
                         a la heurística del test
    '''
    lista_tests = []
    lista_nombres = []
    for i, heuristica in enumerate(lista_heuristicas):
        for estado in lista_estados:
            test = crea_test(estado, heuristica,vertices)
            lista_tests.append([test])
            lista_nombres.append(nombres[i])
    return lista_tests, lista_nombres