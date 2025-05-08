from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *


def main():

    gramatica = leerArchivo("cfg.txt")

    #---grammar procesor--
    # calcularFirst
    first = First(gramatica)
    # print(first)

    # calcularFollow
    follow = calcularFollow(gramatica, first)
    print(follow)

    #-- automaton builder--

    #construir items LR(0)
    #calculo de closure(I)
    #calculo de goto(I,X)

main()
