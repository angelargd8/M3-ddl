from collections import defaultdict
from GrammarProcesor.First import IsTerminal

"""
El conjunto FOLLOW se usa para saber que tokens pueden venir luego de un simbolo no terminal
en cualquier derivacion valida

Sirve para saber cuando se debe de aplicar una produccion derivada de epsolin
y para construir la tabla de parsing LL(1) 
"""

follows = defaultdict(set)


def calcularFollow(producciones: dict, firsts: dict) -> dict:
    # global diccionarioProducciones
    # diccionarioProducciones = diccionarioForFolow(gramatica)

    # Inicializar FOLLOW con símbolo inicial
    simbolo_inicial = list(producciones.keys())[0]
    follows[simbolo_inicial].add("$")

    cambiado = True
    while cambiado:
        cambiado = False
        for A in producciones:
            for produccion in producciones[A]:
                simbolos = produccion
                for i in range(len(simbolos)):
                    B = simbolos[i]
                    if not IsTerminal(B,producciones):

                        # B está al final: FOLLOW(A) ⊆ FOLLOW(B)
                        if i == len(simbolos) - 1:
                            tam_antes = len(follows[B])
                            follows[B].update(follows[A])
                            if len(follows[B]) > tam_antes:
                                cambiado = True
                            continue  # no hay β que procesar

                        #  A → αBβ y ε ∈ FIRST(β)
                        primero_de_beta = set()
                        epsilon_en_beta = False

                        beta = simbolos[i + 1 :]
                        for simbolo_beta in beta:
                            if IsTerminal(simbolo_beta,producciones):
                                primero_de_beta.add(simbolo_beta)
                                break
                            primero = firsts[simbolo_beta]
                            primero_de_beta.update(primero - {"ε"})
                            if "ε" in primero:
                                continue
                            break
                        else:
                            epsilon_en_beta = True

                        tam_antes = len(follows[B])
                        follows[B].update(primero_de_beta)
                        if epsilon_en_beta:
                            follows[B].update(follows[A])
                        if len(follows[B]) > tam_antes:
                            cambiado = True

    # Imprimir resultados
    print("\nTabla de FOLLOW:")
    print("===================================")
    for no_terminal in follows:
        print(f"FOLLOW({no_terminal}) = {follows[no_terminal]}")
    return follows
