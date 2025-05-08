from collections import defaultdict
from typing import List, Tuple
from constructor import *


"""
El conjunto FIRST sirve para saber que tokens pueden aparecer
al inicio de una cadena derivada desde un simbolo terminal o no terminal

Sirve para construir la tabla de parsing y decidir que produccion usar cuando se lee un token

"""

producciones = defaultdict(set)
firsts = defaultdict(set)


def tokenizeProduccion(simbolo: str) -> List[str]:
    tokens = []
    i = 0
    while i < len(simbolo):

        #  Terminal
        if simbolo[i].islower():
            buffer = simbolo[i]
            i += 1
            while i < len(simbolo) and simbolo[i].islower():
                buffer += simbolo[i]
                i += 1
            tokens.append(buffer)

        # No terminales
        elif simbolo[i].isupper():
            buffer = simbolo[i]
            i += 1

            # si tiene una comilla
            while i < len(simbolo) and simbolo[i] == "'":
                buffer += simbolo[i]
                i += 1
            tokens.append(buffer)
        elif simbolo[i] == "'":

            # por si hay una comilla sola
            tokens.append("'")
            i += 1
        else:
            tokens.append(simbolo[i])
            i += 1
    return tokens


def IsTerminal(simbolo: str, producciones: dict) -> bool:
    # # Definir los terminales y no terminales
    return simbolo not in producciones and simbolo != "ε" 

def calcularFirst(simbolo: str, producciones: dict) -> set:
    # print("===================================")
    # print("Calculando FIRST de: " + str(simbolo) )

    if IsTerminal(simbolo, producciones):
        print("Es terminal " + str(simbolo) )
        return set([simbolo])

    if simbolo in firsts and firsts[simbolo]:
        # print("Ya calculado FIRST de: " + str(simbolo) )
        return firsts[simbolo]

    for produccion in producciones[simbolo]:
        # print("Produccion: " + str(produccion) )
        i = 0
        while i < len(produccion):
            simbolo_actual = produccion[i]
            # print("Simbolo actual: " + str(simbolo_actual) )

            if simbolo_actual == simbolo:
                break # evitar bucle infinito

            #calcular el first del simbolo actual 
            first_actual = calcularFirst(simbolo_actual, producciones)

            firsts[simbolo].update(first_actual - {"ε"}) #agregar el first al conjunto de firsts del simbolo            

            if "ε" not in firsts[simbolo]:
                break

            i += 1
        else:
            firsts[simbolo].add("ε")
    return firsts[simbolo]


# poner los elementos en eun diccionario
def diccionarioGramatica(gramatica: str) -> dict:
    producciones = defaultdict(set)
    for produccion in reversed(gramatica):
        no_terminal, expansion = produccion.split("->")
        # producciones[no_terminal].add(expansion)
        partes = expansion.split("|")
        for parte in partes:
            producciones[no_terminal].add(parte)

    print("Producciones:")
    for no_terminal, expansions in producciones.items():
        print(f"{no_terminal} -> {', '.join(expansions)}")
    return producciones


def diccionarioForFolow(gramatica: str) -> dict:
    producciones = defaultdict(set)
    for produccion in gramatica:
        no_terminal, expansion = produccion.split("->")
        # producciones[no_terminal].add(expansion)
        partes = expansion.split("|")
        for parte in partes:
            producciones[no_terminal].add(parte)

    print("Producciones:")
    for no_terminal, expansions in producciones.items():
        print(f"{no_terminal} -> {', '.join(expansions)}")
    return producciones


def First(producciones: str) -> dict:
    # global diccionarioProducciones
    # diccionarioProducciones = diccionarioGramatica(gramatica)

    for no_terminal in producciones:
        calcularFirst(no_terminal, producciones)

    print("\nTabla de FIRST:")
    print("===================================")
    for no_terminal in firsts:
        print(f"FIRST({no_terminal}) = {firsts[no_terminal]}")

    return firsts
