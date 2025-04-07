import os
from typing import List, Union

# leer el archivo

"""
Al refactorizar el leer el archivo se uso IA, y se aplico 
Union[List[str], str] en vez de solo '-> str', como se tenia en el lab de buffer
ya que la IA, recomendo devolver Union[List[str], str] 
para indicar que puede devolver una lista de cadenas o un mensaje de error
"""


def leerArchivo(file: str) -> Union[List[str], str]:
    try:
        script_dir = os.path.dirname(__file__)  # Directorio del script actual
        file_path = os.path.join(script_dir, file)

        with open(file_path, "r", encoding="utf-8") as f:
            expresiones = f.read().split("\n")

        print(expresiones, type(expresiones))
        return expresiones
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except IOError:
        return "Error al leer el archivo"

