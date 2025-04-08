from first import *
from constructor import *
from follow import *

def main():

    gramatica = leerArchivo("cfg.txt")
    #calcularFirst
    first = First(gramatica)
    # print(first)
    f = calcularFollow(gramatica, first)
    #calcularFollow


main()