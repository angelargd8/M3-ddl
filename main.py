from first import *
from constructor import *

def main():

    gramatica = leerArchivo("cfg.txt")
    #calcularFirst
    first = First(gramatica)
    # print(first)
    
    #calcularFollow

main()