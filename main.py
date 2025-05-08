from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *


def main():

    # gramatica = leerArchivo("cfg.txt")

    #agregar validacion de archivo y que sean varios xd
    archivo = "./yapar/slr-1.yalp"
    tokens, producciones = leerYapar(archivo)
    
    print("//// Tokens: ////")
    for token in tokens:
        print(token)

    print("//// Producciones: ////")
    for no_terminal in producciones: 
        for cuerpo in producciones[no_terminal]:
            print(f"{no_terminal} -> {' '.join(cuerpo)}")


    #---grammar procesor--
    # calcularFirst
    first = First(producciones)
    # print(first)

    # # calcularFollow
    # follow = calcularFollow(gramatica, first)
    # print(follow)

    # #-- automaton builder--

    # #construir items LR(0)
    # #calculo de closure(I)
    # #calculo de goto(I,X)

main()
