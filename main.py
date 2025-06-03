from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *
from AutomatonBuilder.ConstruirAutomata import *
from AutomatonBuilder.grafico import *
from LRParsingAlgorithm.LRParsingAlgorithm import *

from LRParsingAlgorithm.TablaSLR import *


from Yalex.lexicalAnalizer import get_pickle_automata
from Yalex.yalReader import yalReader
from Yalex.generator import generar_afd_unificado, _serialize_automata
from Yalex.constructor_yalex import leerArchivo_yalex

import threading
import queue
from typing import List

# Cola compartida entre productor y consumidor
token_queue = queue.Queue()

# Token especial para indicar fin de la producción
FIN = "FIN_TOKEN"


# ------------------- Productor -------------------
def productor(texto: str, automata, ignorados):
    tokenizado_tx = simular_texto(texto, automata)

    for lexema, token in tokenizado_tx:
        if token not in ignorados:
            token_queue.put(token)  # Encolar solo si no está ignorado
        else:
            pass
            # print(f"Ignorando token: '{lexema}' -> {token}")

    # Señal de fin
    token_queue.put('$')


# ------------------- Consumidor -------------------
def consumidor(action, goto, producciones):
    stack = [0]
    tokens = []

    # Numerar producciones
    producciones_numeradas = []
    for lhs, reglas in producciones.items():
        for regla in reglas:
            producciones_numeradas.append((lhs, regla))

    print("\n--- Inicio del Parsing (Consumidor) ---")

    while True:
        token = token_queue.get()
        if token == FIN:
            token = '$'  # Añadir EOF
            tokens.append(token)
        else:
            tokens.append(token)

        while True:
            estado_actual = stack[-1]
            simbolo_actual = tokens[0]

            accion = action.get(estado_actual, {}).get(simbolo_actual)
            if not accion:
                print("\n------- Error sintáctico:")
                print(f"   → Estado actual: {estado_actual}")
                print(f"   → Símbolo encontrado: '{simbolo_actual}'")
                print(f"   → No hay acción definida en la tabla de parsing.")
                return False

            print(f"--- [Estado {estado_actual}] Acción: {accion} con símbolo '{simbolo_actual}'")

            if accion.startswith('s'):
                nuevo_estado = int(accion[1:])
                print(f"✔ Shift: '{simbolo_actual}' → Estado {nuevo_estado}")
                stack.append(nuevo_estado)
                tokens.pop(0)
                break  # Esperar más tokens si es necesario

            elif accion.startswith('r'):
                num = int(accion[1:])
                lhs, rhs = producciones_numeradas[num]
                for _ in rhs:
                    stack.pop()
                estado_actual = stack[-1]
                goto_estado = goto.get(estado_actual, {}).get(lhs)

                if goto_estado is None:
                    print("\n------ Error en GOTO:")
                    print(f"   → Estado actual después del reduce: {estado_actual}")
                    print(f"   → No hay transición GOTO para el símbolo '{lhs}'")
                    return False

                print(f"← Reduce: {lhs} → {' '.join(rhs)}")
                print(f"→ Goto {goto_estado}")
                stack.append(goto_estado)

            elif accion == 'acc':
                print("\n ------------ CADENA ACEPTADA ------------- ")
                return True

            else:
                print("\n-----------Acción inválida detectada:")
                print(f"   → Estado: {estado_actual}")
                print(f"   → Símbolo: '{simbolo_actual}'")
                print(f"   → Acción desconocida: '{accion}'")
                return False


def simular_texto(texto: str, automata) -> List[List[str]]:
    resultados = []
    i = 0

    while i < len(texto):
        estado_actual = automata.afd.estado_inicial
        j = i
        ultimo_estado_final = None
        ultima_pos_final = i
        token_encontrado = None

        while j < len(texto):
            c = texto[j]
            transiciones = automata.afd.transiciones.get(estado_actual, {})
            if c in transiciones:
                estado_actual = transiciones[c]
                j += 1
                if estado_actual in automata.afd.estados_finales:
                    ultimo_estado_final = estado_actual
                    ultima_pos_final = j
                    token_encontrado = automata.estado_a_token.get(estado_actual)
            else:
                break

        if ultimo_estado_final is not None:
            lexema = texto[i:ultima_pos_final]
            resultados.append([lexema, token_encontrado])
            i = ultima_pos_final
        else:
            resultados.append([texto[i], "ERROR"])
            i += 1

    return resultados


def main():


    opcion = int(input(("1) Cargar Pickle \n2) Leer yal nuevo\n")))
    lexical_automata = None
    ignore = []
    if opcion == 1:
        # #  lectura del lexical automata.
        if lexical_automata:
            print("Ya se ha cargado el automata, se va a borrar el anterior")
            lexical_automata = None  # Reiniciar el automata si ya existe
            return
        lexical_automata = get_pickle_automata("./Yalex/out/lexical_out/lexicalAutomata.pkl")
        if lexical_automata:
            pass
        else:
            print("No se pudo encontrar el archivo")
    else:

        contenido_yal = leerArchivo_yalex("yalDocs/slr-2.yal")
        if contenido_yal:
            print(f"\nArchivo Yal leído correctamente\n")

            yal = yalReader(contenido_yal)
            tokens = yal.get_tokens()
            ignore= yal.get_ignore()
            
            if "WHITESPACE" in tokens and "WS" not in tokens:
                tokens["WS"] = tokens.pop("WHITESPACE")
                ignore = ["WS" if x == "WHITESPACE" else x for x in ignore]

            print("[DEBUG] Tokens a ignorar definidos por el .yal:")
            print(ignore)

            print("Tokens detectados:")
            for nombre, expr in tokens.items():
                print(f"  {nombre}: {expr}")


            lexical_automata = generar_afd_unificado(tokens)
            for estado, token in lexical_automata.estado_a_token.items():
                if token == "WHITESPACE":
                    lexical_automata.estado_a_token[estado] = "WS"
                    
            _serialize_automata(lexical_automata, "lexical_out")

    # agregar validacion de archivo y que sean varios xd
    archivo = "./yapar/slr-2.yalp"
    tokens, producciones, ignorados_yalp = leerYapar(archivo)

    print("\n==== TOKENS IGNORADOS====")
    print(ignorados_yalp)

    tokens = [t for t in tokens if t not in ignorados_yalp]

    # termina lectura de tokens
    print("\n==== TOKENS ====")
    print(tokens)

    no_terminales = list(producciones.keys())
    terminales = sorted(set(tokens))  #tokens que no son terminales

    #---grammar procesor--
    # calcularFirst
    first = First(producciones)

    # calcularFollow
    follow = calcularFollow(producciones, first)
    print(follow)

    #-- automaton builder--
    # automata LR(0)
    estados, transiciones, estados_id, estado_aceptacion, simbolo_aumentado = ConstruirAutomata(producciones) 
    graficar_automata(estados, transiciones, estados_id, estado_aceptacion)

    #-- LR-Parsing Algorithm--

    # 1. tabla slr
    action, goto = TablaSLR(producciones, no_terminales, estados, transiciones, estados_id, estado_aceptacion, simbolo_aumentado, follow)

    if estado_aceptacion:
        if '$' not in terminales: 
            terminales.append('$')

    print("\n==================== Tabla SLR (Action | goto) ============================")
    imprimirTablas(action, goto, terminales, no_terminales)

    ignorados = list(set(ignorados_yalp + ignore))

    print("\n==== leyendo archivo... ====")
    t = leerArchivo("./input/prueba.txt")


    for estado, token in lexical_automata.estado_a_token.items():
        if token == "WHITESPACE":
            lexical_automata.estado_a_token[estado] = "WS"

    # print("\n==== TODOS LOS TOKENS A IGNORAR ====")
    # print(ignorados)


    # Crear hilos
    hilo_productor = threading.Thread(target=productor, args=(t, lexical_automata, list(ignorados)))
    hilo_consumidor = threading.Thread(target=consumidor, args=(action, goto, producciones))

    # Iniciar hilos
    hilo_productor.start()
    hilo_consumidor.start()

    # Esperar a que ambos terminen
    hilo_productor.join()
    hilo_consumidor.join()

    tokens_prueba_yalp1 = ["ID", "PLUS", "ID", "TIMES", "LPAREN", "ID", "PLUS", "ID", "RPAREN"]






main()


