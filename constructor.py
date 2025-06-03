import os
from typing import List, Union
from collections import defaultdict

# leer el archivo

"""
Al refactorizar el leer el archivo se uso IA, y se aplico 
Union[List[str], str] en vez de solo '-> str', como se tenia en el lab de buffer
ya que la IA, recomendo devolver Union[List[str], str] 
para indicar que puede devolver una lista de cadenas o un mensaje de error
"""


def leerArchivo(file: str) -> Union[List[str], str]:
    try:
        script_dir = os.path.dirname(__file__) # Directorio del script actual
        file_path = os.path.join(script_dir, file)

        with open(file_path, "r", encoding="utf-8") as f:
            contenido = []
            linea_actual = ""
            while True:
                char = f.read(1)
                if not char:
                    if linea_actual:
                        contenido.append(linea_actual)
                    break
                if char == "\n":
                    contenido.append(linea_actual)
                    linea_actual = ""
                else:
                    linea_actual += char

        print(contenido, type(contenido))
        return contenido
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except IOError:
        return "Error al leer el archivo"


def leerYapar(filepath: str):

    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        linea_actual = ""
        while True:
            char = f.read(1)
            if not char:
                if linea_actual:
                    lines.append(linea_actual)
                break
            if char == "\n":
                lines.append(linea_actual)
                linea_actual = ""
            else:
                linea_actual += char

    tokens = set()
    ignore = set()
    producciones = defaultdict(list)
    current_non_terminal = None


    for line in lines:
        line = line.strip()

        #ignorar las vacias y comentarios
        if not line or line.startswith("/*") or line.startswith("//"):
            continue

        #detectar ignore
        if line.startswith("IGNORE"):
            ignore.update(line.replace("IGNORE", "").split())
            continue

        #detectar tokens
        if line.startswith("%token"):
            tokens.update(line.replace("%token", "").split())
            continue

        #detectar nuevas reglas, como expresiones
        if line.endswith(":"):
            current_non_terminal = line[:-1].strip()
            continue

        #detectar producciones
        if current_non_terminal and ("|" in line or ";" in line or line):
            # Si hay un punto y coma, eliminarlo
            if ";" in line:
                line = line.replace(";", "")

            partes = [partes.strip() for partes in line.split("|")]

            for parte in partes:
                symbols = parte.split()
                if symbols:
                    producciones[current_non_terminal].append(symbols)

    tokens = sorted(set(tokens))  # Ordenar los tokens, esto es para que cada ves que se repita, sea en el mismo orden

    return tokens, producciones, sorted(ignore)

    