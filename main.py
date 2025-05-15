from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *
from AutomatonBuilder.ConstruirAutomata import *
from AutomatonBuilder.grafico import *



def main():

    #agregar validacion de archivo y que sean varios xd
    archivo = "./yapar/slr-1.yalp"
    tokens, producciones = leerYapar(archivo)
    
    print("//// Tokens: ////")
    for token in tokens:
        print(token)

    print("//// Producciones: ////")
    for no_terminal in sorted(producciones): 
        for cuerpo in sorted(producciones[no_terminal]):
            print(f"{no_terminal} → {' '.join(cuerpo)}")


    #---grammar procesor--
    # calcularFirst
    first = First(producciones)

    # calcularFollow
    follow = calcularFollow(producciones, first)
    print(follow)

    #-- automaton builder--
    # automata LR(0)
    estados, transiciones, estados_id, estado_aceptacion = ConstruirAutomata(producciones) 
    graficar_automata(estados, transiciones, estados_id, estado_aceptacion)

    #-- LR-Parsing Algorithm--
    #tomar de entrada el conjunto canonico de items LR0
    #y se va a transformar en una estructura de datos, para simular el algoritmo de parsing
    #se usa una pila para simular el automata de pila
    #va a consumir token tras token 
    #consume token tras token y usa la pila y consulta la table slr para determinar la accion que debe de tomar el analizador
    #la tabla slr accion|goto
    #la salida es si: si la secuencia de tokens que tenemos en la entrada construye una oracion valida a partir de de la gramatica libre de contexto
    #la salida es no: si tenemos errores sintacticos, es cuando la tabla slr no se capaz de decirnos que hacer

    
main()
