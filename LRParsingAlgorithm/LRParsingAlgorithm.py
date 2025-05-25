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

        print(f"[Estado {estado_actual}] Acción: {accion} con símbolo '{simbolo_actual}'")

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
