import os
from typing import List, Union

# leer el archivo

"""
Al refactorizar el leer el archivo se uso IA, y se aplico 
Union[List[str], str] en vez de solo '-> str', como se tenia en el lab de buffer
ya que la IA, recomendo devolver Union[List[str], str] 
para indicar que puede devolver una lista de cadenas o un mensaje de error
"""


# def leerArchivo(file: str) -> Union[List[str], str]:
#     try:
#         script_dir = os.path.dirname(__file__)  # Directorio del script actual
#         file_path = os.path.join(script_dir, file)

#         with open(file_path, "r", encoding="utf-8") as f:
#             expresiones = f.read().split("\n")

#         print(expresiones, type(expresiones))
#         return expresiones
#     except FileNotFoundError:
#         return "El archivo no fue encontrado"
#     except IOError:
#         return "Error al leer el archivo"

def leerArchivo_yalex(file: str):
    try:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, file)

        with open(file_path, "r", encoding="utf-8") as f:
            contenido = f.read().strip()
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
