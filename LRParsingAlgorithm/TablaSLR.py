"""
Action|Goto
se construye a partir de la gramatica, con el conjunto de items canonicos  LR(0)

action: terminales
goto: no terminales

la interseccion de una fila y una columna , tiene un nombre, dependiendo si la columna es un token o un no terminal, 
es accion si es con un token, o goto si es con un no terminal.

action: shift (S), reduce (r), accept solo en una interseccion(acc), error, cualquier entrada que no tenga una accion definida, cuando se busca de un estado
y esta una celda en blanco

si llego a error, es porque hay un error sintactico, no se puede continuar el analisis

goto: codifica el automata finito LR(0) 
por ejemplo si estamos en el estado 0 y leo una E, entonces voy al estado 1. Si estoy en el estado 0 y leo una t, voy al I2
pero solo esta formada por simbolor no terminales.

Goto(Ii, A) = Ij
Goto[i, A] = j

"""

from collections import defaultdict

action= defaultdict(dict)
goto = defaultdict(dict)



def TablaSLR(producciones, no_terminal,  estados, transiciones, estados_id, estado_aceptacion, simbolo_aumentado, follow):


    # print("\n====== TRANSICIONES ======")
    for (origen_id, simbolo), destino_id in transiciones.items():
        # origen_num = estados_id.get(origen_id, '?')
        # destino_num = estados_id.get(destino_id, '?')
        # print(f"δ (q{origen_num}, '{simbolo}') → q{destino_num}")

        origen = estados_id[origen_id]
        destino = estados_id[destino_id]

        #goto
        if simbolo in no_terminal:
            goto[origen][simbolo] = destino

        #action
        else: 
            # shift, caso a, A → α·aβ
            action[origen][simbolo] = f's{destino}' 
    

    
    producciones_numeradas =[]
    for lhs, reglas in producciones.items():
        for regla in reglas: 
            producciones_numeradas.append((lhs, regla))


    for estado_idx, items in enumerate(estados):

        for nt, cuerpo, punto in items: 
            #punto al final, produccion completa, porque reconocio toda la parte derecha
            if punto == len(cuerpo): 
                #si hay un item con la produccion aumentada convertida en item con el punto al final
                #se tiene que colocar $
                if nt == simbolo_aumentado:

                    action[estado_idx]['$'] = 'acc' #estado de acceptacion

                #simbolo de reducir
                else: 
                    # b. 
                    # buscar el numero de produccion (A → α)

                    #lhs el no terminal actual y el rhs el cuerop de la procuccion completa
                    for num, (lhs, rhs) in enumerate(producciones_numeradas):
                        if lhs == nt and list(cuerpo) == rhs:

                            #recorre el conjunto del follow de no terminal, porque en el parser SLR(1) se reduce por esa produccion
                            #cuando el token actual pertenece al follow del lado izquierdo
                            for simbolo in follow[nt]:
                                if simbolo in action[estado_idx]:
                                    #validacion si ya existe alguna accion para el estado y simvolo, como shift/reduce o reduce/reduce 
                                    print("conflicto de en action[{estado_idx}][{simbolo}] ")
                                else:
                                    action[estado_idx][simbolo] = f'r{num}'

    return action, goto
 


def imprimirTablas(action, goto, terminales, no_terminales):
    # Encabezado
    print("\n")
    # lo esto lo dio nuestro cuarto integrante, gepeto
    header = f"{'STATE':^6}|" + "".join(f"{t:^6}|" for t in terminales) + "||" + "".join(f"{nt:^6}|" for nt in no_terminales)
    
    print(header)
    print("-" * len(header))

    # Filas
    all_states = sorted(set(action.keys()) | set(goto.keys()))
    for state in all_states:
        fila = f"{state:^6}|"
        for t in terminales:
            fila += f"{action.get(state, {}).get(t, ''):^6}|"
        fila += "||"
        for nt in no_terminales:
            fila += f"{goto.get(state, {}).get(nt, ''):^6}|"
        print(fila)