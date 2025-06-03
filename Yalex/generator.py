import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from collections import defaultdict
from typing import Dict, List
from dataclasses import dataclass
from Automata.arboles import construirArbolSintactico, imprimirArbolSintactico
from Automata.Regex import infixToPostfix
from Automata.AFD import AFD, construir_AFD
from Automata.Node import calcular_followPos
from Automata.graficadora import visualize_afd
from Automata.AFD import mapear_posiciones_simbolos

import logging

# Configurar logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("afd_generation.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
OUTPUT_DIR = "./Yalex/out"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@dataclass
class LexicalAutomata:
    afd: AFD
    estado_a_token: Dict[int, str]

def normalizar_expresion(expr: str) -> str:
    i = 0
    resultado = ""
    simbols = "+*|()[]?'#."
    if expr[-1] not in simbols:
        while i < len(expr):
            if expr[i] == "\\" and i + 1 < len(expr):
                siguiente = expr[i + 1]
                if siguiente == "n":
                    resultado += "\n"
                elif siguiente == "t":
                    resultado += "\t"
                elif siguiente == "s":
                    resultado += " "

                else:
                    # cualquier otro escape como \+ \* \( \)
                    resultado += siguiente
                i += 2
            else:
                resultado += expr[i]
                i += 1
    else:
        resultado = expr

    return resultado

def generar_afd_unificado(tokens: Dict[str, str]) -> LexicalAutomata:
    expresiones = []
    posicion_a_token = {}
    token_map = {}

    # Generar expresiones con finalizador único usando #idx
    for idx, (nombre_token, expresion) in enumerate(tokens.items()):
        expresion = normalizar_expresion(expresion)
        marcador = f"#{idx}"
        expresiones.append(f"({expresion}){marcador}")
        token_map[marcador] = nombre_token

    # print("\n--- TOKEN MAP ---")
    # print(token_map)

    expresion_global = "|".join(expresiones)
    # print("\n--- EXPRESION GLOBAL ---")
    # print(expresion_global)
    logger.info(f"Expresión global: {expresion_global}")


    postfix = infixToPostfix(expresion_global)
    # print("\n--- POSTFIX TOKENS ---")
    # print(f"Postfix: {postfix}")
    logger.info(f"POSTFIX global: {postfix}")

    arbol = construirArbolSintactico(postfix)
    print("------------árbol sintáctico---------")
    imprimirArbolSintactico(arbol, "", True)

    followpos = defaultdict(set)
    calcular_followPos(arbol, followpos)

    posicion_a_simbolo = {}
    mapear_posiciones_simbolos(arbol, posicion_a_simbolo)

    # Mapear las posiciones finales con marcador #i a su token correspondiente
    for pos, simbolo in posicion_a_simbolo.items():
        if simbolo in token_map:
            posicion_a_token[pos] = token_map[simbolo]

    afd, estados_dict, estado_id_a_conjunto = construir_AFD(arbol, followpos)

    # Marcar estados finales con token
    estado_a_token = {}
    for estado_id, conjunto_pos in estado_id_a_conjunto.items():
        for pos in conjunto_pos:
            if pos in posicion_a_token:
                estado_a_token[estado_id] = posicion_a_token[pos]
                afd.agregar_estado_final(estado_id)

    # visualize_afd(afd, output_dir=OUTPUT_DIR, file_name="AFD_Unificado")

    # print("\nSímbolos en transiciones del AFD:")
    # for origen, trans in afd.transiciones.items():
    #     for simbolo in trans:
    #         print(f"  {origen} -- {repr(simbolo)} --> {trans[simbolo]}")

    return LexicalAutomata(afd=afd, estado_a_token=estado_a_token)

def _serialize_automata(automata: LexicalAutomata, output_name: str):
    new_dir = os.path.join(OUTPUT_DIR, output_name)
    os.makedirs(new_dir, exist_ok=True)
    pickle_file_path = os.path.join(new_dir, "lexicalAutomata.pkl")
    with open(pickle_file_path, "wb") as f:
        pickle.dump(automata, f)
    logger.info(f"Automata serializado en {pickle_file_path}")

def simular_texto(texto: str, automata: LexicalAutomata) -> List[List[str]]:
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

# === MAIN ===
#
# ruta = "./Test.txt"
# texto_prueba = leerArchivo(ruta)
#
# if texto_prueba is None:
#     print(f"Error al leer el archivo {ruta}. Asegúrate de que existe y es accesible.")
#     sys.exit(1)
#
# # tokens = {
# #     "NUMBER": "(((0|1|2|3|4|5|6|7|8|9)+)(\.((0|1|2|3|4|5|6|7|8|9)+))?(E(\+|-)?((0|1|2|3|4|5|6|7|8|9)+)))?",
# #     "WORD": "(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)+",
# #     "WHITESPACE": "( |\t|\n)+",
# #     "COND" : "if|else|while|for|return",
# #     "ID": "((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*)",
# #     "EQUAL": "=",
# #     "PLUS": "\\+",
# #     "MINUS": "-",
# #     "LPAREN": "\\(",
# #     "RPAREN": "\\)",
# #     "LBRACE": "\\{",
# #     "RBRACE": "\\}",
# #     "MULT": "\\*",
# # }
# tokens = {
#     "WS": "( |\t|\n)+",
#     "COND" : "if|else|while|for|return",
#     "NUMBER": "(((0|1|2|3|4|5|6|7|8|9))+)((\.)((((0|1|2|3|4|5|6|7|8|9))+)))?(E((\+)|-)?((((0|1|2|3|4|5|6|7|8|9))+)))?",
#     "ID": "((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)(((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*))",
#     "PLUS": "\\+",
#     "TIMES": "\\*",
#     "LPAREN": "\\(",
#     "RPAREN": "\\)"
# }
#
# lexical_automata = generar_afd_unificado(tokens)
# _serialize_automata(lexical_automata, "lexical_out")
#
# print("\nContenido de Test.txt: \n")
# print(texto_prueba)
#
# print("\n--- SIMULANDO texto ---")
# resultado = simular_texto(texto_prueba, lexical_automata)
# for i in resultado:
#     print(i)
