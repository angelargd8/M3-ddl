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

    
main()
