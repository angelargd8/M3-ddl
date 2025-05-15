"""
Action|Goto
se construye a partir de la gramatica, con el conjunto de items canonicos  LR(0)

action: terminales
goto: no terminales

la interseccion de una fila y una columna , tiene un nombre, dependiendo si la columna es un token o un no terminal, 
es accion si es con un token, o goto si es con un no terminal.

action: shift (S), reduce (r), accept solo en una interseccion(acc), error, cualquier entrada que no tenga una accion definida, cuando se busca de un estado
y esta una celda en blanco

si llego a error, es porque hay un error sintactico, no se puede continuar el analisis

goto: codifica el automata finito LR(0) 
por ejemplo si estamos en el estado 0 y leo una E, entonces voy al estado 1. Si estoy en el estado 0 y leo una t, voy al I2
pero solo esta formada por simbolor no terminales.
"""

