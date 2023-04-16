import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import namedtuple
class triangulo_magico:
    '''
    @Autores: Juan Esteban Gonzalez y Leonardo Luengas
    
    Clase que construye un triangulo mágico con n nodos en cada arista.
    Objetivo: Encontrar una asignación de los números naturales del 1 hasta el 3(n-1) de tal forma que la suma de todos los
    números en cada arista sea igual y no se repitan números en ningún nodo.
    Input: n, numero de vértices por lado
    Output: triángulo mágico de n vértices por lado
    '''
    def __init__(self, n=3):
        '''
        Inicializa el triángulo mágico con una asignación aleatoria de números.
        '''
        l = [x for x in range(1,3*n-2)]
        random.shuffle(l)
        self.estado_inicial= l
        self.vertices = n
        self.max = max(l)
        
    def pintar_estado(self,estado):
        '''
        Input: recibe una lista que representa un estado del triángulo mágico con n vértices en cada lado
        Output: Dibuja la representación gráfica del triángulo mágico
        '''
        assert len(estado) == len(self.estado_inicial), f"{estado} no es compatible con un triangulo mágico de {self.vertices} vértices" 
        G = nx.Graph()
        G.add_nodes_from(estado)
        estado1 = estado[1:]
        estado1.append(estado[0])
        E = [e for e in zip(estado,estado1)]
        G.add_edges_from(E)
        order = {}
        n = self.vertices
        for i in range(n):
            e1 = estado[i]
            e2 = estado[i+n-1]
            e3 = estado[i+2*(n-1)-1]
            order[e1] = [i,0]
            order[e2] = [(n-1)-(i/2),(np.sqrt(3)*i)/2]
            order[e3] = [(n-i)/2,(np.sqrt(3)*(n-i))/2]
        nx.draw_networkx(G,pos=order)
        plt.show()
        
    def acciones_aplicables(self, estado):
        '''
        Input: estado, una lista que representa el triángulo mágico con n vértices en cada lado
        Output: Una lista con todas las tuplas que se pueden intercambiar para un estado. Son listas con dos tuplas de la forma
        (indice_del_elemento, elemento)
        '''
        assert len(estado) == len(self.estado_inicial), f"{estado} no es compatible con un triangulo mágico de {self.vertices} vértices" 
        res = []
        tot = 3*(self.vertices-1)+1
        for i, e in enumerate(estado):
            if e != self.max:
                inicial = (i,e)
                temp = [(f,y) for f,y in enumerate(estado) if y != e and y != self.max]
                for x in temp:
                    new = [(x,inicial)]
                    res += new
        #Truncar las acciones aplicables a 5 seleccionadas aleatoriamente para acelerar la convergencia de una solución
        res_trunc = random.choices(res, k=5)
        return res_trunc
    
    def transicion(self, estado, accion):
        '''
        Input: estado, una lista que representa un estado del problema del triángulo mágico con n vértices en cada lado
               accion, una lista con dos tuplas de la forma (indice_del_elemento, elemento).
        Output: lista con la acción ya aplicada
        '''
        assert len(accion) == 2 and accion[0][1] in self.estado_inicial and accion[1][1] in self.estado_inicial, "La acción no es válida"
        estado[accion[0][0]] = accion[1][1]
        estado[accion[1][0]] = accion[0][1]
        return estado
    
    def test_objetivo(self, estado):
        '''
        Input: estado, una lista que representa un estado del problema del triángulo mágico con n vértices en cada lado
        Output: Booleano que representa si el estado satisface el objetivo del problema
        '''
        setl=set(estado)
        if len(setl) !=len(estado) or (0 in estado):
            return False
        n = self.vertices
        fila1 = [estado[x] for x in range(0,n)]
        fila2 = [estado[x] for x in range(n-1,2*n-1)]
        fila3 = [estado[x] for x in range(2*(n-1),len(estado))]
        fila3.append(estado[0])
        matrix = np.matrix([fila1,fila2,fila3]).sum(axis=1)
        x = matrix[0]
        return (x==matrix).all()
        
    def costo(self, estado, accion):
        '''
        Input: estado, una lista que representa un estado del problema del triángulo mágico con n vértices en cada lado
               accion, una tupla con dos elementos que representan el índice de un elemento de la lista y el valor con el cual
               se va a reemplazar dicho índice.
        Output:int, entero positivo que representa el costo de realizar la acción sobre el triángulo
        '''
        return 1
    
    def codigo(self, estado):
        '''
        Input: estado, una lista que representa un estado del problema del triángulo mágico con n vértices en cada lado
        Output: string, que representa el estado
        '''
        assert len(estado) == len(self.estado_inicial), f"{estado} no es compatible con un triangulo mágico de {self.vertices} vértices" 
        cod = ''
        for x in estado:
            cod += str(x)
        return cod 

Tupla = namedtuple('Tupla', ['elemento', 'valor'])
#ListaPrioritaria modificada para contener un máximo de 1000 elementos
class ListaPrioritaria():
    
    def __init__(self):
        self.pila = []
        
    def __len__(self):
        return len(self.pila)

    def push(self, elemento, valor):
          if len(self.pila) != 1000:
            tupla = Tupla(elemento, valor)
            self.pila.append(tupla)
            self.pila.sort(key=lambda x: x[1])
            
    def pop(self):
        return self.pila.pop(0)[0]
    
    def is_empty(self):
        return len(self.pila) == 0
    
    def __len__(self):
        return len(self.pila)

    def __str__(self):
        cadena = '['
        inicial = True
        for elemento, valor in self.pila:
            if inicial:
                cadena += '(' + str(elemento) + ',' + str(valor) + ')'
                inicial = False
            else:
                cadena += ', (' + str(elemento) + ',' + str(valor) + ')'
        return cadena + ']'      