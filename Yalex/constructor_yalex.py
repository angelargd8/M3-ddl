import os
from typing import List, Union

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

    #retorna el propio objeto como un iterador
    def __iter__(self):
        return self

    #Llama internamente a next_char()
    def __next__(self):
        char = self.next_char()
        #Si el archivo ha terminadolanza StopIteration para compatibilidad con for
        if char == "":
            raise StopIteration
        #Si no, retorna el siguiente carácter
        return char


def leerArchivo_yalex(file: str):
    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, file)

        buffer = BufferLectura(file_path)
        contenido = ""

        # Lee el archivo caracter por caracter
        for char in buffer:
            contenido += char

        # Elimina espacios en blanco al principio y final
        contenido = contenido.strip()
        return contenido if contenido else None

    except FileNotFoundError:
        print(f"[ERROR] El archivo no fue encontrado: {file}")
    except Exception as e:
        print(f"[ERROR] Al leer el archivo '{file}': {e}")
    return None

def guardar_resultado_en_txt(resultados, archivo_salida):
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for palabra, token in resultados:
            f.write(f"{palabra} -> {token}\n")
