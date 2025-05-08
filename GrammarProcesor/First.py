from collections import defaultdict
from typing import List, Tuple
from constructor import *


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


def IsTerminal(simbolo: str) -> bool:

    if simbolo in diccionarioProducciones:
        return False #es un no terminal porque tiene producciones
    
    # Definir los terminales y no terminales
    terminales = ["*", "(", ")", "{", "}", "[", "]", "|", "+", "?", "ε"]
    return simbolo.islower() or simbolo == "ε" or simbolo in terminales


def calcularFirst(simbolo: str) -> set:
    # print("===================================")
    # print("Calculando FIRST de: " + str(simbolo) )

    if IsTerminal(simbolo):
        # print("Es terminal " + str(simbolo) )
        # return simbolo
        return set([simbolo])

    if simbolo in firsts and firsts[simbolo]:
        # print("Ya calculado FIRST de: " + str(simbolo) )
        return firsts[simbolo]

    for prod in diccionarioProducciones[simbolo]:
        # print("Produccion: " + str(prod) )
        produccion = tokenizeProduccion(prod)
        # print("Produccion tokenizada: " + str(produccion) )
        i = 0
        while i < len(produccion):
            simbolo_actual = produccion[i]
            # print("Simbolo actual: " + str(simbolo_actual) )
            # print("Simbolo actual: " + str(simbolo_actual) )

            if simbolo_actual == simbolo:
                break # evitar bucle infinito

            #para evitar el bucle infinito
            if simbolo_actual not in diccionarioProducciones:
                #es un terminal no reconocido como id, o simbolo mal definido
                firsts[simbolo].add(simbolo_actual)
                break


            if IsTerminal(simbolo_actual):
                firsts[simbolo].add(simbolo_actual)
                break

            firsts[simbolo].update(calcularFirst(simbolo_actual))

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


def First(gramatica: str) -> dict:
    global diccionarioProducciones
    diccionarioProducciones = diccionarioGramatica(gramatica)

    for no_terminal in diccionarioProducciones:

        calcularFirst(no_terminal)

    print("\nTabla de FIRST:")
    print("===================================")
    for no_terminal in firsts:
        print(f"FIRST({no_terminal}) = {firsts[no_terminal]}")

    return firsts
