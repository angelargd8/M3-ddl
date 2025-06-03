from Automata.Node import *
from Automata.metachar import Metachar
from typing import List, Union


#arbol sintactico
#1. preparar stack vacio
#2. pricesar cada simbolo de la expresion postfix
#3. crear nosots para cada operando 

#funciones del arbol sintactico
#anulable, primerapos, ultimapos, siguientepos

def tokenize_postfix(postfix: Union[str, list]) -> list:

    if isinstance(postfix, str):
        postfix = list(postfix)

    tokens = []
    i = 0
    while i < len(postfix):

        if postfix[i] == '@':
            marcador = '@'
            j = i + 1
            while j < len(postfix):
                marcador += postfix[j]
                if postfix[j] == '@':
                    tokens.append(marcador)
                    i = j + 1
                    break
                j += 1
            else:
                tokens.append('@')
                i += 1
            continue

        if postfix[i] == '[':
            grupo = '['
            j = i + 1
            while j < len(postfix):
                grupo += postfix[j]
                if postfix[j] == ']':
                    tokens.append(grupo)
                    i = j + 1
                    break
                j += 1
            else:
                # No se cerró bien el grupo, tratamos carácter por carácter
                tokens.append('[')
                i += 1
            continue

        #manejo de caracteres escapados
        if postfix[i] == "\\":
            if i + 1 < len(postfix):
                #caso 1: escapes comunes: \n, \t, \r, \v, \\
                if postfix[i + 1] in {"n", "t", "r", "v", "\\"}:
                    tokens.append(postfix[i] + postfix[i + 1])
                    i += 2
                    continue

                #caso 2: \+ o \- \.
                if postfix[i + 1] == "\\" and i + 2 < len(postfix):
                    escaped_char = postfix[i + 2]
                    tokens.append("\\" + escaped_char)  #\+
                    i += 3
                    continue

                #cualquier otro tipo de escape
                tokens.append(postfix[i] + postfix[i + 1])
                i += 2
                continue



        # Manejo de literales entre comillas
        elif postfix[i] in {"'", '"', "`"}:
            # Si el literal empieza con una comilla, buscar el cierre
            # y agregarlo como un token completo
            quote_char = postfix[i]
            literal = postfix[i]
            i += 1
            while i < len(postfix):
                literal += postfix[i]
                if postfix[i] == quote_char:
                    break
                i += 1
            tokens.append(literal)
            i += 1
        else:
            tokens.append(postfix[i])
            i += 1
    return tokens


def construirArbolSintactico(tokens: Union[str, List[str]]) -> Node:
    # funcion recursiva de backtracking para construir el arbol sintactico
    def backtrack(index):
        # print("index: " + str(index))
        token = tokens[index]
        # print(f"////////// token '{token}'")

        #no es un operador, puede ser epsilon o un literal
        if not Metachar.IsBinaryOperator(token) and not Metachar.IsUnaryOperator(token):
            # print("OPERANDO: " + str(token))
            node = Node(token)
            node.firstpos.add(node.id)
            node.lastpos.add(node.id)
            node.nullable = token in ['ε']
            return node, index - 1
        
        #es un operador unario puede tener un hijo 
        if Metachar.IsUnaryOperator(token):
            # print("UNARIO: " + str(token))
            child, next_index = backtrack(index - 1)
            node = Node(token)
            node.left = child
            node.nullable = token in ['*', '?'] or child.nullable # '*' y '?' permiten 0 ocurrencias, por eso son anulables
            node.firstpos = child.firstpos.copy()
            node.lastpos = child.lastpos.copy()
            return node, next_index
 
        #es un operador binario puede tener dos hijos
        if Metachar.IsBinaryOperator(token):
            # print("BINARIO: " + str(token))
            right, i1 = backtrack(index - 1 )
            left, i2 = backtrack(i1)
            node = Node(token)
            node.left = left
            node.right = right


            #concatenacion
            if token == '.':
                node.nullable = left.nullable and right.nullable
                node.firstpos = left.firstpos if not left.nullable else left.firstpos | right.firstpos
                node.lastpos = right.lastpos if not right.nullable else right.lastpos | left.lastpos
            #union
            elif token == '|':
                node.nullable = left.nullable or right.nullable
                node.firstpos = left.firstpos | right.firstpos
                node.lastpos = left.lastpos | right.lastpos
            
            return node, i2
        
        raise ValueError(f"Token no reconocido: {token}")
    
    raiz, _ = backtrack(len(tokens) - 1)
    print("===ARBOL SINTACTICO CONSTRUIDO===")
    # print("Raiz: " + str(raiz.displayValue()))
    return raiz


"""
esta funcion fue sacada con algo de ayuda de chat porque no salian bien las sangria sjakjsd
"""
def imprimirArbolSintactico(nodo: Node, sangria: str = "", es_ultimo: bool = True):    
    # nodo actual con sangria
    if sangria:
        if es_ultimo:
            print(sangria + "└─ " + str(nodo.displayValue()) + " (" + str(nodo.nullable) +  ") " )# + str(nodo.firstpos))
            sangria_nueva = sangria + "   "
        else:
            print(sangria + "├─ " + str(nodo.displayValue()) + " (" + str(nodo.nullable) +   ") " )# + str(nodo.firstpos) )
            sangria_nueva = sangria + "│  "
    else:
        print(str(nodo.__str__()))
        # print(str(nodo.displayValue()) + f" (nullable={nodo.nullable})")

        sangria_nueva = "   "  # sangria para los hijos del nodo raiz

    # hijos recursivos
    if nodo.left:
        imprimirArbolSintactico(nodo.left, sangria_nueva, nodo.right is None)
    if nodo.right:
        imprimirArbolSintactico(nodo.right, sangria_nueva, True)
