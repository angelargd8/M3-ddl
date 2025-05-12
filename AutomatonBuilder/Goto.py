from AutomatonBuilder.Closure import *

"""

Entrada: conjunto de items I, símbolo X
Salida: conjunto de items con el punto movido y cerrado

Lo que hace goto es buscar el simbolo gramatical que le estoy enviando en la funcion
buscar el simbolo gramatical del lado derecho del puntito o el puntito esta a la izquierda 
del simbolo gramatical, lo que se hace es mover el puntito a la derecha del simbolo gramatical


entonces hay que buscar los simbolos gramaticales que tienen el puntito a la izquierda de un no terminal

#i0 y los simbolos gramaticales 
goto(I0, E)
X: simbolo gramatical
el resultado hay que aplicarle el closure
"""


def goto(I: set, X: str, producciones: dict) -> set:
    # print(f"goto({I}, {X})")
    
    nuevos_items = set()  # Inicializa el conjunto de nuevos items

    for (nt, cuerpo, punto) in I:  # Itera sobre los items en el conjunto I
        #si el punto esta antes que X
        if punto < len(cuerpo) and cuerpo[punto] == X:
            #mover el punto a la derecha
            nuevo_item = (nt, cuerpo, punto + 1)  # Crea un nuevo item con el punto movido a la derecha
            nuevos_items.add(nuevo_item)

    #aplica el closure a los nuevos items
    nuevos_items = Closure(nuevos_items, producciones)
    return frozenset(nuevos_items)  



