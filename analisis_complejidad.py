# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 21:45:09 2023

@author: nicoo
"""

# Diseño y Análise de Algoritmos: Práctica 2
# Nicolás Aller Ponte, Esteban Rodríguez García, Eduardo de Carricarte Pérez

import time
from prettytable import PrettyTable
from numpy.random import seed
from numpy.random import randint
import math
import statistics
seed(1)

"""1º Implementacion en Python de los algortimos proporcionados"""""

"Implementacion del algoritmo de insercion"
def insertionSort(v):
    n = len(v)
    for i in range(1,n):
        x = v[i]
        j = i-1
        while j >= 0 and v[j] > x:
            v[j+1] = v[j]
            j = j-1
        v[j+1] = x



def bubbleSort(v):
    n = len(v)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if v[j+1] < v[j]:
                v[j], v[j+1] = v[j+1], v[j]
        

        
        
"""""2º Validación de los algoritmos por usando funcion assert"""""

"Lista de listas de numeros para hacer pruebas"
tests = [[-9,4,13,-1,-5],[6,-3,-15,5,4,5,2],[13,4],
         [9],[7,6,6,5,4,3,2,1],[1,2,3,4,4,5,6,7],[],[0,0,0,0]]

"Lista de las soluciones esperadas de las anteriores listas"
validas=[[-9,-5,-1,4,13],[-15,-3,2,4,5,5,6],[4,13],
         [9],[1,2,3,4,5,6,6,7],[1,2,3,4,4,5,6,7],[],[0,0,0,0]]

"Tamaños de las listas aleatorias"

sizes = [5,10,15]
def test(tests, funcs, validas, sizes):
    for size in sizes:
        array = list(randint(-10,10,size))
        # Añade a tests una lista generada aleatoriamente de tamaño size
        tests.append(array)
        # Ordena el array con la funcion sort de python y la añade a validas
        array.sort();validas.append(array)
    for tupla in zip(tests, validas):
        # Comprueba si el valor de tests coincide con validas despues de
        # aplicar cada una de las dos funciones
            for func in funcs:
               assert func(tupla[0]) != tupla[1],'''{}
               no funcionó correctamente'''.format(func._name_)
    print("Ambos algoritmos han pasado el test correctamente")

test(tests,[insertionSort,bubbleSort],validas,sizes)


"""""3º Determinar los tiempos de ejecución para"""""
#Convierte a nanosegundos
def perfcounter_ns():
    return time.perf_counter() * (10**9)


def secuencia(size,orden):
    # Crea el vector v que puede ser ordneado ascendentemente, ordenado 
    # descendentemente y vector aleatorio 
    v=[]
    if orden =="up":
        for i in range(1,size+1):
            v.append(i)
        return v
    elif orden =="down":
        for i in range(size):
            v.append(size-i)
        return v
    elif orden =="random":
        v=list(randint(-10,10,size))
        return v

def calculo_tiempos(funcion,enesimos,tipo,orden,inf,ajus,sup,cte):
    tabla = PrettyTable(['n','t(n)', 't(n)/{}  Ω'.format(inf[0]),
                          't(n)/{}  Θ'.format(ajus[0]),
                          't(n)/{}  O'.format(sup[0])])
    tabla.float_format = '.3'
    b=[]
    for a in enesimos:
        bucle=False
        t1 = perfcounter_ns()
        v=tipo(a,orden)
        funcion(v)
        t2 = perfcounter_ns()
        
        if t2 - t1 > 500000:
            tiempo = t2 - t1
        else: 
            bucle=True
            # Mediciones de tiempos pequeños por medio de repeticion de k veces
            # del algoritmo
            t1 = perfcounter_ns()
            K = 1000
            for i in range(0, K):
                v=tipo(a,orden)
                funcion(v)
            t2 = perfcounter_ns()
            tiempo = (t2 - t1)/ K
        if bucle:
            tabla.add_row([a, str(tiempo)+'*', tiempo/inf[1](a), 
                           tiempo/ajus[1](a), tiempo/sup[1](a)])
            b.append(tiempo/ajus[1](a))
        else:
            tabla.add_row([a,tiempo, tiempo/inf[1](a), tiempo/ajus[1](a),
                           tiempo/sup[1](a)])
            b.append(tiempo/ajus[1](a))
    cte.append(b)
    
    return tabla
if __name__ == '__main__':
    seed(123)
    "4º Comprobacion empírica de los resultados"
    ### Cotas de las funciones ###
    
    # Algoritmo Insertion aleatorio:
    inf_in_r = ['n*log(n)', lambda n:n*math.log(n)]
    ajus_in_r=['n^2',lambda n:n**2]
    sup_in_r = ['n^2.2', lambda n:(n)**2.2]
    
    # Algoritmo Insertion Ordenado:
    inf_in_a = ['log(n)', lambda n:math.log(n)]
    ajus_in_a=['n',lambda n:(n)]
    sup_in_a = ['n^1.25', lambda n:(n)**1.25]
    
    
    # Algoritmo Insertion Orden Inverso:
    inf_in_d = ['n*1.8', lambda n:n*1.8]
    ajus_in_d=['n^2',lambda n:(n)**2]
    sup_in_d = ['n^2.2', lambda n:(n)**2.2]
    
   #####################################################################
    
    # Algoritmo bubbleSort aleatorio:
    inf_bubble_r = ['n', lambda n:n]
    ajus_bubble_r=['n*log(n)',lambda n:(n)*math.log(n)]
    sup_bubble_r = ['n^1.8', lambda n:(n)**1.8]
    
    # Algoritmo bubbleSort Ascendente:
    inf_bubble_a = ['n', lambda n:math.log(n)]
    ajus_bubble_a=['n*log(n)',lambda n:(n)*math.log(n)]
    sup_bubble_a = ['n^1.8', lambda n:(n)**1.8]
    
    
    # Algoritmo bubbleSort Descendente:
    inf_bubble_d = ['n', lambda n:n]
    ajus_bubble_d=['n*log(n)',lambda n:(n)*math.log(n)]
    sup_bubble_d = ['n^1.8', lambda n:(n)**1.8]
    
    #Tamaño de los operadores
    enesimos=[100,200,400,800,1600,3200]
    cte=[]
    tabla_ins_random = calculo_tiempos(insertionSort, enesimos,secuencia,
                                        "random",inf_in_r, ajus_in_r, sup_in_r,
                                        cte)
    
    tabla_ins_as = calculo_tiempos(insertionSort, enesimos,secuencia,
                                            "up",inf_in_a, ajus_in_a, sup_in_a,
                                            cte)
    tabla_ins_des= calculo_tiempos(insertionSort, enesimos,secuencia,"down",
                                  inf_in_d, ajus_in_d, sup_in_d,cte)
    
    
    print("TODAS LAS MEDICCIONES DE TIEMPO ESTAN EN NANOSEGUNDOS")
    print("")
    print("########### Algoritmo Insertion ###########")
    print('Complejidad del algoritmo insertion aleatorio \n', tabla_ins_random,
          '\n',"CTE =",round(statistics.mean(cte[0]),3))
    print('Complejidad del algoritmos insertion Ordenado \n', tabla_ins_as,
          '\n',"CTE =",round(statistics.mean(cte[1]),3))
    print('Complejidad del algoritmos insertion orden inverso \n',tabla_ins_des,
          '\n',"CTE =",round(statistics.mean(cte[2]),3))
    
    print("")
    print("########### Algoritmo BubbleSort ###########")
    print("")
    
    tabla_bubble_random = calculo_tiempos(bubbleSort, enesimos,secuencia,"random",
                                  inf_bubble_r, ajus_bubble_r, sup_bubble_r,cte)
    tabla_bubble_as = calculo_tiempos(bubbleSort, enesimos,secuencia,"up",
                                  inf_bubble_a, ajus_bubble_a, sup_bubble_a,cte)
    tabla_bubble_des = calculo_tiempos(bubbleSort, enesimos,secuencia,"down",
                                  inf_bubble_d, ajus_bubble_d, sup_bubble_d,cte)
    
    print("TODAS LAS MEDICCIONES DE TIEMPO ESTAN EN NANOSEGUNDOS")
    print('Complejidad del algoritmo bubbleSort aleatorio \n', tabla_bubble_random,
          '\n',"CTE =",round(statistics.mean(cte[3]),3))
    print('Complejidad del algoritmos bubbleSort ordenado \n', tabla_bubble_as,
          '\n',"CTE =",round(statistics.mean(cte[4]),3))
    print('Complejidad del algoritmos bubbleSort orden inverso \n',
    tabla_bubble_des,'\n',"CTE =",round(statistics.mean(cte[5]),3))