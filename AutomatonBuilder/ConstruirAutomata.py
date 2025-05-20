from AutomatonBuilder.Closure import *
from AutomatonBuilder.Goto import *

"""

ejemplo de la clase:
void items(G'){
    C = { Clousure(I0) }
    repeat
        for each set of items in C:
        for each grammar symbol X:
            if goto(I, X) is not empty and not in C:
                add goto(I, X) to C
    until no new items are addes to C on a round

}

"""

def ConstruirAutomata(producciones: dict) -> dict:

    estados = []  # Lista para almacenar
    estados_id = {}  # Diccionario para almacenar los estados y sus IDs
    transiciones = {}  # Diccionario para almacenar transiciones

    #-construir items LR(0)--
    # 1. calculo de closure(I) del item

    #-crear el item inicial 
    simbolo_inicial = list(producciones.keys())[0]  # Obtiene el primer símbolo no terminal
    simbolo_aumentado = simbolo_inicial + "'"  # Aumenta el símbolo inicial
    # print(f"Simbolo inicial: {simbolo_inicial}")
    #  
    #crear produccion aumentada
    producciones[simbolo_aumentado] = [[simbolo_inicial]]  # Agrega la producción aumentada al diccionario

    I0 = { (simbolo_aumentado, (simbolo_inicial,), 0) } # Inicializa el conjunto de items
    I0 = Closure(I0, producciones)
    print("\n//// Items LR(0) ////")
    imprimir_items(I0)

    

    # 2. calculo de goto(I,X)
    print(f"\n//// -- goto -- ////")
    estados.append(I0)
    pendientes = [I0]  # Lista de conjuntos de items pendientes
    estados_id[id(I0)] = 0

    estado_aceptacion = None

    # repeat
    # for each set of items in C:
    #    for each grammar symbol X:
    #       if goto(I, X) is not empty and not in C:
    #           add goto(I, X) to C
    # until no new items are addes to C on a round

    while pendientes:
        I = pendientes.pop(0)
        # print(f"\nConjunto de items pendiente: {I}")

        # estado de aceptacion  
        for item in I:
            nt, cuerpo, punto = item
            if nt == simbolo_aumentado and punto == len(cuerpo):
                estado_sum = estados_id.get(id(I), '?')
                estado_aceptacion = id(I)
                # print(f"/// Estado de aceptación: q{estado_sum} ///")
                # print(f"Producción: {nt} → {' '.join(cuerpo)}")


        for simbolo_gramatical in obtener_simbolos_gramaticales(producciones):
            # print(f"Simbolo: {simbolo_gramatical}")
            goto_result = goto(I, simbolo_gramatical, producciones)
            # print(f"goto_result: {goto_result}")


            if goto_result:
                existente = encontrar_estado_id_por_contenido(estados, goto_result)

                if existente is None:
                    estados.append(goto_result)  # Agrega el nuevo estado a la lista de estados
                    nuevo_id = len(estados) - 1  # Asigna un ID al nuevo estado
                    estados_id[id(goto_result)] = nuevo_id  # Asigna el ID al nuevo estado
                    pendientes.append(goto_result)  # Agrega el nuevo estado a la lista de pendientes
                    destino_id = id(goto_result) 
                else: 
                    destino_id = id(estados[existente])
                
                transiciones[(id(I), simbolo_gramatical)] = destino_id  # Agrega la transición al diccionario de transiciones

    print("\n===== ESTADOS LR(0) =====")
    for i, estado in enumerate(estados):
        print(f"\nEstado {i}:")
        imprimir_items(estado)

    print("\n====== TRANSICIONES ======")
    for (origen_id, simbolo), destino_id in transiciones.items():
        origen_num = estados_id.get(origen_id, '?')
        destino_num = estados_id.get(destino_id, '?')
        print(f"δ (q{origen_num}, '{simbolo}') → q{destino_num}")

    print(f"\nEstado de aceptación: q{estados_id[estado_aceptacion]}")
    print(f"Producción: {simbolo_aumentado} → {' '.join(producciones[simbolo_aumentado][0])}")

    
    return estados, transiciones, estados_id, estado_aceptacion, simbolo_aumentado
           

def encontrar_estado_id_por_contenido(estados, estado_nuevo):
    for i, estado in enumerate(estados):
        if estado == estado_nuevo:
            return i
    return None


def obtener_simbolos_gramaticales(producciones: dict) -> set:
    """
    Obtiene los símbolos gramaticales de las producciones.

    Args:
        producciones (dict): Diccionario de producciones.

    Returns:
        set: Conjunto de símbolos gramaticales.
    """
    simbolos = set()
    for nt, reglas in producciones.items():
        simbolos.add(nt) # Agrega el no terminal

        for cuerpo in reglas:
            simbolos.update(cuerpo)  # Agrega los símbolos del cuerpo de la producción 
    
    return sorted(simbolos)