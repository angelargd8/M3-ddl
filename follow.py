from collections import defaultdict
from first import IsTerminal, calcularFirst, diccionarioGramatica, tokenizeProduccion


follows = defaultdict(set)


def calcularFollow(gramatica: str, firsts: dict) -> dict:
    global diccionarioProducciones
    diccionarioProducciones = diccionarioGramatica(gramatica)

    # Inicializar FOLLOW con símbolo inicial
    simbolo_inicial = list(diccionarioProducciones.keys())[0]
    follows[simbolo_inicial].add("$")

    cambiado = True
    while cambiado:
        cambiado = False
        for A in diccionarioProducciones:
            for produccion in diccionarioProducciones[A]:
                simbolos = tokenizeProduccion(produccion)
                for i in range(len(simbolos)):
                    B = simbolos[i]
                    if not IsTerminal(B):
                        primero_de_beta = set()
                        epsilon_en_beta = False

                        if i + 1 < len(simbolos):
                            beta = simbolos[i + 1 :]
                            for simbolo_beta in beta:
                                if IsTerminal(simbolo_beta):
                                    primero_de_beta.add(simbolo_beta)
                                    break
                                primero = firsts[simbolo_beta]
                                primero_de_beta.update(primero - {"ε"})
                                if "ε" in primero:
                                    continue
                                break
                            else:
                                epsilon_en_beta = True
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
