"""

Entrada: conjunto de items (ejemplo: {S' → · S})
Salida: I0 que es el conjunto expandido con todos los items que derivan de los no terminales después del punto

"""


def Closure(items: set, producciones: dict) -> set:

    cerrado = set(items)  # Inicializa el conjunto cerrado 

    agregado = True  # Bandera para controlar si se han agregado nuevos items

    while agregado:
        # print("bandera de agregado ")
        agregado = False  # Reinicia la bandera
        items_nuevos = set()  # Conjunto para almacenar nuevos items

        for (nt, cuerpo, punto) in cerrado:

            if punto < len(cuerpo):  # Verifica si hay un no terminal después del punto
                simbolo = cuerpo[punto]

                if simbolo in producciones:  # Verifica si el símbolo es un no terminal
                    for produccion in producciones[simbolo]:
                        item = (simbolo, tuple(produccion), 0)  # Crea un nuevo item con el no terminal y su producción
                        if item not in cerrado:  # Verifica si el item no está en el conjunto
                            # print(f"Agregando item: {item}")
                            items_nuevos.add(item)  # Agrega el item al conjunto de nuevos items

        if items_nuevos:  # Si hay nuevos items
            # print(f"Agregando {len(items_nuevos)} items nuevos al conjunto cerrado")
            cerrado.update(items_nuevos)
            agregado = True

    # print(f"\n---------------\nConjunto cerrado: {cerrado}")  # Imprime el conjunto cerrado
    return cerrado  # Devuelve el conjunto cerrado final


#esta funcion la sugerio la ia
def imprimir_items(items: set):
    # print("\n//// Items ////")
    for (nt, cuerpo, punto) in items:
        antes_punto = " ".join(cuerpo[:punto])
        despues_punto = " ".join(cuerpo[punto:])
        print(f"{nt} → {antes_punto} · {despues_punto}")