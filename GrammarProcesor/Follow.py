from collections import defaultdict
from GrammarProcesor.First import IsTerminal

"""
El conjunto FOLLOW se usa para saber que tokens pueden venir luego de un simbolo no terminal
en cualquier derivacion valida

Sirve para saber cuando se debe de aplicar una produccion derivada de epsolin
y para construir la tabla de parsing LL(1) 
"""




def calcularFollow(producciones: dict, firsts: dict) -> dict:
    # global diccionarioProducciones
    # diccionarioProducciones = diccionarioForFolow(gramatica)

    follows = defaultdict(set)

    # Inicializar FOLLOW con símbolo inicial
    simbolo_inicial = list(producciones.keys())[0]
    follows[simbolo_inicial].add("$")

    cambiado = True
    while cambiado:
        cambiado = False
        for A in producciones:
            for produccion in producciones[A]:
                simbolos = produccion
                for i, B in enumerate(simbolos):
                    if not IsTerminal(B, producciones):
                        beta = simbolos[i + 1:]

                        primero_de_beta = set()
                        epsilon_en_beta = True  # se asume que puede derivar ε

                        for simbolo in beta:
                            if IsTerminal(simbolo, producciones):
                                primero_de_beta.add(simbolo)
                                epsilon_en_beta = False
                                break
                            else:
                                primero = firsts[simbolo]
                                primero_de_beta.update(primero - {"ε"})
                                if "ε" not in primero:
                                    epsilon_en_beta = False
                                    break

                        tam_antes = len(follows[B])
                        follows[B].update(primero_de_beta)

                        if epsilon_en_beta or not beta:
                            follows[B].update(follows[A])

                        if len(follows[B]) > tam_antes:
                            cambiado = True

    # Imprimir resultados
    print("\nTabla de FOLLOW:")
    print("===================================")
    for no_terminal in follows:
        print(f"FOLLOW({no_terminal}) = {follows[no_terminal]}")
    return follows
