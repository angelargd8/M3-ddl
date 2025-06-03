from collections import deque, defaultdict
from typing import Dict, Set


class AFD:
    def __init__(self):
        self.estados: Set[int] = set()
        self.alfabeto: Set[str] = set()
        self.estado_inicial: int = None
        self.estados_finales: Set[int] = set()
        self.transiciones: Dict[int, Dict[str, int]] = defaultdict(dict)

    def agregar_transiciones(
        self, estado_origen: int, simbolo: str, estado_destino: int
    ):
        self.transiciones[estado_origen][simbolo] = estado_destino

    def agregar_estado_inicial(self, estado: int):
        self.estado_inicial = estado

    def agregar_estado_final(self, estado: int):
        self.estados_finales.add(estado)

    def mostrar(self):
        print("Estados:", self.estados)
        print("Alfabeto:", self.alfabeto)
        print("Estado inicial:", self.estado_inicial)
        print("Estados finales:", self.estados_finales)
        print("Transiciones:")
        for estado_origen, trans in self.transiciones.items():
            for simbolo, estado_destino in trans.items():
                print(f"{estado_origen} -> {estado_destino} [simbolo: {simbolo}]")
        print("---" * 15)

    def __str__(self):
        return (
            f"AFD(estados={self.estados}, alfabeto={self.alfabeto}, "
            f"estado_inicial={self.estado_inicial}, estados_finales={self.estados_finales}, "
            f"transiciones={self.transiciones})"
        )



def mapear_posiciones_simbolos(nodo, posicion_a_simbolo):
    # si el nodo es None, terminar la función y retornar
    if nodo is None:
        return

    # verificar si el nodo es una hoja o un simbolo, este tiene un id unico
    if (nodo.left is None and nodo.right is None) or nodo.value not in [
        ".",
        "*",
        "+",
        "|",
        "^",
    ]:
        posicion_a_simbolo[nodo.id] = nodo.value

    # recorrer subarboles
    mapear_posiciones_simbolos(nodo.left, posicion_a_simbolo)
    mapear_posiciones_simbolos(nodo.right, posicion_a_simbolo)


def procesar_escapado(cadena):
    especiales = "+*|()[]?'#."

    if cadena[-1] not in especiales:
        return cadena
    else:
        resultado = ""
        i = 0

        while i < len(cadena):
            if cadena[i] == "\\" and i + 1 < len(cadena) and cadena[i + 1] in especiales:
                resultado += cadena[i + 1]  # Agrega solo el carácter especial sin el '\'
                i += 2  # Salta ambos caracteres
            else:
                resultado += cadena[i]
                i += 1

        return resultado



def construir_AFD(arbolSintactico, followpos):

    if arbolSintactico:

        # 1 . instanciar AFD
        afd = AFD()


    # 1. Mapear posiciones a símbolos
    posicion_a_simbolo = {}
    mapear_posiciones_simbolos(arbolSintactico, posicion_a_simbolo)

    # 2. Alfabeto sin operadores especiales
    alfabeto = set()
    for simbolo in posicion_a_simbolo.values():
        if not simbolo.startswith("#") and not (
                simbolo.startswith("@") and simbolo.endswith("@") and simbolo[1:-1].isdigit()
        ):
            alfabeto.add(simbolo)

    afd.alfabeto = alfabeto
    # print("---ALFABETO---")
    # print(afd.alfabeto)

    # 3. Estado inicial: conjunto firstpos de la raíz
    estado_inicial = frozenset(arbolSintactico.firstpos)
    estados_dict = {estado_inicial: 0}
    estado_id_a_conjunto = {0: set(estado_inicial)}
    afd.estados.add(0)
    afd.estado_inicial = 0

    no_marcados = [estado_inicial]
    id_counter = 1

    # 4. Buscar la posición del símbolo final '#' (aunque no es necesario si usamos etiquetas como #num)
    while no_marcados:
        estado_actual = no_marcados.pop(0)
        id_actual = estados_dict[estado_actual]

        for simbolo in afd.alfabeto:
            posiciones_simbolo = {
                pos for pos in estado_actual if posicion_a_simbolo.get(pos) == simbolo
            }

            if posiciones_simbolo:
                nuevo_estado = set()
                for pos in posiciones_simbolo:
                    nuevo_estado.update(followpos[pos])
                nuevo_estado_frozen = frozenset(nuevo_estado)

                if nuevo_estado_frozen not in estados_dict:
                    estados_dict[nuevo_estado_frozen] = id_counter
                    estado_id_a_conjunto[id_counter] = nuevo_estado
                    afd.estados.add(id_counter)
                    no_marcados.append(nuevo_estado_frozen)
                    id_counter += 1

                afd.agregar_transiciones(
                    id_actual, procesar_escapado(simbolo), estados_dict[nuevo_estado_frozen]
                )

    return afd, estados_dict, estado_id_a_conjunto


def minimizar_AFD(afd):
    # 1. Inicializar partición con estados finales y no finales
    particion = [set(afd.estados_finales), set(afd.estados) - set(afd.estados_finales)]
    nueva_particion = []

    while nueva_particion != particion:
        if nueva_particion:
            particion = nueva_particion
        nueva_particion = []

        for grupo in particion:
            subgrupos = defaultdict(set)

            for estado in grupo:
                # Clave única para identificar cómo el estado se comporta con cada símbolo
                clave = tuple(
                    (
                        simbolo,
                        frozenset(
                            encontrar_grupo(
                                afd.transiciones.get(estado, {}).get(simbolo), particion
                            )
                            or {}
                        ),
                    )
                    for simbolo in afd.alfabeto
                )
                subgrupos[clave].add(estado)

            nueva_particion.extend(subgrupos.values())

    # 2. Crear nuevo AFD minimizado
    nuevo_afd = AFD()
    representantes = {next(iter(grupo)): grupo for grupo in nueva_particion if grupo}

    for representante, grupo in representantes.items():
        nuevo_afd.estados.append(representante)

        if representante in afd.estados_finales:
            nuevo_afd.agregar_estado_final(representante)

        if representante == afd.estado_inicial:
            nuevo_afd.agregar_estado_inicial(representante)

        for simbolo in afd.alfabeto:
            destino = afd.transiciones.get(representante, {}).get(simbolo)
            if destino is not None:
                grupo_destino = encontrar_grupo(destino, nueva_particion)
                if grupo_destino:
                    destino_representante = next(iter(grupo_destino), None)
                    if destino_representante is not None:
                        nuevo_afd.agregar_transiciones(
                            representante, simbolo, destino_representante
                        )

    nuevo_afd.alfabeto = afd.alfabeto
    return nuevo_afd


def encontrar_grupo(estado, particion):
    """Encuentra a qué grupo pertenece un estado en la partición"""
    if estado is None:
        return None
    for grupo in particion:
        if estado in grupo:
            return grupo
    return None
