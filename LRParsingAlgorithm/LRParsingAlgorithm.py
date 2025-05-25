"""
-- LR-Parsing Algorithm--

tomar de entrada el conjunto canonico de items LR0
y se va a transformar en una estructura de datos, para simular el algoritmo de parsing
se usa una pila para simular el automata de pila
va a consumir token tras token 
consume token tras token y usa la pila y consulta la table slr para determinar la accion que debe de tomar el analizador
la tabla slr accion|goto
la salida es si: si la secuencia de tokens que tenemos en la entrada construye una oracion valida a partir de de la gramatica libre de contexto
la salida es no: si tenemos errores sintacticos, es cuando la tabla slr no se capaz de decirnos que hacer
al tener la tabla slr, se usa el algoritmo de LR parsing program y alli es cuando dice si la oracion que estoy parseando es valida o no

Algoritmo de LR parsing program

let a be the first symbol of w$;
while (1){ /*repeat forever*/
    let s be the state on top of the stack;
    if (ACTION[s,a] == shift t) {
        push t onto the stack;
        let a be the next input symbol;
    }else if (ACTION[s,a] = reduce A -> β){
        pop |β| symbols off the stack;
        let state t now be on top of the stackl
        push GOTO[t,A] onto the stack;
        output the production A -> β;
    Ejecuta el algoritmo de parsing LR(0) utilizando una tabla SLR(1).
    
    }else if (ACTION[s,a] == accept) break; /* parsing is done*/
    else call error-recovery routine;
    
}

"""

def ejecutarParser(tokens, action, goto, producciones):
    """
    Ejecuta el algoritmo de parsing LR(0) utilizando una tabla SLR(1).
    
    Parámetros:
    - tokens: lista de tokens de entrada (ya incluye '$' al final).
    - action: tabla de acciones (dict estado -> simbolo -> accion).
    - goto: tabla de goto (dict estado -> no_terminal -> estado).
    - producciones: diccionario de producciones {LHS: [[RHS], ...]}.

    Retorna True si la cadena es aceptada, False en caso de error.
    """

    # Preparar la pila e índice de entrada
    stack = [0]
    index = 0
    tokens.append('$')

    # Numerar las producciones para mapear reduce
    producciones_numeradas = []
    for lhs, reglas in producciones.items():
        for regla in reglas:
            producciones_numeradas.append((lhs, regla))

    print("\n--- Inicio del Parsing ---")
    print(f"Tokens de entrada: {tokens}")

    while True:
        estado_actual = stack[-1]
        simbolo_actual = tokens[index]

        accion = action.get(estado_actual, {}).get(simbolo_actual)

        if not accion:
            print(f"Error sintáctico: no hay acción definida para estado {estado_actual} con símbolo '{simbolo_actual}'")
            return False

        print(f"---[Estado {estado_actual}] Acción: {accion} con símbolo '{simbolo_actual}'")

        if accion.startswith('s'):
            nuevo_estado = int(accion[1:])
            stack.append(nuevo_estado)
            index += 1
            print(f"→ Shift a estado {nuevo_estado}")

        elif accion.startswith('r'):
            num = int(accion[1:])
            lhs, rhs = producciones_numeradas[num]
            for _ in rhs:
                stack.pop()
            estado_actual = stack[-1]
            goto_estado = goto[estado_actual][lhs]
            stack.append(goto_estado)
            print(f"← Reduce usando producción: {lhs} → {' '.join(rhs)}")
            print(f"→ Ir al estado {goto_estado} (goto)")

        elif accion == 'acc':
            print("Cadena aceptada por el analizador sintáctico.")
            return True

        else:
            print(f"Acción inválida: {accion}")
            return False
