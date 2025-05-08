from GrammarProcesor.First import *
from constructor import *
from GrammarProcesor.Follow import *


def main():

    gramatica = leerArchivo("cfg.txt")
    # calcularFirst
    first = First(gramatica)
    # print(first)

    # calcularFollow
    follow = calcularFollow(gramatica, first)
    print(follow)


main()
