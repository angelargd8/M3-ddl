from first import *
from constructor import *
from follow import *


def main():

    gramatica = leerArchivo("cfg.txt")
    # calcularFirst
    first = First(gramatica)
    # print(first)
    follow = calcularFollow(gramatica, first)
    # calcularFollow
    print(follow)


main()
