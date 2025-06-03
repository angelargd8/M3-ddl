import os
from typing import List, Union
from collections import defaultdict

# leer el archivo

"""
Al refactorizar el leer el archivo se uso IA,
porque la verdad ya no nos recordabamos que habiamos hecho un buffer
"""

"""
 lector secuencial carácter por carácter desde un archivo de texto, 
 simulando el comportamiento de un buffer de entrada como los usados en 
 analizadores léxicos 

"""
class BufferLectura:
    def __init__(self, filepath: str):
        # objeto de archivo abierto para lectura en modo texto r
        self.file = open(filepath, "r", encoding="utf-8")
        #bandera que indica si se ha alcanzado el final del archivo
        self.eof = False

    """Devuelve el siguiente carácter del archivo"""
    def next_char(self) -> str:
        
        if self.eof:
            return ""

        char = self.file.read(1)
        if not char:
            self.eof = True
            self.file.close()
            return ""
        return char

    #retorna el propio objeto como un iterador.
    def __iter__(self):
        return self

    #Llama internamente a next_char()
    def __next__(self):
        char = self.next_char()
        #Si el archivo ha terminadolanza StopIteration para compatibilidad con for
        if char == "":
            raise StopIteration
        #Si no, retorna el siguiente caracter
        return char


import os
from typing import Union


def leerArchivo(file: str) -> Union[str, str]:
    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, file)

        buffer = BufferLectura(file_path)
        contenido = ""

        for char in buffer:
            contenido += char

        print(contenido, type(contenido))
        return contenido
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except IOError:
        return "Error al leer el archivo"


def leerYapar(filepath: str):
    buffer = BufferLectura(filepath)

    tokens = set()
    ignore = set()
    producciones = defaultdict(list)
    current_non_terminal = None

    linea_actual = ""

    # Leer linea por linea, reconstruyendola desde caracteres
    for char in buffer:
        if char == "\n":
            line = linea_actual.strip()
            linea_actual = ""

            # Ignorar líneas vacías y comentarios
            if not line or line.startswith("/*") or line.startswith("//"):
                continue
            
            # Extraer IGNORE
            if line.startswith("IGNORE"):
                ignore.update(line.replace("IGNORE", "").split())
                continue
            
            # Extraer %token
            if line.startswith("%token"):
                tokens.update(line.replace("%token", "").split())
                continue

            # Detectar nuevo no terminal
            if line.endswith(":"):
                current_non_terminal = line[:-1].strip()
                continue

            # Agregar producciones asociadas al no terminal actual
            if current_non_terminal and ("|" in line or ";" in line or line):
                if ";" in line:
                    line = line.replace(";", "")
                partes = [p.strip() for p in line.split("|")]
                for parte in partes:
                    symbols = parte.split()
                    if symbols:
                        producciones[current_non_terminal].append(symbols)
        else:
            linea_actual += char

    # Procesar la última línea si no termina en \n
    if linea_actual:
        line = linea_actual.strip()
        if line and not line.startswith("/*") and not line.startswith("//"):
            if line.startswith("IGNORE"):
                ignore.update(line.replace("IGNORE", "").split())
            elif line.startswith("%token"):
                tokens.update(line.replace("%token", "").split())
            elif line.endswith(":"):
                current_non_terminal = line[:-1].strip()
            elif current_non_terminal:
                if ";" in line:
                    line = line.replace(";", "")
                partes = [p.strip() for p in line.split("|")]
                for parte in partes:
                    symbols = parte.split()
                    if symbols:
                        producciones[current_non_terminal].append(symbols)

    return sorted(tokens), producciones, sorted(ignore)