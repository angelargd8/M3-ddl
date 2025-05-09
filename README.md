# M3-ddl: Proyecto de generador sintactico: 

## Resumen: 
    Con una gramatica independiente del contexto que esta escrita en lenguaje yapar. Se encuentra la gramatica y con ella se construye el conjunto canonico de Items LR(0). A partir de los items canónicos LR(0) se construye la tabla de análisis sintáctico. Luego, con los tokens que devuelve el lexer. Se simula la tabla de análisis sintáctico y dice si la oración compuesta por los tokens pertenece o no a la grámatica entrada del proyecto. 