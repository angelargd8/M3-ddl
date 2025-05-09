"""

Entrada: conjunto de items (ejemplo: {S' → · S})
Salida: I0 que es el conjunto expandido con todos los items que derivan de los no terminales después del punto

"""


def Closure(producciones: dict) -> set:

    cerrado = set()  # Inicializa el conjunto cerrado 

    simbolo_inicial = list(producciones.keys())[0]  # Obtiene el primer símbolo no terminal
    simbolo_aumentado = simbolo_inicial + "'"  # Aumenta el símbolo inicial

    #crear produccion aumentada
    producciones[simbolo_aumentado] = [[simbolo_inicial]]  # Agrega la producción aumentada al diccionario

    #crear el item inicial 
    cerrado.add((simbolo_aumentado, (simbolo_inicial,), 0) ) # Agrega el item inicial al conjunto cerrado


    agregado = True  # Bandera para controlar si se han agregado nuevos items

    while agregado:
        print("bandera de agregado ")
        agregado = False  # Reinicia la bandera
        items_nuevos = set()  # Conjunto para almacenar nuevos items

        for (nt, cuerpo, punto) in cerrado:

            if punto < len(cuerpo):  # Verifica si hay un no terminal después del punto
                simbolo = cuerpo[punto]

                if simbolo in producciones:  # Verifica si el símbolo es un no terminal
                    for produccion in producciones[simbolo]:
                        item = (simbolo, tuple(produccion), 0)  # Crea un nuevo item con el no terminal y su producción
                        if item not in cerrado:  # Verifica si el item no está en el conjunto
                            items_nuevos.add(item)  # Agrega el item al conjunto de nuevos items

        if items_nuevos:  # Si hay nuevos items
            cerrado.update(items_nuevos)
            agregado = True

    # print(f"Conjunto cerrado: {cerrado}")  # Imprime el conjunto cerrado
    return cerrado  # Devuelve el conjunto cerrado final


def imprimir_items(items: set):
    print("\n//// Items LR(0) ////")
    for (nt, cuerpo, punto) in items:
        antes_punto = " ".join(cuerpo[:punto])
        despues_punto = " ".join(cuerpo[punto:])
        print(f"{nt} → {antes_punto} · {despues_punto}")