from GrammarProcesor.First import *
from GrammarProcesor.Follow import *
from AutomatonBuilder.ConstruirAutomata import *
from AutomatonBuilder.grafico import *
from LRParsingAlgorithm.LRParsingAlgorithm import *

from LRParsingAlgorithm.TablaSLR import *


from Yalex.lexicalAnalizer import get_pickle_automata
from Yalex.yalReader import yalReader
from Yalex.generator import generar_afd_unificado, _serialize_automata
from Yalex.constructor_yalex import leerArchivo_yalex
from constructor import leerYapar, leerExpresiones

import threading
import queue
from typing import List

# Token especial para indicar fin de la producción
FIN = "FIN_TOKEN"

# ------------------- Productor -------------------
def productor(texto: str, automata, ignorados, token_queue):
    tokens = simular_texto(texto, automata)
    for lexema, token in tokens:
        if token not in ignorados:
            token_queue.put(token)  # Encolar solo si no está ignorado
    # Señal de fin
    token_queue.put('$')

# ------------------- Consumidor -------------------
def consumidor(action, goto, producciones, token_queue):
    stack = [0]
    tokens = []

    # Numerar producciones
    producciones_numeradas = [(lhs, rhs) for lhs in producciones for rhs in producciones[lhs]]

    # print("\n--- Inicio del Parsing (Consumidor) ---")
    while True:
        token = token_queue.get()
        if token == FIN:
            token = '$'
            tokens.append(token)
        else:
            tokens.append(token)

        while True:
            estado_actual = stack[-1]
            simbolo_actual = tokens[0]
            accion = action.get(estado_actual, {}).get(simbolo_actual)
            if not accion:
                print(f"\n✖ Error en estado {estado_actual} con símbolo '{{simbolo_actual}}'")
                return
            if accion.startswith('s'):
                stack.append(int(accion[1:]))
                tokens.pop(0)
                break
            elif accion.startswith('r'):
                num = int(accion[1:])
                lhs, rhs = producciones_numeradas[num]
                for _ in rhs:
                    stack.pop()
                goto_estado = goto.get(stack[-1], {}).get(lhs)
                if goto_estado is None:
                    print("✖ Error en GOTO")
                    return
                stack.append(goto_estado)
            elif accion == 'acc':
                print("✔ Cadena aceptada")
                return
            else:
                print("✖ Acción inválida")
                return

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


    opcion = int(input("1) Cargar Pickle \n2) Leer yal nuevo\n"))
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
        if not contenido_yal:
            print("No se pudo leer el archivo yal")
            return
        
        yal = yalReader(contenido_yal)
        tokens = yal.get_tokens()
        ignore = yal.get_ignore()

        if "WHITESPACE" in tokens and "WS" not in tokens:
            tokens["WS"] = tokens.pop("WHITESPACE")
            ignore = ["WS" if x == "WHITESPACE" else x for x in ignore]

        lexical_automata = generar_afd_unificado(tokens)
        _serialize_automata(lexical_automata, "lexical_out")

    archivo = "./yapar/slr-2.yalp"
    tokens, producciones, ignorados_yalp = leerYapar(archivo)
    ignorados = list(set(ignore + ignorados_yalp))

    print("\n==== TOKENS IGNORADOS====")
    print(ignorados)

    print("\n==== TOKENS ====")
    print(tokens)

    no_terminales = list(producciones.keys())
    terminales = sorted(set(tokens))  #tokens que no son terminales

    #---grammar procesor--
    # calcularFirst
    first = First(producciones)

    # calcularFollow
    follow = calcularFollow(producciones, first)

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

    expresiones = leerExpresiones("./input/prueba.txt")

    for i, expr in enumerate(expresiones):
        # print(f"\n========== Analizando expresion {i+1}: {expr}")
        token_queue = queue.Queue()
        hilo_p = threading.Thread(target=productor, args=(expr, lexical_automata, ignorados, token_queue))
        hilo_c = threading.Thread(target=consumidor, args=(action, goto, producciones, token_queue))
        hilo_p.start()
        hilo_c.start()
        hilo_p.join()
        hilo_c.join()

main()

