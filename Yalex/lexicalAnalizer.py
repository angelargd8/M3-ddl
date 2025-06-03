import pickle
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Yalex.generator import LexicalAutomata
from typing import Dict, List


def get_pickle_automata(file_path) -> LexicalAutomata:
    with open(
        file_path,
        "rb",
    ) as file:
        automata = pickle.load(file)
    return automata


def simular_texto(texto: str, automata: LexicalAutomata) -> List[List[str]]:
    resultados = []
    i = 0
    while i < len(texto):
        estado_actual = automata.afd.estado_inicial
        j = i
        ultimo_estado_final = None
        ultima_pos_final = i

        while j < len(texto):
            c = texto[j]
            transiciones = automata.afd.transiciones.get(estado_actual, {})

            if c == "+" or c == "(" or c == ")" or c == "*":
                c = "\\" + c
            if c in transiciones:
                estado_actual = transiciones[c]
                j += 1
                if estado_actual in automata.afd.estados_finales:
                    ultimo_estado_final = estado_actual
                    ultima_pos_final = j
            else:
                break

        if ultimo_estado_final is not None:
            lexema = texto[i:ultima_pos_final]
            token = automata.estado_a_token.get(ultimo_estado_final, "UNKNOWN")
            resultados.append([lexema, token])
            i = ultima_pos_final
        else:
            resultados.append([texto[i], "ERROR"])
            i += 1

    return resultados


def guardar_en_txt(resultados: List[List[str]], ruta_salida: str):
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for palabra, token in resultados:
            f.write(f"{palabra} -> {token}\n")

#
# automata = get_pickle_automata()
#
# # Leer el texto a analizar (puedes cambiar la ruta aquí)
# with open("./random_data_2.txt", "r", encoding="utf-8") as f:
#     texto = f.read()
#
# resultados = simular_texto(texto, automata)
#
# # Guardar resultados
# guardar_en_txt(resultados, "./out2/TokensReadPckl.txt")
# print("Resultados guardados en ./out2/TokensReadPckl.txt")
